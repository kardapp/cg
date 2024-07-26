from functools import wraps
from pathlib import Path
from typing import Any, Type

from cg.constants.constants import FileFormat
from cg.constants.pacbio import PacBioDirsAndFiles
from cg.exc import PacBioMetricsParsingError
from cg.io.controller import ReadFile
from cg.services.post_processing.pacbio.metrics_parser.models import (
    BaseMetrics,
    ControlMetrics,
    HiFiMetrics,
    PolymeraseMetrics,
    ProductivityMetrics,
    SmrtlinkDatasetsMetrics,
)
from cg.utils.files import get_file_with_pattern_from_list


def handle_pac_bio_parsing_errors(func):
    """Decorator to catch any metrics parsing error to raise a PacBioMetricsParsingError instead."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as error:
            raise PacBioMetricsParsingError(f"Could not find the metrics file: {error}")
        except Exception as error:
            raise PacBioMetricsParsingError(f"An error occurred while parsing the metrics: {error}")

    return wrapper


def _get_data_model_from_pattern(pattern: str) -> Type[BaseMetrics]:
    """Return the data model based on the pattern."""
    pattern_to_model = {
        PacBioDirsAndFiles.BASECALLING_REPORT: HiFiMetrics,
        PacBioDirsAndFiles.CONTROL_REPORT: ControlMetrics,
        PacBioDirsAndFiles.LOADING_REPORT: ProductivityMetrics,
        PacBioDirsAndFiles.RAW_DATA_REPORT: PolymeraseMetrics,
        PacBioDirsAndFiles.SMRTLINK_DATASETS_REPORT: SmrtlinkDatasetsMetrics,
    }
    return pattern_to_model.get(pattern)


def _parse_report_to_model(report_file: Path, data_model: Type[BaseMetrics]) -> BaseMetrics:
    """Parse the metrics report to a data model."""
    parsed_json: dict = ReadFile.read_file[FileFormat.JSON](report_file)
    if data_model == SmrtlinkDatasetsMetrics:
        return data_model.model_validate(parsed_json[0], from_attributes=True)
    metrics: list[dict[str, Any]] = parsed_json.get("attributes")
    data: dict = {report_field["id"]: report_field["value"] for report_field in metrics}
    return data_model.model_validate(data, from_attributes=True)


@handle_pac_bio_parsing_errors
def get_parsed_metrics_from_file_name(metrics_files: list[Path], file_name: str) -> BaseMetrics:
    report_file: Path = get_file_with_pattern_from_list(files=metrics_files, pattern=file_name)
    data_model: Type[BaseMetrics] = _get_data_model_from_pattern(pattern=file_name)
    return _parse_report_to_model(report_file=report_file, data_model=data_model)
