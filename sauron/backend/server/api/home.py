from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.cli.checks import DOMAINS


home = Blueprint("home", __name__, url_prefix="/api/home")


@home.route("/", methods=["GET"])
def get():
    data = []
    return jsonify(
        status_code=HTTPStatus.OK,
        message="Request processed successfully",
        data=data,
    )

