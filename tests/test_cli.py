from click.testing import CliRunner
from unittest.mock import patch
from geniescript.cli import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Main command group for geniescript CLI" in result.output


def test_run_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run a genie script" in result.output


@patch("geniescript.cli.run_impl")
def test_run_basic(mock_run):
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "test.genie"])

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        "test.genie", execute=True, script_args=[], force_regenerate=False
    )


@patch("geniescript.cli.run_impl")
def test_run_no_execute(mock_run):
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--no-execute", "test.genie"])

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        "test.genie", execute=False, script_args=[], force_regenerate=False
    )


@patch("geniescript.cli.run_impl")
def test_run_with_script_args(mock_run):
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--script-args", "arg1 arg2", "test.genie"])

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        "test.genie", execute=True, script_args=["arg1", "arg2"], force_regenerate=False
    )


@patch("geniescript.cli.run_impl")
def test_run_force_regenerate(mock_run):
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--force-regenerate", "test.genie"])

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        "test.genie", execute=True, script_args=[], force_regenerate=True
    )


def test_run_unknown_args():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "test.genie", "--unknown"])

    assert result.exit_code != 0
    assert "Unknown arguments" in result.output
