import logging
import subprocess
import sys
from datetime import datetime

import click
from elasticsearch import Elasticsearch
from rich import print_json
from rich.console import Console

from sauron.cli.db_utils import add_data, get_data, drop_data, connect_es
from sauron.processor.base_backend import BackendTypes
from sauron.backend.server.commands.dashboard import (
    get_package_info,
    summary,
    full_process,
)
from sauron.cli.checks_util import (
    get_from_config,
    get_validated_class,
)
from sauron.cli.checks import DOMAINS, DOMAIN_TO_EMOJI


DEFAULT_ES_URL = "http://localhost:9200"

LOG = logging.getLogger("sauron.cli.db")


def get_es_client():
    es = Elasticsearch()


@click.group(help="Manage the Elasticsearch database")
def db():
    pass


@db.command(context_settings=dict(ignore_unknown_options=True))
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
    "--elastic-url",
    type=str,
    default=DEFAULT_ES_URL,
    help="URL of Elasticsearch.",
)
@click.pass_context
def add_repo(ctx, url, name, type, token, elastic_url):
    token = get_from_config("github_token", token, silent=True)
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if not es.ping():
        click.secho("❗ Could not connect to elastic search!", fg="red", bold=True)
        sys.exit(1)

    data = {}
    for domain in DOMAINS:
        click.secho(
            f"{DOMAIN_TO_EMOJI[domain]}  Ingesting {domain} data", fg="blue", bold=True
        )
        p = get_validated_class(domain, url, name, type, token)
        d = full_process(p)
        data[domain] = d
        LOG.info(data[domain])
        click.secho(f"✔️  Completed ingesting {domain} data", fg="green", bold=True)
    data["final_score"], data["final_desc"] = summary(data)
    pkg_info = get_package_info(p)
    data["name"], data["type"], data["description"], data["url"] = (
        pkg_info["name"],
        pkg_info["type"],
        pkg_info["desc"],
        pkg_info["url"],
    )
    click.secho(f"➕ Adding repository data to Elasticsearch", bold=True)
    try:
        add_data(es, data)
    except Exception as e:
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(1)

    click.secho(f"✅️  Completed adding data of {p.name}", fg="green", bold=True)


@db.command(context_settings=dict(ignore_unknown_options=True))
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
@click.option(
    "--elastic-url",
    type=str,
    default=DEFAULT_ES_URL,
    help="URL of Elasticsearch.",
)
@click.pass_context
def get_repo(ctx, url, name, type, elastic_url):
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if not es.ping():
        click.secho("❗ Could not connect to elastic search!", fg="red", bold=True)
        sys.exit(1)

    click.secho(f"🎯 Getting repository data from Elasticsearch", bold=True)
    p = get_validated_class("popularity", url, name, type)
    try:
        d = get_data(url, name, type, es)
    except Exception as e:
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(1)

    console = Console()
    console.print_json(data=d)
    click.secho(f"\n✅️ Completed getting data of {p.name}", fg="green", bold=True)


@db.command(
    context_settings=dict(ignore_unknown_options=True),
    help="Delete the entire index from Elasticsearch",
)
@click.option(
    "--elastic-url",
    type=str,
    default=DEFAULT_ES_URL,
    help="URL of Elasticsearch.",
)
@click.pass_context
def drop(ctx, elastic_url):
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    if not es.ping():
        click.secho("❗ Could not connect to elastic search!", fg="red", bold=True)
        sys.exit(1)

    click.secho(f"🗑️  Deleting repository data from Elasticsearch", bold=True)
    try:
        r = drop_data(es)
    except Exception as e:
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(1)

    click.secho(f"✅️  Completed dropping data", fg="green", bold=True)
