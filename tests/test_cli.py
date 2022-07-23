from click.testing import CliRunner
from sauron.cli.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


