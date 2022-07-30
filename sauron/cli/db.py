import logging
import subprocess
import sys
from datetime import datetime

import click
from elasticsearch import Elasticsearch


DEFAULT_ES_URL = "http://localhost:9200"

LOG = logging.getLogger("sauron.cli.db")

def get_es_client():
    es = Elasticsearch()


@click.group(help="Manage the Elasticsearch database")
def db():
    pass


@db.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--repo-url", type=str, help="URL of repository or package.")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.option(
    "--elastic-url",
    type=str,
    default=DEFAULT_ES_URL,
    help="URL of Elasticsearch.",
)
@click.pass_context
def add_repo(ctx, repo_url, token, elastic_url):
    pass
