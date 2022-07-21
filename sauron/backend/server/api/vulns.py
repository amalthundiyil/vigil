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


vulns = Blueprint("vulns", __name__, url_prefix="/api/vulns")


@vulns.route("/vulns", methods=["GET"])
def go():
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Your account has been created",
        data={"vulns": "ok"},
    )


