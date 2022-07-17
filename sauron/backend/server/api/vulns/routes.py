from flask import Blueprint, jsonify, request, current_app, make_response
from server import bcrypt, db
from server.models.user import User
from server.commands.auth import clear_tokens, refresh_tokens
from server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)
from http import HTTPStatus
import jwt


vulns = Blueprint("vulns", __name__, url_prefix="/api/v1/vulns")


@vulns.route("/vulns", methods=["GET"])
def go():
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Your account has been created",
        data={"vulns": "ok"},
    )


