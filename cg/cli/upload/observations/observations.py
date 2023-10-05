"""Code for uploading observations data via CLI."""

import contextlib
import logging
from datetime import datetime
from typing import Optional, Union

import click
from pydantic.v1 import ValidationError
from sqlalchemy.orm import Query

from cg.cli.upload.observations.utils import get_observations_api, get_observations_case_to_upload
from cg.cli.workflow.commands import (
    ARGUMENT_CASE_ID,
    OPTION_DRY,
    OPTION_LOQUSDB_SUPPORTED_PIPELINES,
)
from cg.constants.constants import Pipeline
from cg.exc import CaseNotFoundError, LoqusdbError
from cg.meta.observations.balsamic_observations_api import BalsamicObservationsAPI
from cg.meta.observations.mip_dna_observations_api import MipDNAObservationsAPI
from cg.models.cg_config import CGConfig
from cg.store import Store
from cg.store.models import Family

LOG = logging.getLogger(__name__)


@click.command("observations")
@ARGUMENT_CASE_ID
@OPTION_DRY
@click.pass_obj
def upload_observations_to_loqusdb(context: CGConfig, case_id: Optional[str], dry_run: bool):
    """Upload observations from an analysis to Loqusdb."""

    click.echo(click.style("----------------- OBSERVATIONS -----------------"))

    with contextlib.suppress(LoqusdbError):
        case: Family = get_observations_case_to_upload(context, case_id)
        observations_api: Union[
            MipDNAObservationsAPI, BalsamicObservationsAPI
        ] = get_observations_api(context, case)

        if dry_run:
            LOG.info(f"Dry run. Would upload observations for {case.internal_id}.")
            return

        observations_api.upload(case)


@click.command("available-observations")
@OPTION_LOQUSDB_SUPPORTED_PIPELINES
@OPTION_DRY
@click.pass_context
def upload_available_observations_to_loqusdb(
    context: click.Context, pipeline: Optional[Pipeline], dry_run: bool
):
    """Uploads the available observations to Loqusdb."""

    click.echo(click.style("----------------- AVAILABLE OBSERVATIONS -----------------"))

    status_db: Store = context.obj.status_db
    cases_to_upload: Query = status_db.observations_to_upload(pipeline=pipeline)
    if not cases_to_upload:
        LOG.error(
            f"There are no available cases to upload to Loqusdb for {pipeline} ({datetime.now()})"
        )
        return

    for case in cases_to_upload:
        try:
            LOG.info(f"Will upload observations for {case.internal_id}")
            context.invoke(
                upload_observations_to_loqusdb, case_id=case.internal_id, dry_run=dry_run
            )
        except (CaseNotFoundError, FileNotFoundError, ValidationError) as error:
            LOG.error(f"Error uploading observations for {case.internal_id}: {error}")
            continue
