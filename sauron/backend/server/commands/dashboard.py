from sauron.processor.base_processor import (
    BaseProcessor,
    ValidationError,
    final_summary,
)
from sauron.cli.checks_util import get_from_config
from sauron.cli.checks import DOMAINS
from sauron.backend.server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)


def get_validated_class(domain, url=None, name=None, type=None, token=None):
    token = get_from_config("github_token", token, silent=False)
    try:
        return BaseProcessor.get_processor_class(domain, url, name, type, token)
    except ValidationError as e:
        raise BadRequestError(e.message)


def full_process(p):
    score_data = p.process()
    summary_data = p.summarize()
    ts_data = p.server_ts()
    return {"score_data": score_data, "ts_data": ts_data, "summary": summary_data}


def summary(data):
    scores = []
    for domain in DOMAINS:
        scores.append(data[domain]["summary"]["score"])
    return final_summary(scores)


def get_package_info(p):
    return {"desc": p.backend.description, "type": p.type, "name": p.name, "url": p.url}


def get_es_data(url=None, name=None, type=None, token=None):
    from sauron.cli.db_utils import connect_es, get_db_data

    p = BaseProcessor.get_processor_class("community", url, name, type, token)
    es = connect_es()
    if not es:
        return
    es_data = get_db_data(p.url, p.name, p.type, es)
    if not es_data:
        return
    return es_data
