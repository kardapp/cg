"""Module to test the PacBioStoreService."""

from cg.services.post_processing.pacbio.data_storage_service.pacbio_store_service import (
    PacBioStoreService,
)
from cg.services.post_processing.pacbio.data_transfer_service.dto import PacBioDTOs
from cg.services.post_processing.pacbio.run_data_generator.run_data import PacBioRunData
from cg.store.models import PacBioSMRTCell, PacBioSequencingRun, PacBioSampleSequencingMetrics
from unittest import mock


def test_store_post_processing_data(
    pac_bio_store_service: PacBioStoreService,
    pac_bio_dtos: PacBioDTOs,
    expected_pac_bio_run_data: PacBioRunData,
):
    # GIVEN a PacBioStoreService

    # GIVEN a successful data transfer service

    # WHEN storing data for a PacBio instrument run
    with mock.patch(
        "cg.services.post_processing.pacbio.data_transfer_service.data_transfer_service.PacBioDataTransferService.get_post_processing_dtos",
        return_value=pac_bio_dtos,
    ):
        pac_bio_store_service.store_post_processing_data(expected_pac_bio_run_data)

    # THEN the SMRT cell data is stored
    smrt_cell: PacBioSMRTCell = pac_bio_store_service.store._get_query(PacBioSMRTCell).first()
    assert smrt_cell
    assert smrt_cell.internal_id == pac_bio_dtos.run_device.internal_id

    # THEN the sequencing run is stored
    sequencing_run: PacBioSequencingRun = pac_bio_store_service.store._get_query(
        PacBioSequencingRun
    ).first()
    assert sequencing_run
    assert sequencing_run.well == pac_bio_dtos.sequencing_run.well

    # THEN the sample sequencing metrics are stored
    sample_sequencing_run_metrics: PacBioSampleSequencingMetrics = (
        pac_bio_store_service.store._get_query(PacBioSampleSequencingMetrics).first()
    )
    assert sample_sequencing_run_metrics
    assert (
        sample_sequencing_run_metrics.sample.internal_id
        == pac_bio_dtos.sample_sequencing_metrics[0].sample_internal_id
    )
