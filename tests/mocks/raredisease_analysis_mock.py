from pathlib import Path

from cg.constants.constants import FileFormat
from cg.io.controller import ReadFile
from cg.meta.workflow.analysis import AnalysisAPI
from cg.models.analysis import NextflowAnalysis

from cg.models.deliverables.metric_deliverables import MetricsBase


def create_raredisease_metrics_deliverables():
    """Get an raredisease_metrics_deliverables object."""
    metrics_deliverables: dict = ReadFile.get_content_from_file(
        file_format=FileFormat.YAML,
        file_path=Path("tests", "fixtures", "apps", "mip", "case_metrics_deliverables.yaml"),
    )
    return [MetricsBase(**metric) for metric in metrics_deliverables["metrics"]]


class MockNextflowAnalysis(AnalysisAPI):
    """Mock MIP analysis object."""

    @staticmethod
    def get_latest_metadata(family_id=None):
        """Mock get_latest_metadata."""
        # Returns: dict: parsed data
        # Define output dict
        metrics: MetricsBase = create_raredisease_metrics_deliverables()
        return NextflowAnalysis(
            sample_metrics=metrics.sample_id_metrics,
        )
