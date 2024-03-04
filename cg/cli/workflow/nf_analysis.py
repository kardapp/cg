"""CLI options for Nextflow and NF-Tower."""

import logging

import click
from pydantic.v1 import ValidationError

from cg.cli.workflow.commands import ARGUMENT_CASE_ID, OPTION_DRY
from cg.constants.constants import MetaApis
from cg.exc import CgError
from cg.meta.workflow.nf_analysis import NfAnalysisAPI
from cg.models.cg_config import CGConfig

LOG = logging.getLogger(__name__)

OPTION_WORKDIR = click.option(
    "--work-dir",
    type=click.Path(),
    help="Directory where intermediate result files are stored",
)
OPTION_RESUME = click.option(
    "--resume",
    is_flag=True,
    default=False,
    show_default=True,
    help="Execute the script using the cached results, useful to continue \
        executions that was stopped by an error",
)
OPTION_PROFILE = click.option(
    "--profile",
    type=str,
    show_default=True,
    help="Choose a configuration profile",
)

OPTION_LOG = click.option(
    "--log",
    type=click.Path(),
    help="Set nextflow log file path",
)

OPTION_CONFIG = click.option(
    "--config",
    type=click.Path(),
    help="Nextflow config file path",
)

OPTION_PARAMS_FILE = click.option(
    "--params-file",
    type=click.Path(),
    help="Nextflow workflow-specific parameter file path",
)

OPTION_USE_NEXTFLOW = click.option(
    "--use-nextflow",
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help="Execute workflow using nextflow",
)

OPTION_REVISION = click.option(
    "--revision",
    type=str,
    help="Revision of workflow to run (either a git branch, tag or commit SHA number)",
)
OPTION_COMPUTE_ENV = click.option(
    "--compute-env",
    type=str,
    help="Compute environment name. If not specified the primary compute environment will be used.",
)
OPTION_TOWER_RUN_ID = click.option(
    "--nf-tower-id",
    type=str,
    is_flag=False,
    default=None,
    help="NF-Tower ID of run to relaunch. If not provided the latest NF-Tower ID for a case will be used.",
)
OPTION_FROM_START = click.option(
    "--from-start",
    is_flag=True,
    default=False,
    show_default=True,
    help="Start workflow from start without resuming execution",
)


@click.command("metrics-deliver")
@ARGUMENT_CASE_ID
@OPTION_DRY
@click.pass_obj
def metrics_deliver(context: CGConfig, case_id: str, dry_run: bool) -> None:
    """Create and validate a metrics deliverables file for given case id.
    If QC metrics are met it sets the status in Trailblazer to complete.
    If failed, it sets it as failed and adds a comment with information of the failed metrics."""

    analysis_api: NfAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]

    try:
        analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
        analysis_api.write_metrics_deliverables(case_id=case_id, dry_run=dry_run)
        analysis_api.validate_qc_metrics(case_id=case_id, dry_run=dry_run)
    except CgError as error:
        raise click.Abort() from error


@click.command("report-deliver")
@ARGUMENT_CASE_ID
@OPTION_DRY
@click.pass_obj
def report_deliver(context: CGConfig, case_id: str, dry_run: bool) -> None:
    """Create a Housekeeper deliverables file for given case id."""

    analysis_api: NfAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]

    try:
        analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
        analysis_api.trailblazer_api.is_latest_analysis_completed(case_id=case_id)
        if not dry_run:
            analysis_api.report_deliver(case_id=case_id)
        else:
            LOG.info(f"Dry-run: Would have created delivery files for case {case_id}")
    except Exception as error:
        LOG.error(f"Could not create report file: {error}")
        raise click.Abort()
