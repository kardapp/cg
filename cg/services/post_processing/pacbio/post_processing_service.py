from cg.services.post_processing.abstract_classes import PostProcessingService
from cg.services.post_processing.pacbio.data_storage_service.pacbio_store_service import (
    PacBioStoreService,
)
from cg.services.post_processing.pacbio.housekeeper_service.pacbio_houskeeper_service import (
    PacBioHousekeeperService,
)
from cg.services.post_processing.pacbio.run_data_generator.pacbio_run_data_generator import (
    PacBioRunDataGenerator,
)
from cg.services.post_processing.pacbio.run_data_generator.run_data import PacBioRunData


class PacBioPostProcessingService(PostProcessingService):
    """Service for handling post-processing of PacBio sequencing runs."""

    def __init__(
        self,
        run_data_generator: PacBioRunDataGenerator,
        hk_service: PacBioHousekeeperService,
        store_service: PacBioStoreService,
        sequencing_dir: str,
    ):
        self.run_data_generator: PacBioRunDataGenerator = run_data_generator
        self.hk_service: PacBioHousekeeperService = hk_service
        self.store_service: PacBioStoreService = store_service
        self.sequencing_dir: str = sequencing_dir

    def post_process(self, run_name: str):
        run_data: PacBioRunData = self.run_data_generator.get_run_data(
            run_name=run_name, sequencing_dir=self.sequencing_dir
        )
        self.store_service.store_post_processing_data(run_data=run_data)
        self.hk_service.store_files_in_housekeeper(run_data=run_data)
