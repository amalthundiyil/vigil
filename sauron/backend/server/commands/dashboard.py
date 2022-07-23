from http import HTTPStatus

import jwt
from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.processor.processors.popularity import PopularityProcessor
from sauron.backend.server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)


def filter_dashboard(request):
    req = request.json
    try:
        validate(req.get("url"), req.get("name"), req.get("type"))
    except ValidationError as e:
        raise BadRequestError(e.message)
    return req


def process_popularity(req):
    if req.get("name") and req.get("type"):
        p = PopularityProcessor.from_name(
            req.get("name"), req.get("type"), req.get("github_token")
        )
    elif req.get("url"):
        
        p = PopularityProcessor.from_url(req["url"], req.get("github_token"))
    data = p.process()
    if not data:
        raise NoContentError("Failed to process request.")
    return data
