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
)

# DOMAINS = ["community", "popularity", "maintainence", "vulnerabilites"]
DOMAINS = ["community", "popularity", "maintainence"]

LOG = logging.getLogger("sauron.cli.checks")


def run_check(ctx, url, name, type, token, comm, maint, vulns, pop):
    if comm:
        community(ctx, url, name, type, token)
    if maint:
        maintainence(ctx, url, name, type, token)
    if vulns:
        vulnerabilites(ctx, url, token)
    if pop:
        popularity(ctx, url, name, type, token)


def community(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🌏  Analyzing Community", fg="blue", bold=True)
    p = get_validated_class("community", url, name, type, token)
    df = full_process(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid"),
        justify="center",
    )


def maintainence(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🛠️  Analyzing Maintainence", fg="yellow", bold=True)
    p = get_validated_class("maintainence", url, name, type, token)
    df = full_process(p, True)
    click.secho(f"✅️ Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid"),
        justify="center",
    )


def vulnerabilites(ctx, url, token):
    click.secho(f"🛡️  Analyzing Vulnerabilites ", fg="blue", bold=True)
    p = get_validated_class("vulnerabilities", url)
    data = full_process(p, True)
    click.secho(f"✅️ Completed analysis for {p.name}", fg="green", bold=True)
    df = pd.DataFrame(data, columns=list(data[0].keys()))
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center",
    )


def popularity(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"📈 Analyzing Popularity ", fg="blue", bold=True)
    p = get_validated_class("popularity", url, name, type, token)
    data = full_process(p, True)
    click.secho(f"✅️ Completed analysis for {p.name}", fg="green", bold=True)
    df = pd.DataFrame(data, columns=list(data.keys()), index=[0])
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        justify="center",
    )


@click.command(
    context_settings=dict(ignore_unknown_options=True),
    help="Run different all (default) or specified checks",
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
    "--vulnerabilites",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run vulnerabilites checks",
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
    vulnerabilites,
    popularity,
):
    if community or maintainence or vulnerabilites or popularity:
        run_check(
            ctx,
            url,
            name,
            type,
            token,
            community,
            maintainence,
            vulnerabilites,
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
