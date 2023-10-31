import imp
import logging
import sys
import click

import pandas as pd
from tabulate import tabulate
from rich.console import Console

from base.backend import BackendTypes
from base.processor import final_summary
from checks_util import (
    get_from_config,
    get_validated_class,
    full_process,
    summarize,
    transform,
)

DOMAINS = ["community", "popularity", "maintainence", "security"]
# DOMAINS = ["community", "popularity", "maintainence"]

LOG = logging.getLogger("vigil.cli.checks")
LOGO = """
██╗   ██╗██╗ ██████╗ ██╗██╗     
██║   ██║██║██╔════╝ ██║██║     
██║   ██║██║██║  ███╗██║██║     
╚██╗ ██╔╝██║██║   ██║██║██║     
 ╚████╔╝ ██║╚██████╔╝██║███████╗
  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝
"""
DOMAIN_TO_EMOJI = {
    "community": "🌏",
    "popularity": "📈️",
    "maintainence": "🛠️",
    "security": "🛡️",
}


def run_check(ctx, url, name, type, token, comm, maint, sec, pop, elastic):
    if comm:
        return community(ctx, url, name, type, token, elastic)
    if maint:
        return maintainence(ctx, url, name, type, token, elastic)
    if sec:
        return security(ctx, url, name, type, token, elastic)
    if pop:
        return popularity(ctx, url, name, type, token, elastic)
    return -1


def community(ctx, url, name, type, token, elastic):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🌏  Analyzing Community", fg="blue", bold=True)
    p = get_validated_class("community", url, name, type, token)
    df = full_process(p, True, elastic)
    s = summarize(p, True, elastic)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print("\n")
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
    )
    console.print("\n")
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')
    return s["score"]


def maintainence(ctx, url, name, type, token, elastic):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"️🛠️  Analyzing Maintainence", fg="yellow", bold=True)
    p = get_validated_class("maintainence", url, name, type, token)
    df = full_process(p, True, elastic)
    s = summarize(p, True, elastic)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print("\n")
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
    )
    console.print("\n")
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')
    return s["score"]


def security(ctx, url, name, type, token, elastic):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"🛡️  Analyzing security ", fg="yellow", bold=True)
    p = get_validated_class("security", url, name, type, token)
    df = full_process(p, True, elastic)
    s = summarize(p, True, elastic)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print("\n")
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
    )
    console.print("\n")
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')
    return s["score"]


def popularity(ctx, url, name, type, token, elastic):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"📈 Analyzing Popularity ", fg="white", bold=True)
    p = get_validated_class("popularity", url, name, type, token)
    df = full_process(p, True, elastic)
    s = summarize(p, True, elastic)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print("\n")
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
    )
    console.print("\n")
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')
    return s["score"]


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
@click.option(
    "--threshold",
    type=float,
    help="Minimum score required to pass",
)
@click.option(
    "--elastic",
    is_flag=True,
    default=False,
    show_default=True,
    help="Use Vigil CLI with Elasticsearch.",
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
    threshold,
    elastic,
):
    if threshold and threshold < 0:
        click.secho(
            f"⚠️  Threshold must be greater than 0. Currently set to {threshold}",
            fg="red",
            bold=True,
        )
        sys.exit(1)

    if elastic:
        from checks_util import add_data

        token = get_from_config("github_token", token, silent=True)
        res = add_data("", url, name, type, token)

    if community or maintainence or security or popularity:
        final_score = run_check(
            ctx,
            url,
            name,
            type,
            token,
            community,
            maintainence,
            security,
            popularity,
            elastic,
        )
    else:
        token = get_from_config("github_token", token, silent=True)
        click.secho(LOGO)
        click.secho(f"🧐 Running all checks", fg="white", bold=True)
        scores = []
        descs = []
        for domain in DOMAINS:
            click.secho(f"{DOMAIN_TO_EMOJI[domain]}  Analyzing {domain}", fg="blue", bold=True)
            p = get_validated_class(domain, url, name, type, token)
            df = full_process(p, True, elastic)
            s = summarize(p, True, elastic)
            click.secho(f"✔️  Completed {domain} analysis", fg="green", bold=True)
            scores.append(s["score"])
            descs.append(s["description"])

        df = transform({"metrics": DOMAINS, "score": scores, "description": descs})
        final_score, final_description = final_summary(scores)
        console = Console()
        console.print("\n")
        console.print(
            tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
        )
        console.print("\n")
        click.secho(f"🚩 Aggregate score: {final_score}")
        click.secho(f"📜 Aggregate summary: {final_description}")

    if threshold:
        if final_score >= threshold:
            click.secho("✅️  Passed all checks", fg="green", bold=True)
        else:
            click.secho(f"⚠️  Failed to meet minimum score of {threshold}", fg="red", bold=True)
            sys.exit(1)
