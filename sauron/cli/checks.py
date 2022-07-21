import logging
import click
import sys
from urllib.parse import urlparse

import pandas as pd
from tabulate import tabulate
from sauron.processor.community import CommunityProcessor

from sauron.processor.maintainence import MaintainenceProcessor
from sauron.processor.popularity import GithubPopularity
from sauron.processor.vulns import VulnsProcessor

LOG = logging.getLogger("sauron.cli.checks")

NPM_URL = "npmjs.com"
GITHUB_URL = "github.com"
PYPI_URL = "pypi.org"

@click.group(help="Groups commands for running checks.")
@click.pass_context
def check(ctx):
    pass

@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def community(ctx, url, token):
    c = CommunityProcessor(url, token)
    click.secho(f'️🌐️ Analyzing Community', fg="blue", bold=True)
    try:
        data = c.process()
    except Exception:
        click.secho(f'❗ Failed analyzing community for {url}', fg="red", bold=True)
        sys.exit(0)
    click.secho(f'✅️ Completed analysis for {c.repo_url}', fg="green", bold=True)
    df = pd.DataFrame(data, columns=["has_readme", "has_contributing", "has_code_of_conduct", "contributors"], index=[0])
    click.secho(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False), fg="magenta")


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def maintainence(ctx, url, token):
    m = MaintainenceProcessor(url, token)
    click.secho(f'️🛠️ Analyzing Maintainence', fg="blue", bold=True)
    try:
        data = m.process()
    except Exception:
        click.secho(f'❗ Failed analyzing maintainence for {url}', fg="red", bold=True)
        sys.exit(0)
    click.secho(f'✅️ Completed analysis for {m.repo_url}', fg="green", bold=True)
    df = pd.DataFrame(data, columns=["open_issues", "open_pr", "latest_commit", "latest_release"], index=[0])
    click.secho(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False), fg="magenta")


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def vulnerabilites(ctx, url):
    v = VulnsProcessor(url)
    click.secho(f'🛡️ Analyzing Vulnerabilites ', fg="blue", bold=True)
    r = v.process()
    if r.stderr:
        click.secho(f'❗ Failed analyzing vulnerabilties for {url}', fg="red", bold=True)
        sys.exit(0)
    click.secho(f'✅ Completed analysis for {v.repo_url}', fg="green", bold=True)
    click.echo(r.stdout)



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
        click.secho(f'❗ Failed analyzing popularity for {url}', fg="red", bold=True)
        sys.exit(0)
    data = p.process()
    try:
        data["downloads"] = data["downloads"][0]["count"]
    except KeyError:
        data ["downloads"] = 0
    click.secho(f'✅️ Completed analysis for {p.repo_url}', fg="green", bold=True)
    df = pd.DataFrame(data, columns=["stars", "downloads", "forks", "contributors", "dependents"], index=[0])
    click.secho(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))



@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def all(ctx, url):
    click.secho(f'🧐 Running all checks', fg="blue", bold=True)
