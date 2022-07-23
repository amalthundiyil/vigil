from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.backend.server.commands.dashboard import get_validated_class
from sauron.cli.checks import DOMAINS


dashboard = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard.route("/", methods=["POST"])
def post():
    req = request.json
    data = []
    for domain in DOMAINS:
        p = get_validated_class(domain, req.get("url"), req.get("name"), req.get("type"), req.get("token"))
        d = p.process()
        if d:
            data.append(d)

    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Request processed successfully",
        data=data,
    )
