from sauron.processor.base_processor import BaseProcessor, ValidationError
from sauron.cli.checks_util import get_from_config
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
    ts_data = p.server_ts()
    return {"score_data": score_data, "ts_data": ts_data}