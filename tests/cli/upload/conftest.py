"""Fixtures for cli balsamic tests"""
import json
import logging
from pathlib import Path

import pytest

from cg.apps.hk import HousekeeperAPI
from cg.apps.lims import LimsAPI
from cg.apps.scoutapi import ScoutAPI
from cg.apps.tb import TrailblazerAPI
from cg.meta.upload.scoutapi import UploadScoutAPI
from cg.meta.workflow.mip_dna import AnalysisAPI
from cg.store import Store

LOG = logging.getLogger(__name__)


@pytest.fixture(scope="function", name="base_context")
def fixture_base_context(analysis_store_single_case: Store) -> dict:
    """context to use in cli"""

    return {
        "scout_api": MockScoutApi(),
        "scout_upload_api": MockScoutUploadApi(),
        "housekeeper_api": MockHK(),
        "tb_api": MockTB(),
        "status": analysis_store_single_case,
    }


@pytest.fixture(scope="function", name="analysis_family_single_case")
def fixture_analysis_family_single():
    """Build an example family."""
    family = {
        "name": "family",
        "internal_id": "yellowhog",
        "panels": ["IEM", "EP"],
        "samples": [
            {
                "name": "proband",
                "sex": "male",
                "internal_id": "ADM1",
                "status": "affected",
                "ticket_number": 123456,
                "reads": 5000000,
            }
        ],
    }
    return family


@pytest.fixture(scope="function")
def hk_api(scout_load_config):
    """Return a hkapi"""
    api = MockHK()
    api.add_file(scout_load_config, None, None)

    return api


@pytest.fixture(scope="function")
def upload_scout_api():
    """Return a upload scout api"""
    api = MockScoutUploadApi()

    return api


def load_family(store, family):
    """Load a family into a status database"""
    analysis_family = family
    base_store = store
    customer = base_store.customer("cust000")
    family = base_store.Family(
        name=analysis_family["name"],
        panels=analysis_family["panels"],
        internal_id=analysis_family["internal_id"],
        priority="standard",
    )
    family.customer = customer
    base_store.add(family)
    application_version = base_store.application("WGTPCFC030").versions[0]
    for sample_data in analysis_family["samples"]:
        sample = base_store.add_sample(
            name=sample_data["name"],
            sex=sample_data["sex"],
            internal_id=sample_data["internal_id"],
            ticket=sample_data["ticket_number"],
            reads=sample_data["reads"],
        )
        sample.family = family
        sample.application_version = application_version
        sample.customer = customer
        base_store.add(sample)
    base_store.commit()
    for sample_data in analysis_family["samples"]:
        sample_obj = base_store.sample(sample_data["internal_id"])
        link = base_store.relate_sample(
            family=family,
            sample=sample_obj,
            status=sample_data["status"],
            father=base_store.sample(sample_data["father"]) if sample_data.get("father") else None,
            mother=base_store.sample(sample_data["mother"]) if sample_data.get("mother") else None,
        )
        base_store.add(link)

    _analysis = base_store.add_analysis(pipeline="pipeline", version="version")
    _analysis.family = family
    _analysis.config_path = "dummy_path"

    base_store.commit()


@pytest.yield_fixture(scope="function", name="analysis_store_trio")
def fixture_analysis_store_trio(base_store, analysis_family):
    """Setup a store instance with a trion loaded for testing analysis API."""
    _store = base_store
    load_family(_store, analysis_family)

    yield _store


@pytest.yield_fixture(scope="function", name="analysis_store_single_case")
def fixture_analysis_store_single(base_store, analysis_family_single_case):
    """Setup a store instance with a single ind case for testing analysis API."""
    _store = base_store
    load_family(_store, analysis_family_single_case)

    yield _store


@pytest.fixture
def hk_mock():
    """docstring for hk_mock"""
    return MockHK()


class MockTB(TrailblazerAPI):
    """Mock of trailblazer """

    def __init__(self):
        """Mock the init"""

    def get_family_root_dir(self, case_id):
        """docstring for get_family_root_dir"""
        return Path("hej")


