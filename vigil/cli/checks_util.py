import logging
import sys
import string

import click
import pandas as pd

from base.processor import BaseProcessor, ValidationError
import config

LOG = logging.getLogger("vigil.cli.checks")


def get_from_config(key, value, silent=False):
    if not silent:
        return value if value else config.get_from_config(key)
    try:
        return value if value else config.get_from_config(key)
    except Exception as e:
        LOG.error(e)
        click.secho(f"❗ Couldn't get {key} from config", fg="red", bold=True)
        sys.exit(0)


def get_validated_class(domain, url=None, name=None, type=None, token=None):
    try:
        return BaseProcessor.get_processor_class(domain, url, name, type, token)
    except ValidationError as e:
        click.secho(f"❗ Missing fields: {e.message}", fg="red", bold=True)
        sys.exit(0)
    except Exception as e:
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(0)


def summarize(p, silent, elastic):
    if elastic:
        es_data = get_es_data(p)
        if es_data:
            return es_data[p.domain]["summary"]
    if not silent:
        data = p.summarize()
        return data
    try:
        data = p.summarize()
        return data
    except Exception as e:
        LOG.error(e)
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(0)


def full_process(p, silent, elastic):
    if elastic:
        es_data = get_es_data(p)
        if es_data:
            df = transform(es_data[p.domain]["score_data"])
            return df
    if not silent:
        data = p.process()
        df = transform(data)
        return df
    try:
        data = p.process()
        df = transform(data)
        return df
    except Exception as e:
        LOG.error(e)
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(0)


def add_data(elastic_url, url, name, type, token):
    from db_utils import connect_es, add_data, get_db_data
    from backend.server.commands.dashboard import (
        full_process,
        summary,
        get_package_info,
    )
    from checks import DOMAINS

    es = connect_es(elastic_url)
    if not es:
        return

    data = {}
    es_data = get_db_data(url, name, type, es)
    if es_data:
        return es_data

    for domain in DOMAINS:
        p = get_validated_class(domain, url, name, type, token)
        d = full_process(p)
        data[domain] = d
    data["final_score"], data["final_desc"] = summary(data)
    pkg_info = get_package_info(p)
    data["name"], data["type"], data["description"], data["url"] = (
        pkg_info["name"],
        pkg_info["type"],
        pkg_info["desc"],
        pkg_info["url"],
    )
    data = add_data(es, data)
    return data


def get_es_data(p):
    from db_utils import connect_es, get_db_data

    es = connect_es()
    if not es:
        return
    es_data = get_db_data(p.url, p.name, p.type, es)
    if not es_data:
        return
    return es_data


def transform(l):
    l["metrics"] = transform_list(l["metrics"])
    df = pd.DataFrame(l)
    df.rename(
        columns={"metrics": "Metrics", "score": "Score", "description": "Description"},
        inplace=True,
    )
    return df


def transform_list(l):
    new_l = []
    for e in l:
        new_key = string.capwords(e, "_")
        new_key = " ".join(new_key.split("_"))
        new_l.append(new_key)
    return new_l
