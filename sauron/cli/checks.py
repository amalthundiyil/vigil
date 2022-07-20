import logging

import click

from sauron.backend.server.commands import vulns

LOG = logging.getLogger("sauron.cli.checks")


@click.group()
@click.pass_context
def check(ctx):
    pass


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def all(ctx, url):
    # r = vulns.process_vulns(url)
    click.echo("asdf")
