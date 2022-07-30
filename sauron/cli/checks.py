import logging
import sys
import click

import pandas as pd
from tabulate import tabulate
from rich.console import Console

from sauron.processor.base_backend import BackendTypes
from sauron.processor.base_processor import final_summary
from sauron.cli.checks_util import (
    get_from_config,
    get_validated_class,
    full_process,
    summarize,
    transform
)

DOMAINS = ["community", "popularity", "maintainence", "security"]
# DOMAINS = ["community", "popularity", "maintainence"]

LOG = logging.getLogger("sauron.cli.checks")
LOGO = """
███████╗ █████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ██╗
██╔════╝██╔══██╗██║   ██║██╔══██╗██╔═══██╗████╗  ██║
███████╗███████║██║   ██║██████╔╝██║   ██║██╔██╗ ██║
╚════██║██╔══██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║
███████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""
DOMAIN_TO_EMOJI = {
    "community" : '🌏', 
    "popularity" : '📈️', 
    "maintainence" : '🛠️', 
    "security" : '🛡️', 
}


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
    )
    click.secho(f'🚩 Aggregate score: {s["score"]}')
    click.secho(f'📜 Aggregate summary: {s["description"]}')


def security(ctx, url, name, type, token):
    token = get_from_config("github_token", token, silent=True)
    click.secho(f"🛡️  Analyzing security ", fg="yellow", bold=True)
    p = get_validated_class("security", url, name, type, token)
    df = full_process(p, True)
    s = summarize(p, True)
    click.secho(f"✅️  Completed analysis for {p.name}", fg="green", bold=True)
    console = Console()
    console.print(
        tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
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

@click.option(
    "--threshold",
    type=float,
    help="Minimum score required to pass",
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
        token = get_from_config("github_token", token, silent=True)
        click.secho(LOGO)
        click.secho(f"🧐 Running all checks", fg="white", bold=True)
        scores = []
        descs = []
        for domain in DOMAINS:
            click.secho(f"{DOMAIN_TO_EMOJI[domain]}  Analyzing {domain}", fg="blue", bold=True)
            p = get_validated_class(domain, url, name, type, token)
            df = full_process(p, True)
            s = summarize(p, True)
            click.secho(f"✔️  Completed {domain} analysis", fg="green", bold=True)
            scores.append(s["score"])
            descs.append(s["description"])

        df = transform({"metrics": DOMAINS, "score": scores, "description": descs})
        final_score, final_description = final_summary(scores)
        console = Console()
        console.print(
            tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False),
            justify="center", 
        )
        click.secho(f'🚩 Aggregate score: {final_score}')
        click.secho(f'📜 Aggregate summary: {final_description}')

        if threshold:
            if final_score >= threshold:
                click.secho("✅️  Passed all checks", fg="green", bold=True)
            else:
                click.secho(f"⚠️  Failed to meet minimum score of {threshold}", fg="red", bold=True)
                sys.exit(1)



