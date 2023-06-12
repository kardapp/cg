"""Functions that deals with dummy samples"""
from cg.apps.demultiplex.sample_sheet.models import (
    FlowCellSample,
    FlowCellSampleNovaSeq6000Bcl2Fastq,
    FlowCellSampleNovaSeq6000Dragen,
)
from cg.constants.demultiplexing import BclConverter
from typing import Type


def dummy_sample_name(sample_name: str) -> str:
    """Convert a string to a dummy sample name replacing spaces and parentheses with dashes."""
    return sample_name.replace(" ", "-").replace("(", "-").replace(")", "-")


def dummy_sample(
    flow_cell_id: str, dummy_index: str, lane: int, name: str, sample_type: Type[FlowCellSample]
) -> FlowCellSample:
    """Constructs and returns a dummy sample in Novaseq sample sheet format."""
    return sample_type(
        flowcell_id=flow_cell_id,
        lane=lane,
        sample_id=dummy_sample_name(sample_name=name),
        index=dummy_index,
        sample_name="indexcheck",
        project="indexcheck",
    )
