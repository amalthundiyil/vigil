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

from sauron.processor.processors.vulns import VulnsProcessor


vulns = Blueprint("vulns", __name__, url_prefix="/api/vulns")


@vulns.route("/community", methods=["POST"])
def check_community():
    req = request.json
    if not req:
        raise BadRequestError("Fields cannot be empty.")
    if not req["url"]:
        raise BadRequestError("Please enter the URL.")
    v = VulnsProcessor(req["url"], req.get("token"))
    data = v.process()
    if not data:
        raise NoContentError("Failed to process request.")
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Sent request successfully",
        data=data,
    )
