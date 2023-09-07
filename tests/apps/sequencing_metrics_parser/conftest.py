"""Fixtures for the sequencing metrics parser tests."""
from pathlib import Path
from cg.apps.sequencing_metrics_parser.models.bcl_convert import (
    BclConvertDemuxMetrics,
    BclConvertQualityMetrics,
)
from cg.apps.sequencing_metrics_parser.parsers.bcl_convert import BclConvertMetricsParser
import pytest
from cg.constants.bcl_convert_metrics import (
    BclConvertQualityMetricsColumnNames,
    BclConvertDemuxMetricsColumnNames,
)


@pytest.fixture(name="bcl_convert_metrics_dir_path", scope="session")
def fixture_bcl_convert_metrics_dir_path() -> Path:
    """Return a path to a BCLConvert metrics directory."""
    return Path(
        "tests", "fixtures", "apps", "sequencing_metrics_parser", "230622_A00621_0864_AHY7FFDRX2"
    )


@pytest.fixture(name="test_sample_internal_id", scope="session")
def fixture_test_sample_internal_id() -> str:
    """Return a test sample internal id."""
    return "ACC11927A2"


@pytest.fixture(name="test_sample_project", scope="session")
def fixture_test_sample_project() -> str:
    """Return a test sample project."""
    return "405887"


@pytest.fixture(name="test_lane", scope="session")
def fixture_test_lane() -> int:
    """Return a test lane."""
    return 1


@pytest.fixture(name="bcl_convert_reads_for_test_sample", scope="session")
def fixture_bcl_convert_reads_for_test_sample() -> int:
    """Return the number of reads for the test sample."""
    return 15962796


@pytest.fixture(name="bcl_convert_test_q30_bases_percent", scope="session")
def fixture_bcl_convert_test_q30_bases_percent() -> float:
    """Return the Q30 bases percent for the test sample."""
    return 94


@pytest.fixture(name="bcl_convert_test_mean_quality_score_per_lane", scope="session")
def fixture_bcl_convert_test_mean_quality_score() -> float:
    """Return the mean quality score for the test sample."""
    return 36.02


@pytest.fixture(name="bcl_convert_demux_metric_model_with_data", scope="session")
def fixture_bcl_convert_demux_metric_model_with_data(
    test_lane,
    test_sample_internal_id,
    test_sample_project,
) -> BclConvertDemuxMetrics:
    """Return a BclConvertDemuxMetrics model with data."""
    return BclConvertDemuxMetrics(
        **{
            BclConvertDemuxMetricsColumnNames.LANE.value: test_lane,
            BclConvertDemuxMetricsColumnNames.SAMPLE_INTERNAL_ID.value: test_sample_internal_id,
            BclConvertDemuxMetricsColumnNames.READ_PAIR_COUNT.value: 15962796,
        }
    )


@pytest.fixture(name="bcl_convert_quality_metric_model_with_data", scope="session")
def fixture_bcl_convert_quality_metric_model_with_data(
    test_lane, test_sample_internal_id, test_sample_project
) -> BclConvertQualityMetrics:
    """Return a BclConvertQualityMetrics model with data."""
    return BclConvertQualityMetrics(
        **{
            BclConvertQualityMetricsColumnNames.LANE.value: test_lane,
            BclConvertQualityMetricsColumnNames.SAMPLE_INTERNAL_ID.value: test_sample_internal_id,
            BclConvertQualityMetricsColumnNames.MEAN_QUALITY_SCORE_Q30.value: 36.15,
            BclConvertQualityMetricsColumnNames.Q30_BASES_PERCENT.value: 0.95,
        }
    )


@pytest.fixture(name="parsed_bcl_convert_metrics", scope="session")
def fixture_parsed_bcl_convert_metrics(bcl_convert_metrics_dir_path) -> BclConvertMetricsParser:
    """Return an object with parsed BCLConvert metrics."""
    return BclConvertMetricsParser(bcl_convert_metrics_dir_path=bcl_convert_metrics_dir_path)
