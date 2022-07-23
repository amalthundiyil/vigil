import logging
import click
import sys
import string

from sauron.processor.base import BaseProcessor, ValidationError
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


def get_validated_class(domain, url, name, type, token):
    try:
        return BaseProcessor.get_processor_class(domain, url, name, type, token)
    except ValidationError as e:
        click.secho(f"❗ Missing fields: {e.message}", fg="red", bold=True)
        sys.exit(0)
    except Exception as e:
        click.secho(f"❗ Failed: {e}", fg="red", bold=True)
        sys.exit(0)


def process(p, silent):
    if not silent:
        data = p.process()
        data = p.get_download_count(data)
        data = transform(data)
        return data
    try:
        data = p.process()
        data = p.get_download_count(data)
        data = transform(data)
        return data
    except Exception as e:
        LOG.error(e)
        click.secho(f"❗ Failed analyzing popularity", fg="red", bold=True)
        sys.exit(0)


def transform(d):
    new_d = {}
    for old_key, v in d.items():
        new_key = string.capwords(old_key, "_")
        new_d[new_key] = v
    return new_d
