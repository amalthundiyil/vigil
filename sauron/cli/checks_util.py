import logging
import sys
import string

import click
import pandas as pd

from sauron.processor.base_processor import BaseProcessor, ValidationError
from sauron import config

LOG = logging.getLogger("sauron.cli.checks")


def get_from_config(key, value, silent):
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


def full_process(p, silent):
    if not silent:
        data = p.process()
        df = transform(data)
        return df
    # try:
    data = p.process()
    df = transform(data)
    return df
    # except Exception as e:
    #     LOG.error(e)
    #     click.secho(f"❗ Failed: {e}", fg="red", bold=True)
    #     sys.exit(0)


def transform(l):
    frames = []
    for d in l:
        nd = transform_dict(d)
        frames.append(pd.DataFrame.from_dict(nd, orient='index'))
    df = pd.concat(frames)
    df.rename_axis("Metrics", inplace=True)
    df.rename(columns={"score": "Score", "description": "Description"}, inplace=True)
    return df


def transform_dict(d):
    new_d = {}
    for old_key, v in d.items():
        new_key = string.capwords(old_key, "_")
        new_key = " ".join(new_key.split("_"))
        new_d[new_key] = v
    return new_d


