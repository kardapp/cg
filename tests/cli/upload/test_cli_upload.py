"""Test CG CLI upload module."""
import pytest

from datetime import datetime, timedelta

from click.testing import CliRunner

from cg.cli.upload.base import upload
from cg.models.cg_config import CGConfig
from cg.store.models import Case
from cg.store.store import Store
from tests.store_helpers import StoreHelpers


@pytest.mark.parametrize(
    "upload_context", ["balsamic", "microsalt", "mip", "mip-rna", "raredisease", "rnafusion", "taxprofiler", "tomte"], indirect=True
)
def test_upload_started_long_time_ago_raises_exception(
    cli_runner: CliRunner,
    upload_context: CGConfig,
    helpers: StoreHelpers,
):
    """Test that an upload for a missing case does fail hard."""

    # GIVEN an analysis that is already uploading since a week ago
    disk_store: Store = upload_context.status_db
    case = helpers.add_case(disk_store)
    case_id = case.internal_id
    today = datetime.now()
    upload_started = today - timedelta(hours=100)
    helpers.add_analysis(disk_store, case=case, upload_started=upload_started, uploading=True)

    # WHEN trying to upload an analysis that was started a long time ago
    result = cli_runner.invoke(upload, ["-f", case_id], obj=upload_context)

    # THEN an exception should have be thrown
    assert result.exit_code != 0
    assert result.exception

@pytest.mark.parametrize(
    "upload_context", ["balsamic", "microsalt", "mip", "mip-rna", "raredisease", "rnafusion", "taxprofiler", "tomte"], indirect=True
)
def test_upload_force_restart(cli_runner: CliRunner, upload_context: CGConfig, helpers: StoreHelpers):
    """Test that a case that is already uploading can be force restarted."""

    # GIVEN an analysis that is already uploading
    disk_store: Store = upload_context.status_db
    case: Case = helpers.add_case(disk_store)
    case_id: str = case.internal_id

    helpers.add_analysis(disk_store, case=case, uploading=True)

    # WHEN trying to upload it again with the force restart flag
    result = cli_runner.invoke(upload, ["-f", case_id, "-r"], obj=upload_context)

    # THEN it tries to restart the upload
    assert "already started" not in result.output
