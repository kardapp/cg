from typing import Optional
from cg.store import Store
from cg.store.filters.status_metrics_filters import (
    filter_total_read_count_for_sample,
    filter_metrics_for_flow_cell_sample_internal_id_and_lane,
)
from cg.store.models import SampleLaneSequencingMetrics
from sqlalchemy.orm import Query


def test_filter_total_read_count_for_sample(
    store_with_sequencing_metrics: Store, sample_id: str, expected_total_reads: int
):
    # GIVEN a Store with sequencing metrics
    metrics: Query = store_with_sequencing_metrics._get_query(table=SampleLaneSequencingMetrics)

    # WHEN getting total read counts for a sample
    total_reads_query: Query = filter_total_read_count_for_sample(
        metrics=metrics, sample_internal_id=sample_id
    )

    # THEN assert that the returned object is a Query
    assert isinstance(total_reads_query, Query)

    # THEN a total reads count is returned
    actual_total_reads: Optional[int] = total_reads_query.scalar()
    assert actual_total_reads

    # THEN assert that the actual total read count is as expected
    assert actual_total_reads == expected_total_reads


def test_filter_metrics_for_flow_cell_sample_internal_id_and_lane(
    store_with_sequencing_metrics: Store, sample_id: str, flow_cell_name: str
):
    # GIVEN a Store with sequencing metrics
    metrics: Query = store_with_sequencing_metrics._get_query(table=SampleLaneSequencingMetrics)

    # WHEN getting metrics for a flow cell, sample internal id and lane
    metrics_query: Query = filter_metrics_for_flow_cell_sample_internal_id_and_lane(
        metrics=metrics,
        flow_cell_name=flow_cell_name,
        sample_internal_id=sample_id,
        lane=1,
    )

    # THEN assert that the returned object is a Query
    assert isinstance(metrics_query, Query)

    # THEN assert that the query returns a list of metrics
    assert metrics_query.all()

    # THEN assert that the query returns the expected number of metrics
    assert len(metrics_query.all()) == 1

    # THEN assert that the query returns the expected metrics
    assert metrics_query[0].flow_cell_name == flow_cell_name
    assert metrics_query[0].sample_internal_id == sample_id
    assert metrics_query[0].flow_cell_lane_number == 1
