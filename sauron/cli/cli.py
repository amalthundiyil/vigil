import logging

import click

from sauron.backend.server.commands import vulns
from sauron.cli.cli_util import print_version, call_and_exit_flag
from sauron.cli.checks import check
from sauron.cli.db import db


@click.group()
@call_and_exit_flag(
    "--version",
    callback=print_version,
    help="Show version information and exit.",
)
@click.option("-v", "--verbose", count=True, help="Repeat for more verbosity")
@click.pass_context
def cli(ctx, verbose):
    ctx.obj =  click.Context(ctx, ctx)
    # default == WARNING; -v == INFO; -vv == DEBUG
    ctx.obj.verbosity = verbose
    log_level = logging.WARNING - min(10 * verbose, 20)
    if verbose >= 2:
        fmt = "%(asctime)s T%(thread)d %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
    else:
        fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    logging.basicConfig(level=log_level, format=fmt)

    if verbose >= 3:
        # enable SQLAlchemy query logging
        logging.getLogger("sqlalchemy.engine").setLevel("INFO")


cli.add_command(check)
cli.add_command(db)
