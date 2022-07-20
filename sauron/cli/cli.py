import click

from sauron.backend.server.commands import vulns
from sauron.cli.cli_util import print_version, call_and_exit_flag


@click.group()
@call_and_exit_flag(
    "--version",
    callback=print_version,
    help="Show version information and exit.",
)
@click.option("-v", "--verbose", count=True, help="Repeat for more verbosity")
@click.pass_context
def cli(ctx, verbose):
    pass


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def analyze(ctx, url):
    r = vulns.process_vulns(url)
    click.echo(r)
