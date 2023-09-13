import logging
from pathlib import Path
from typing import Dict, List, Type
from pydantic import TypeAdapter

from cg.apps.demultiplex.sample_sheet.models import (
    FlowCellSample,
    FlowCellSampleBCLConvert,
    FlowCellSampleBcl2Fastq,
    SampleSheet,
)
from cg.constants.constants import FileFormat
from cg.constants.demultiplexing import (
    BclConverter,
    SampleSheetBcl2FastqSections,
    SampleSheetBCLConvertSections,
)
from cg.constants.sequencing import Sequencers

from cg.exc import SampleSheetError
from cg.io.controller import ReadFile

LOG = logging.getLogger(__name__)


def validate_samples_are_unique(samples: List[FlowCellSample]) -> None:
    """Validate that each sample only exists once."""
    sample_ids: set = set()
    for sample in samples:
        sample_id: str = sample.sample_id.split("_")[0]
        if sample_id in sample_ids:
            message: str = f"Sample {sample.sample_id} exists multiple times in sample sheet"
            LOG.warning(message)
            raise SampleSheetError(message)
        sample_ids.add(sample_id)


def validate_samples_unique_per_lane(samples: List[FlowCellSample]) -> None:
    """Validate that each sample only exists once per lane in a sample sheet."""
    sample_by_lane: Dict[int, List[FlowCellSample]] = get_samples_by_lane(samples)
    for lane, lane_samples in sample_by_lane.items():
        LOG.debug(f"Validate that samples are unique in lane: {lane}")
        validate_samples_are_unique(samples=lane_samples)


def get_sample_sheet_from_file(
    infile: Path,
    flow_cell_sample_type: Type[FlowCellSample],
) -> SampleSheet:
    """Parse and validate a sample sheet from file."""
    sample_sheet_content: List[List[str]] = ReadFile.get_content_from_file(
        file_format=FileFormat.CSV, file_path=infile
    )
    return get_validated_sample_sheet(
        sample_sheet_content=sample_sheet_content,
        sample_type=flow_cell_sample_type,
    )


def get_sample_type_from_sequencer_type(sequencer_type: str) -> Type[FlowCellSample]:
    bcl_converter: str = get_bcl_converter_by_sequencer(sequencer_type)
    if bcl_converter == BclConverter.BCL2FASTQ:
        return FlowCellSampleBcl2Fastq
    return FlowCellSampleBCLConvert


def get_bcl_converter_by_sequencer(sequencer_type: str) -> str:
    """Return the BCL converter based on the sequencer."""
    if sequencer_type in [Sequencers.NOVASEQ, Sequencers.NOVASEQX]:
        return BclConverter.DRAGEN
    return BclConverter.BCL2FASTQ


def get_validated_sample_sheet(
    sample_sheet_content: List[List[str]],
    sample_type: Type[FlowCellSample],
) -> SampleSheet:
    """Return a validated sample sheet object."""
    raw_samples: List[Dict[str, str]] = get_raw_samples(sample_sheet_content=sample_sheet_content)
    adapter = TypeAdapter(List[sample_type])
    samples = adapter.validate_python(raw_samples)
    validate_samples_unique_per_lane(samples=samples)
    return SampleSheet(samples=samples)


def get_raw_samples(sample_sheet_content: List[List[str]]) -> List[Dict[str, str]]:
    """Return the samples in a sample sheet as a list of dictionaries."""
    header: List[str] = []
    raw_samples: List[Dict[str, str]] = []

    for line in sample_sheet_content:
        # Skip lines that are too short to contain samples
        if len(line) <= 5:
            continue
        if line[0] in [
            SampleSheetBcl2FastqSections.Data.FLOW_CELL_ID.value,
            SampleSheetBCLConvertSections.Data.LANE.value,
        ]:
            header = line
            continue
        if not header:
            continue
        raw_samples.append(dict(zip(header, line)))
    if not header:
        message = "Could not find header in sample sheet"
        LOG.warning(message)
        raise SampleSheetError(message)
    if not raw_samples:
        message = "Could not find any samples in sample sheet"
        LOG.warning(message)
        raise SampleSheetError(message)
    return raw_samples


def get_samples_by_lane(
    samples: List[FlowCellSample],
) -> Dict[int, List[FlowCellSample]]:
    """Group and return samples by lane."""
    LOG.debug("Order samples by lane")
    sample_by_lane: Dict[int, List[FlowCellSample]] = {}
    for sample in samples:
        if sample.lane not in sample_by_lane:
            sample_by_lane[sample.lane] = []
        sample_by_lane[sample.lane].append(sample)
    return sample_by_lane


def get_sample_internal_ids_from_sample_sheet(
    sample_sheet_path: Path, flow_cell_sample_type: Type[FlowCellSample]
) -> List[str]:
    """Return the sample internal ids for samples in the sample sheet."""
    sample_sheet = get_sample_sheet_from_file(
        infile=sample_sheet_path, flow_cell_sample_type=flow_cell_sample_type
    )
    return sample_sheet.get_sample_ids()
