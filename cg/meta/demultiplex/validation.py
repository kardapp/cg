import logging
from pathlib import Path
from typing import List, Optional

from cg.constants.demultiplexing import DemultiplexingDirsAndFiles
from cg.exc import FlowCellError, MissingFilesError
from cg.meta.demultiplex.utils import get_sample_fastqs_from_flow_cell
from cg.models.demultiplex.flow_cell import FlowCellDirectoryData

LOG = logging.getLogger(__name__)


def is_demultiplexing_complete(flow_cell_directory: Path) -> bool:
    return Path(flow_cell_directory, DemultiplexingDirsAndFiles.DEMUX_COMPLETE).exists()


def is_flow_cell_ready_for_delivery(flow_cell_directory: Path) -> bool:
    return Path(flow_cell_directory, DemultiplexingDirsAndFiles.DELIVERY).exists()


def validate_sample_sheet_exists(flow_cell: FlowCellDirectoryData) -> None:
    sample_sheet_path: Path = flow_cell.sample_sheet_path
    if not sample_sheet_path or not sample_sheet_path.exists():
        raise FlowCellError(f"Sample sheet {sample_sheet_path} does not exist in housekeeper.")
    LOG.debug(f"Found sample sheet {sample_sheet_path} in housekeeper.")


def validate_demultiplexing_complete(flow_cell_output_directory: Path) -> None:
    if not is_demultiplexing_complete(flow_cell_output_directory):
        raise FlowCellError(
            f"Demultiplexing not completed for flow cell directory {flow_cell_output_directory}."
        )


def validate_flow_cell_delivery_status(flow_cell_output_directory: Path, force: bool) -> None:
    if is_flow_cell_ready_for_delivery(flow_cell_output_directory) and not force:
        raise FlowCellError(
            f"Flow cell output directory {flow_cell_output_directory}"
            " has already been processed and is ready for delivery."
        )


def validate_samples_have_fastq_files(flow_cell: FlowCellDirectoryData) -> None:
    """Check if all samples have already a fastq files in the demultiplex directory.
    Raises: MissingFilesError
        When one of the samples does not have enough fastq files in the flow cell
    """
    sample_ids: List[str] = flow_cell.sample_sheet.get_sample_ids()
    for sample_id in sample_ids:
        fastq_files: Optional[List[Path]] = get_sample_fastqs_from_flow_cell(
            flow_cell_directory=flow_cell.path, sample_internal_id=sample_id
        )
        if not fastq_files:
            raise MissingFilesError(f"Sample {sample_id} has no fastq files in flow cell")
    LOG.debug("Flow cell has fastq files for all samples")


def is_flow_cell_ready_for_postprocessing(
    flow_cell_output_directory: Path,
    flow_cell: FlowCellDirectoryData,
    force: bool = False,
) -> None:
    validate_sample_sheet_exists(flow_cell)
    validate_demultiplexing_complete(flow_cell_output_directory)
    validate_flow_cell_delivery_status(
        flow_cell_output_directory=flow_cell_output_directory, force=force
    )
