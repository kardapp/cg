""" Test the CLI for mip-dna link"""
from cg.cli.workflow.mip_dna.base import link


def test_cg_workflow_mip_dna_link(cli_runner, case_id, dna_mip_context):
    """Test print the MIP dna link command to console"""

    # GIVEN a cli function

    # WHEN we run a case in dry run mode
    result = cli_runner.invoke(link, [case_id], obj=dna_mip_context)

    # THEN the command should be printed
    assert result.exit_code == 0
