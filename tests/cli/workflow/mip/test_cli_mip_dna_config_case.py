""" Test the CLI for mip-dna config-case"""
import logging

from cg.cli.workflow.mip_dna.base import config_case


def test_cg_workflow_mip_dna_config_case_dry_run(cli_runner, caplog, case_id, mip_context):
    """Test print the MIP dna case config command to console"""

    caplog.set_level(logging.INFO)

    # GIVEN a cli function

    # WHEN we run a case in dry run mode
    result = cli_runner.invoke(config_case, ["--dry-run", case_id], obj=mip_context)

    # THEN the command should be printed
    assert result.exit_code == 0
    assert f"config-case --dry {case_id}"


def test_cg_workflow_mip_dna_config_case(cli_runner, caplog, case_id, mip_context):
    """Test print the MIP dna case config command to file"""

    caplog.set_level(logging.INFO)

    # GIVEN a cli function

    # WHEN we run a case in dry run mode
    result = cli_runner.invoke(config_case, [case_id], obj=mip_context)

    # THEN the command should be printed
    assert result.exit_code == 0
    assert f"config-case --dry {case_id}"
