from distutils.command.config import config
import logging

import click

from sauron.backend.server.commands import vulns
from datetime import datetime
import sys

from grimoire_elk.elk import feed_backend, enrich_backend
from grimoire_elk.elastic import ElasticSearch
from grimoire_elk.elastic_items import ElasticItems
from grimoire_elk.utils import get_params, config_logging


LOG = logging.getLogger("sauron.cli.checks")


@click.group()
def db():
    pass


@db.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--es-url", type=str, help="Add repository to Elasticsearch.")
@click.option("--no-incremental", type=str, help="Add repository to Elasticsearch.")
@click.option("--fetch-cache", type=str)
@click.option("--backend", type=str)
@click.option("--bulk-size", type=str)
@click.option("--scroll-size", type=str)
@click.option("--scroll-wait", type=str)
@click.option("--enrich-only", type=str)
@click.option("--index", type=str)
@click.option("--index-enrich", type=str)
@click.option("--project", type=str)
@click.option("--url", type=str)
@click.option("--clean", type=str)
@click.option("--db-projects-map", type=str)
@click.option("--json-projects-map", type=str)
@click.option("--db-sorting-hat", type=str)
@click.option("--only-identities", type=str)
@click.option("--github-token", type=str)
@click.option("--studies", type=str)
@click.option("--studies-list", type=str)
@click.option("--only-studies", type=str)
@click.option("--elastic-url-search", type=str)
@click.option("--events-enrich", type=str)
@click.option("--db-user", type=str)
@click.option("--db-password", type=str)
@click.option("--db-host", type=str)
@click.option("--refresh-projects", type=str)
@click.option("--refresh-identites", type=str)
@click.option("--author-id", type=str)
@click.option("--author-uuid", type=str)
@click.option("--filter-raw", type=str)
@click.option("--jenkins-rename-file", type=str)
@click.option("--unaffiliated-group", type=str)
@click.option("--pair-programming", type=str)
@click.option("--enrich", type=str)
@click.pass_context
def add_repo(
    ctx,
    debug,
    elastic_url,
    no_incremental,
    fetch_cache,
    backend,
    bulk_size,
    scroll_size,
    scroll_wait,
    enrich_only,
    index,
    index_enrich,
    project,
    url,
    clean,
    db_projects_map,
    json_projects_map,
    db_sortinghat,
    only_identities,
    github_token,
    studies,
    studies_list,
    only_studies,
    elastic_url_enrich,
    events_enrich,
    db_user,
    db_password,
    db_host,
    refresh_projects,
    refresh_identities,
    author_id,
    author_uuid,
    filter_raw,
    jenkins_rename_file,
    unaffiliated_group,
    pair_programming,
    enrich,
):
    app_init = datetime.now()
    config_logging(debug)

    url = elastic_url

    clean = no_incremental
    if fetch_cache:
        clean = True

    try:
        if backend:
            # Configure elastic bulk size and scrolling
            if bulk_size:
                ElasticSearch.max_items_bulk = bulk_size
            if scroll_size:
                ElasticItems.scroll_size = scroll_size
            if scroll_wait:
                ElasticItems.scroll_wait = scroll_wait
            if not enrich_only:
                feed_backend(
                    url,
                    clean,
                    fetch_cache,
                    backend,
                    backend,
                    index,
                    index_enrich,
                    project,
                )
                LOG.info("Backend feed completed")

            studies_args = None
            if studies_list:
                # Convert the list to the expected format in enrich_backend method
                studies_args = []

                for study in studies_list:
                    studies_args.append({"name": study, "type": study, "params": {}})

            if enrich or enrich_only:
                unaffiliated_group = None
                enrich_backend(
                    url,
                    clean,
                    backend,
                    backend,
                    None,
                    index,
                    index_enrich,
                    db_projects_map,
                    json_projects_map,
                    db_sortinghat,
                    no_incremental,
                    only_identities,
                    github_token,
                    studies,
                    only_studies,
                    elastic_url_enrich,
                    events_enrich,
                    db_user,
                    db_password,
                    db_host,
                    refresh_projects,
                    refresh_identities,
                    author_id,
                    author_uuid,
                    filter_raw,
                    jenkins_rename_file,
                    unaffiliated_group,
                    pair_programming,
                    studies_args,
                )
                LOG.info("Enrich backend completed")
            elif events_enrich:
                LOG.info("Enrich option is needed for events_enrich")
        else:
            LOG.error("You must configure a backend")
    except KeyboardInterrupt:
        LOG.info("\n\nReceived Ctrl-C or other break signal. Exiting.\n")
        sys.exit(0)
    total_time_min = (datetime.now() - app_init).total_seconds() / 60
    LOG.info("Finished in %.2f min" % (total_time_min))
