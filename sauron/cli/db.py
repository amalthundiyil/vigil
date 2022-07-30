from distutils.command.config import config
import logging
import subprocess

import click

from datetime import datetime
import sys

DEFAULT_ES_URL = "http://localhost:9200"

LOG = logging.getLogger("sauron.cli.checks")


@click.group(help="Command to manage the database")
def db():
    pass


@db.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--repo-url", type=str, help="URL of repository to add to GitHub.")
@click.option("-t", "--token", type=str, help="API token to increase rate limit.")
@click.option(
    "--elastic-url",
    type=str,
    default=DEFAULT_ES_URL,
    help="URL where Elasticsearch is listening.",
)
@click.pass_context
def add_repo(ctx, repo_url, token, elastic_url):
    pass
