from base.processor import BaseProcessor, ValidationError, final_summary
from constants import DOMAINS


def get_validated_class(domain, url=None, name=None, type=None, token=None):
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
