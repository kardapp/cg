"""Fixtures for Illumina flow cell objects."""

from pathlib import Path

import pytest

from cg.constants.demultiplexing import DemultiplexingDirsAndFiles
from cg.models.run_devices.illumina_run_directory import (
    IlluminaRunDirectory,
)

# Canonical flow cell runs


@pytest.fixture(scope="module")
def hiseq_x_single_index_flow_cell(
    hiseq_x_single_index_flow_cell_dir: Path,
) -> IlluminaRunDirectory:
    """Return a single-index HiSeqX flow cell."""
    return IlluminaRunDirectory(sequencing_run_path=hiseq_x_single_index_flow_cell_dir)


@pytest.fixture(scope="module")
def hiseq_x_dual_index_flow_cell(
    hiseq_x_dual_index_flow_cell_dir: Path,
) -> IlluminaRunDirectory:
    """Return a dual-index HiSeqX flow cell."""
    return IlluminaRunDirectory(sequencing_run_path=hiseq_x_dual_index_flow_cell_dir)


@pytest.fixture(scope="module")
def hiseq_2500_dual_index_flow_cell(
    hiseq_2500_dual_index_flow_cell_dir: Path,
) -> IlluminaRunDirectory:
    """Return a dual-index HiSeq2500 flow cell."""
    return IlluminaRunDirectory(sequencing_run_path=hiseq_2500_dual_index_flow_cell_dir)


@pytest.fixture(scope="module")
def hiseq_2500_custom_index_flow_cell(
    hiseq_2500_custom_index_flow_cell_dir: Path,
) -> IlluminaRunDirectory:
    """Return a custom-index HiSeq2500 flow cell."""
    return IlluminaRunDirectory(sequencing_run_path=hiseq_2500_custom_index_flow_cell_dir)


@pytest.fixture
def novaseq_6000_pre_1_5_kits_flow_cell(
    illumina_flow_cells_directory: Path,
    novaseq_6000_pre_1_5_kits_flow_cell_full_name: str,
) -> IlluminaRunDirectory:
    """Return a Novaseq6000 flow cell with index settings pre 1.5 kits."""
    return IlluminaRunDirectory(
        Path(illumina_flow_cells_directory, novaseq_6000_pre_1_5_kits_flow_cell_full_name)
    )


@pytest.fixture
def novaseq_6000_post_1_5_kits_flow_cell(
    illumina_flow_cells_directory: Path,
    novaseq_6000_post_1_5_kits_flow_cell_full_name: str,
) -> IlluminaRunDirectory:
    """Return a Novaseq6000 flow cell with index settings post 1.5 kits."""
    return IlluminaRunDirectory(
        Path(illumina_flow_cells_directory, novaseq_6000_post_1_5_kits_flow_cell_full_name)
    )


@pytest.fixture
def novaseq_x_flow_cell(novaseq_x_flow_cell_dir: Path) -> IlluminaRunDirectory:
    """Return a NovaSeqX flow cell."""
    return IlluminaRunDirectory(novaseq_x_flow_cell_dir)


@pytest.fixture
def seven_canonical_flow_cells(
    hiseq_x_single_index_flow_cell: IlluminaRunDirectory,
    hiseq_x_dual_index_flow_cell: IlluminaRunDirectory,
    hiseq_2500_dual_index_flow_cell: IlluminaRunDirectory,
    hiseq_2500_custom_index_flow_cell: IlluminaRunDirectory,
    novaseq_6000_pre_1_5_kits_flow_cell: IlluminaRunDirectory,
    novaseq_6000_post_1_5_kits_flow_cell: IlluminaRunDirectory,
    novaseq_x_flow_cell: IlluminaRunDirectory,
) -> list[IlluminaRunDirectory]:
    """Return a list with the seven canonical flow cells."""
    return [
        hiseq_x_single_index_flow_cell,
        hiseq_x_dual_index_flow_cell,
        hiseq_2500_dual_index_flow_cell,
        hiseq_2500_custom_index_flow_cell,
        novaseq_6000_pre_1_5_kits_flow_cell,
        novaseq_6000_post_1_5_kits_flow_cell,
        novaseq_x_flow_cell,
    ]


# Demultiplexed runs


@pytest.fixture
def novaseqx_flow_cell_with_sample_sheet_no_fastq(
    tmp_demultiplexed_flow_cell_no_fastq_files: Path,
) -> IlluminaRunDirectory:
    """Return a flow cell from a tmp dir with a sample sheet and no sample fastq files."""
    tmp_demultiplexed_flow_cell_no_fastq_files.mkdir(parents=True, exist_ok=True)
    flow_cell = IlluminaRunDirectory(tmp_demultiplexed_flow_cell_no_fastq_files)
    sample_sheet_path = Path(flow_cell.path, DemultiplexingDirsAndFiles.SAMPLE_SHEET_FILE_NAME)
    flow_cell._sample_sheet_path_hk = sample_sheet_path
    return flow_cell


@pytest.fixture
def tmp_bcl_convert_flow_cell(
    tmp_flow_cell_directory_bcl_convert: Path,
) -> IlluminaRunDirectory:
    """Create a flow cell object with flow cell that is demultiplexed."""
    return IlluminaRunDirectory(tmp_flow_cell_directory_bcl_convert)


@pytest.fixture
def hiseq_x_single_index_demultiplexed_flow_cell_with_sample_sheet(
    illumina_demultiplexed_runs_directory: Path,
    hiseq_x_single_index_flow_cell_name: str,
    hiseq_x_single_index_sample_sheet_path: Path,
) -> IlluminaRunDirectory:
    """Return a Novaseq6000 flow cell with a sample sheet."""
    path = Path(illumina_demultiplexed_runs_directory, hiseq_x_single_index_flow_cell_name)
    flow_cell = IlluminaRunDirectory(path)
    flow_cell.set_sample_sheet_path_hk(hiseq_x_single_index_sample_sheet_path)
    return flow_cell


@pytest.fixture
def novaseq_x_demux_runs_flow_cell(novaseq_x_demux_runs_dir: Path) -> IlluminaRunDirectory:
    """Return a NovaSeqX flow cell."""
    return IlluminaRunDirectory(novaseq_x_demux_runs_dir)


@pytest.fixture
def hiseq_2500_dual_index_demux_runs_flow_cell(
    hiseq_2500_dual_index_demux_runs_dir: Path,
) -> IlluminaRunDirectory:
    """Return a HiSeq2500 flow cell."""
    return IlluminaRunDirectory(hiseq_2500_dual_index_demux_runs_dir)
