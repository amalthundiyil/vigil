from flask import Blueprint, jsonify, request, current_app, make_response
from server import bcrypt, db
from server.commands.auth import clear_tokens, refresh_tokens
from server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)
from http import HTTPStatus
from server.commands import vulns
import jwt


dashboard = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard.route("/", methods=["POST"])
def post():
    req = request.json
    url = req["url"]
    if not url:
        return jsonify(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Please specify a URL",
            data={},
        )
    reports = vulns.process_vulns(url)
    return jsonify(
        status_code=HTTPStatus.OK,
        message=reports,
        data={},
    )


@dashboard.route("/", methods=["GET"])
def get():
    req = request.json
    url = req["url"]
    if not url:
        return jsonify(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Please specify a URL",
            data={},
        )
    return jsonify(
        status_code=HTTPStatus.OK,
        message=res.stdout,
        data={},
    )