class MockVersion:
    """Mock a version object"""

    @property
    def id(self):
        return ""


class MockFile:
    """Mock a file object"""

    def __init__(self, path="", to_archive=False, tags=None, **kwargs):
        self.path = path
        self.to_archive = to_archive
        self.tags = tags or []
        self._empty_first = kwargs.get("empty_first", False)

    def first(self):
        if self._empty_first:
            return None
        return MockFile()

    @property
    def full_path(self):
        return str(self.path)

    def is_included(self):
        return False


class MockHK(HousekeeperAPI):
    def __init__(self):
        """Mock the init"""
        self.delivery_report = True
        self.missing_mandatory = False
        self._file_added = False
        self._file_included = False
        self._files = []

    def files(self, **kwargs):
        """docstring for file"""
        tags = set(kwargs.get("tags", []))
        delivery = set(["delivery-report"])
        mandatory = set(["vcf-snv-clinical"])
        if tags.intersection(delivery) and self.delivery_report is False:
            return MockFile(empty_first=True)
        if tags.intersection(mandatory) and self.missing_mandatory is True:
            return MockFile(empty_first=True)
        return MockFile()

    def get_files(self, bundle, tags, version="1.0"):
        """Mock get files sub from Housekeeper"""
        return self._files

    def add_file(self, file, version_obj, tag_name, to_archive=False):
        """Mock add file to the HK database"""
        self._file_added = True
        new_file = MockFile(path=file)
        self._files.append(new_file)
        return new_file

    def version(self, arg1: str, arg2: str):
        """Fetch version from the database."""
        return MockVersion()

    def last_version(self, bundle: str):
        """docstring for last_version"""
        return MockVersion()

    def include_file(self, file_obj, version_obj):
        """docstring for include_file"""
        self._file_included = True

    def add_commit(self, file_obj):
        """docstring for include_file"""
        pass


class MockFamily(object):
    """Mock of family used in store """

    def __init__(self):
        """Mock the init"""
        self.analyses = ["analysis_obj"]


class MockScoutApi(ScoutAPI):
    def __init__(self):
        """docstring for __init__"""
        pass

    def upload(self, scout_config, force=False):
        """docstring for upload"""
        LOG.info("Case loaded successfully to Scout")


class MockAnalysisApi(AnalysisAPI):
    def __init__(self):
        """docstring for __init__"""
        pass

    def get_latest_metadata(self, internal_id):
        """docstring for upload"""
        return {}


class MockScoutUploadApi(UploadScoutAPI):
    def __init__(self, **kwargs):
        """docstring for __init__"""
        self.mock_generate_config = True
        self.housekeeper = MockHK()
        self.analysis = MockAnalysisApi()
        self.config = {}
        self.file_exists = False
        self.lims = MockLims()

    @pytest.fixture(autouse=True)
    def _request_analysis(self, analysis_store_single_case):
        self.analysis = analysis_store_single_case

    def generate_config(self, analysis_obj, **kwargs):
        """Mock the generate config"""
        if self.mock_generate_config:
            return self.config

        return super().generate_config(analysis_obj, **kwargs)

    def save_config_file(self, scout_config, file_path):
        """docstring for save_config_file"""
        return

    def add_scout_config_to_hk(self, file_path, hk_api, case_id):
        """docstring for add_scout_config_to_hk"""
        if self.file_exists:
            raise FileExistsError("Scout config already exists")


class MockLims:
    """Mock lims fixture"""

    lims = None

    def __init__(self):
        self.lims = self

    @staticmethod
    def lims_samples():
        """ Return LIMS-like family samples """
        lims_family = json.load(open("tests/fixtures/report/lims_family.json"))
        return lims_family["samples"]

    def sample(self, sample_id):
        """ Returns a lims sample matching the provided sample_id """
        for sample in self.lims_samples():
            if sample["id"] == sample_id:
                return sample
        return None
