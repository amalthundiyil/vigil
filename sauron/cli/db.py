from distutils.command.config import config
import logging
import subprocess

import click

from datetime import datetime
import sys

from grimoire_elk.elk import feed_backend, enrich_backend
from grimoire_elk.elastic import ElasticSearch
from grimoire_elk.elastic_items import ElasticItems
from grimoire_elk.utils import get_params, config_logging
from sauron.processor.p2o import P20_SCRIPT_PATH

DEFAULT_ES_URL = "http://localhost:9200"

LOG = logging.getLogger("sauron.cli.checks")


@click.group()
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
    subprocess.run(
        [
            "python",
            P20_SCRIPT_PATH,
            "--enrich",
            "--index",
            "git_raw",
            "--index-enrich",
            "git",
            "-e",
            elastic_url,
            "--no_inc",
            "--debug",
            "git",
            repo_url,
        ]
    )
    # Produce github and github_raw indexes from GitHub issues and prs
    subprocess.run(['python',P20_SCRIPT_PATH,  '--enrich', '--index', 'github_raw',
      '--index-enrich', 'github', '-e', elastic_url,
      '--no_inc', '--debug', 'github', 'grimoirelab', "perceval",
      '-t', token, '--sleep-for-rate'])