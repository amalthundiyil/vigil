import logging
import os

import click
from vigil import ROOT_VIGIL_DIRECTORY

from vigil.cli.cli_util import print_version, call_and_exit_flag
from vigil.cli.checks import check
from vigil.cli.db import db


@click.group()
@call_and_exit_flag(
    "--version",
    callback=print_version,
    help="Show version information and exit.",
)
@click.pass_context
def cli(ctx):
    fmt = "%(asctime)s T%(thread)d %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
    # fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    # logging.basicConfig(filename=os.path.join(ROOT_VIGIL_DIRECTORY, "logs", "cli.log"), filemode='a', format=fmt, force=True)

cli.add_command(check)
cli.add_command(db)

if __name__ == '__main__':
    cli()  