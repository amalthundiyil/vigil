import logging
import click

import pandas as pd
from tabulate import tabulate
from rich.console import Console

from sauron.processor.base_backend import BackendTypes
from sauron.cli.checks_util import (
    get_from_config,
    get_validated_class,
    full_process,
    summarize,
)

DOMAINS = ["community", "popularity", "maintainence", "security"]
# DOMAINS = ["community", "popularity", "maintainence"]

LOG = logging.getLogger("sauron.cli.checks")


def run_check(ctx, url, name, type, token, comm, maint, sec, pop):
    if comm:
        community(ctx, url, name, type, token)
    if maint:
        maintainence(ctx, url, name, type, token)
    if sec:
        security(ctx, url, name, type, token)
    if pop:
        popularity(ctx, url, name, type, token)


def community(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🌏  Analyzing Community", fg="blue", bold=True)
    p = get_validated_class("community", url, name, type, token)
    df = full_process(p, True)
    s = summarize(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center", 
    )
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')


def maintainence(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🛠️  Analyzing Maintainence", fg="yellow", bold=True)
    p = get_validated_class("maintainence", url, name, type, token)
    df = full_process(p, True)
    s = summarize(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center", 
    )
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')



def security(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"🛡️  Analyzing security ", fg="blue", bold=True)
    p = get_validated_class("security", url, name, type, token)
    df = full_process(p, True)
    s = summarize(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center", 
    )
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')



def popularity(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"📈 Analyzing Popularity ", fg="white", bold=True)
    p = get_validated_class("popularity", url, name, type, token)
    df = full_process(p, True)
    s = summarize(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center", 
    )
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')


@click.command(
    context_settings=dict(ignore_unknown_options=True),
    help="Run security and health checks of Open source software",
)
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
@click.option(
    "--community",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run community checks",
)
@click.option(
    "--maintainence",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run maintainence checks",
)
@click.option(
    "--security",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run security checks",
)
@click.option(
    "--popularity",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run popularity checks",
)
@click.pass_context
def check(
    ctx,
    url,
    name,
    type,
    token,
    community,
    maintainence,
    security,
    popularity,
):
    if community or maintainence or security or popularity:
        run_check(
            ctx,
            url,
            name,
            type,
            token,
            community,
            maintainence,
            security,
            popularity,
        )
    else:
        token = get_from_config("github_token")
        click.secho(f"🧐  Running all checks", fg="blue", bold=True)
        for domain in DOMAINS:
            p = get_validated_class(domain, url, name, type, token)
            click.secho(f"Analyzing {domain}", fg="blue", bold=True)
            data = full_process(p, True)
            click.secho(
                f"✅️ Completed {domain} analysis for {p.name}", fg="green", bold=True
            )
