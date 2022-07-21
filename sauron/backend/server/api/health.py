from flask import Blueprint, jsonify, request, current_app, make_response
from sauron.backend.server.commands.auth import clear_tokens, refresh_tokens
from sauron.backend.server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)
from http import HTTPStatus
import jwt
from http import HTTPStatus
from sauron.processor.popularity import GithubPopularity
from sauron.processor.community import CommunityProcessor


health = Blueprint("health", __name__, url_prefix="/api/health")


@health.route("/popularity", methods=["POST"])
def check_popularity():
    req = request.json
    if not req:
        raise BadRequestError("Fields cannot be empty.")
    if not req.url:
        raise BadRequestError("Please enter the URL.")
    p = GithubPopularity(req.url, req.token)
    data = p.process()
    if not data:
        raise NoContentError("Failed to process request.")

    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Sent request successfully",
        data=data,
    )

@health.route("/community", methods=["POST"])
def check_community():
    req = request.json
    if not req:
        raise BadRequestError("Fields cannot be empty.")
    if not req.url:
        raise BadRequestError("Please enter the URL.")
    p = CommunityProcessor(req.url, req.token)
    data = p.process()
    if not data:
        raise NoContentError("Failed to process request.")

    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Sent request successfully",
        data=data,
    )

