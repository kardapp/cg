from copy import deepcopy
import logging
from pathlib import Path

from marshmallow import Schema, fields, validate
import ruamel.yaml

from cg.exc import PedigreeConfigError
from cg.constants import DEFAULT_CAPTURE_KIT, NO_PARENT


LOG = logging.getLogger(__name__)


class SampleSchema(Schema):
    sample_id = fields.Str(required=True)
    sample_display_name = fields.Str()
    analysis_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=[
                "tga",
                "wes",
                "wgs",
                "wts",
            ]
        ),
    )
    father = fields.Str(default=NO_PARENT)
    mother = fields.Str(default=NO_PARENT)
    phenotype = fields.Str(
        required=True,
        validate=validate.OneOf(choices=["affected", "unaffected", "unknown"]),
    )
    sex = fields.Str(required=True, validate=validate.OneOf(choices=["female", "male", "unknown"]))
    expected_coverage = fields.Float()
    capture_kit = fields.Str(default=DEFAULT_CAPTURE_KIT)


class ConfigSchema(Schema):
    case = fields.Str(required=True)
    default_gene_panels = fields.List(fields.Str(), required=True)
    samples = fields.List(fields.Nested(SampleSchema), required=True)


class ConfigHandler:
    def make_pedigree_config(self, data: dict, pipeline: str = None) -> dict:
        """Make a MIP pedigree config"""
        self.validate_config(data=data, pipeline=pipeline)
        config_data = self.parse_pedigree_config(data)
        return config_data

    @staticmethod
    def validate_config(data: dict, pipeline: str = None) -> dict:
        """Validate MIP pedigree config format"""
        errors = ConfigSchema().validate(data)
        fatal_error = False
        for field, messages in errors.items():
            if isinstance(messages, dict):
                for sample_index, sample_errors in messages.items():
                    try:
                        sample_id = data["samples"][sample_index]["sample_id"]
                    except KeyError:
                        raise PedigreeConfigError("missing sample id")
                    for sample_key, sub_messages in sample_errors.items():
                        if sub_messages != ["Unknown field."]:
                            fatal_error = True
                        LOG.error(f"{sample_id} -> {sample_key}: {', '.join(sub_messages)}")
            else:
                fatal_error = True
                LOG.error(f"{field}: {', '.join(messages)}")
        if fatal_error:
            raise PedigreeConfigError("invalid config input", errors=errors)
        return errors

    @staticmethod
    def parse_pedigree_config(data: dict) -> dict:
        """Parse the pedigree config data"""
        data_copy = deepcopy(data)
        # handle single sample cases with 'unknown' phenotype
        if len(data_copy["samples"]) == 1 and data_copy["samples"][0]["phenotype"] == "unknown":
            LOG.info("setting 'unknown' phenotype to 'unaffected'")
            data_copy["samples"][0]["phenotype"] = "unaffected"
        for sample_data in data_copy["samples"]:
            sample_data["mother"] = sample_data.get("mother") or NO_PARENT
            sample_data["father"] = sample_data.get("father") or NO_PARENT
            if sample_data["analysis_type"] == "wgs" and sample_data.get("capture_kit") is None:
                sample_data["capture_kit"] = DEFAULT_CAPTURE_KIT
        return data_copy

    def write_pedigree_config(self, data: dict) -> Path:
        """Write the pedigree config to the the case dir"""
        out_dir = Path(self.root) / data["case"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "pedigree.yaml"
        dump = ruamel.yaml.round_trip_dump(data, indent=4, block_seq_indent=2)
        out_path.write_text(dump)
        return out_path
