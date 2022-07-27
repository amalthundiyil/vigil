from http import HTTPStatus

import jwt
from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.processor.base_processor import BaseProcessor, ValidationError
from sauron.backend.server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)


def get_validated_class(domain, url=None, name=None, type=None, token=None):
    try:
        return BaseProcessor.get_processor_class(domain, url, name, type, token)
    except ValidationError as e:
        raise BadRequestError(e.message)
