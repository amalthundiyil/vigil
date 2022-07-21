import logging
import click
import sys
from urllib.parse import urlparse

import pandas as pd
from tabulate import tabulate

from sauron.backend.server.commands import vulns
from sauron.processor.popularity import GithubPopularity

LOG = logging.getLogger("sauron.cli.checks")

NPM_URL = "npmjs.com"
GITHUB_URL = "github.com"
PYPI_URL = "pypi.org"

@click.group()
@click.pass_context
def check(ctx):
    pass


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def vulns(ctx, url, token):
    netloc = urlparse(url).netloc
    click.secho(f'🛡️ Analyzing Vulnerabilites ', fg="blue", bold=True)
    if netloc == NPM_URL:
        pass
    elif netloc == GITHUB_URL:
        p = GithubPopularity(url, token)
    elif netloc == PYPI_URL:
        pass
    else:
        click.secho(f'Failed analyzing vulnerability for {url}', fg="red", bold=True)
        sys.exit(0)
    data = p.summarize()
    try:
        data["downloads"] = data["downloads"][0]["count"]
    except KeyError:
        data ["downloads"] = 0
    click.secho(f'Completed analysis for {p.repo_url}', fg="green", bold=True)
    df = pd.DataFrame(data, columns=["stars", "downloads", "forks", "contributors", "dependents"], index=[0])
    click.secho(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def popularity(ctx, url, token):
    netloc = urlparse(url).netloc
    click.secho(f'📈 Analyzing Popularity ', fg="blue", bold=True)
    if netloc == NPM_URL:
        pass
    elif netloc == GITHUB_URL:
        p = GithubPopularity(url, token)
    elif netloc == PYPI_URL:
        pass
    else:
        click.secho(f'Failed analyzing popularity for {url}', fg="red", bold=True)
        sys.exit(0)
    data = p.summarize()
    try:
        data["downloads"] = data["downloads"][0]["count"]
    except KeyError:
        data ["downloads"] = 0
    click.secho(f'Completed analysis for {p.repo_url}', fg="green", bold=True)
    df = pd.DataFrame(data, columns=["stars", "downloads", "forks", "contributors", "dependents"], index=[0])
    click.secho(tabulate(df, headers="keys", tablefmt="psql", showindex=False))



@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def all(ctx, url):
    # r = vulns.process_vulns(url)
    click.echo("asdf")
