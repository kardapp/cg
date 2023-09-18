from pathlib import Path
from typing import List, Tuple
from cg.constants.demultiplexing import BclConverter
from cg.models.demultiplex.flow_cell import FlowCellDirectoryData
from cg.store.models import SampleLaneSequencingMetrics
from cg.apps.sequencing_metrics_parser.parsers.bcl2fastq_to_sequencing_statistics import (
    create_bcl2fastq_metrics,
    create_bcl2fastq_undetermined_metrics,
)
from cg.apps.sequencing_metrics_parser.parsers.bcl_convert_to_sequencing_statistics import (
    create_bcl_convert_undetermined_metrics,
    create_sample_lane_sequencing_metrics_from_bcl_convert_metrics_for_flow_cell,
)


def create_sequencing_metrics_for_flow_cell(
    flow_cell_directory: Path, bcl_converter: str
) -> List[SampleLaneSequencingMetrics]:
    """Parse the sequencing metrics data for the correct demultiplexing software into the sequencing statistics model."""
    if bcl_converter == BclConverter.BCLCONVERT or bcl_converter == BclConverter.DRAGEN:
        return create_sample_lane_sequencing_metrics_from_bcl_convert_metrics_for_flow_cell(
            flow_cell_directory
        )
    return create_bcl2fastq_metrics(flow_cell_directory)


def create_undetermined_non_pooled_metrics(
    flow_cell_data: FlowCellDirectoryData,
) -> List[SampleLaneSequencingMetrics]:
    """Return sequencing metrics for any undetermined reads in non pooled lanes."""

    non_pooled_lanes_and_samples: List[
        Tuple[int, str]
    ] = flow_cell_data.sample_sheet.get_non_pooled_lanes_and_samples()

    if flow_cell_data.bcl_converter == BclConverter.BCL2FASTQ:
        return create_bcl2fastq_undetermined_metrics(
            bcl2fastq_flow_cell_path=flow_cell_data.path,
            non_pooled_lane_sample_pairs=non_pooled_lanes_and_samples,
        )
    return create_bcl_convert_undetermined_metrics(
        flow_cell_dir=flow_cell_data.path,
        non_pooled_lane_sample_pairs=non_pooled_lanes_and_samples,
    )
