import logging
import click
import sys

import pandas as pd
from tabulate import tabulate
from rich.console import Console

from sauron.processor import BackendTypes
from sauron.cli.checks_util import (
    transform,
    get_from_config,
    get_validated_class,
    process,
)

LOG = logging.getLogger("sauron.cli.checks")


@click.group(help="Command to run any or all of the checks and scans.")
@click.pass_context
def check(ctx):
    pass


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def community(ctx, url, token):
    c = CommunityProcessor(url, token)
    click.secho(f"️🌏  Analyzing Community", fg="blue", bold=True)
    try:
        data = c.process()
    except Exception:
        click.secho(f"❗  Failed analyzing community for {url}", fg="red", bold=True)
        sys.exit(0)
    click.secho(f"✅️  Completed analysis for {c.repo_url}", fg="green", bold=True)
    df = pd.DataFrame(
        data,
        columns=[
            "has_readme",
            "has_contributing",
            "has_code_of_conduct",
            "contributors",
        ],
        index=[0],
    )
    click.secho(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        fg="magenta",
    )


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def maintainence(ctx, url, token):
    m = MaintainenceProcessor(url, token)
    click.secho(f"️🛠️ Analyzing Maintainence", fg="blue", bold=True)
    try:
        data = m.process()
    except Exception:
        click.secho(f"❗ Failed analyzing maintainence for {url}", fg="red", bold=True)
        sys.exit(0)
    click.secho(f"✅️ Completed analysis for {m.repo_url}", fg="green", bold=True)
    df = pd.DataFrame(
        data,
        columns=["open_issues", "open_pr", "latest_commit", "latest_release"],
        index=[0],
    )
    click.secho(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        fg="magenta",
    )


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the repository to analyze")
@click.pass_context
def vulnerabilites(ctx, url):
    v = VulnsProcessor(url)
    click.secho(f"🛡️  Analyzing Vulnerabilites ", fg="blue", bold=True)
    data = v.process()
    if not data:
        click.secho(f"❗ Failed analyzing vulnerabilties for {url}", fg="red", bold=True)
        sys.exit(0)
    click.secho(f"✅ Completed analysis for {v.repo_url}", fg="green", bold=True)
    df = pd.DataFrame(data, columns=list(data.keys()), index=[0])
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center",
    )


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the package to analyze")
@click.option(
    "-n",
    "--name",
    type=str,
    help="Name of package to analyze. For GitHub enter <organization>/<repository>",
)
@click.option(
    "--type",
    type=click.Choice([x.value for x in BackendTypes]),
    help="Type of package to analyze",
)
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def popularity(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"📈 Analyzing Popularity ", fg="blue", bold=True)
    p = get_validated_class("popularity", url, name, type, token)
    data = process(p, True)
    click.secho(f"✅️ Completed analysis for {p.name}", fg="green", bold=True)
    df = pd.DataFrame(data, columns=list(data.keys()), index=[0])
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center",
    )


@check.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-u", "--url", type=str, help="URL of the package to analyze")
@click.option(
    "-n",
    "--name",
    type=str,
    help="Name of package to analyze. For GitHub enter <organization>/<repository>",
)
@click.option(
    "--type",
    type=click.Choice([x.value for x in BackendTypes]),
    help="Type of package to analyze",
)
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.pass_context
def all(ctx, url, name, type, token):
    token = get_from_config("github_token")
    click.secho(f"🧐  Running all checks", fg="blue", bold=True)
    Processors = [
        CommunityProcessor,
        PopularityProcessor,
        MaintainenceProcessor,
        VulnsProcessor,
    ]
    if name and type:
        obj = name
        p = PopularityProcessor.from_name(name, type, token)
    elif url:
        obj = url
        p = PopularityProcessor.from_url(url, token)
    else:
        click.secho(f"❗ Missing fields", fg="red", bold=True)
        sys.exit(0)
    try:
        data = p.process()
        data = p.get_download_count(data)
        data = transform(data)
    except Exception as e:
        LOG.error(e)
        click.secho(f"❗ Failed analyzing popularity for {obj}", fg="red", bold=True)
        sys.exit(0)
    click.secho(f"✅️ Completed analysis for {p.name}", fg="green", bold=True)
    df = pd.DataFrame(data, columns=list(data.keys()), index=[0])
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center",
    )
