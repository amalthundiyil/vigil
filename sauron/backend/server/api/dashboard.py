import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.backend.server.commands.dashboard import get_validated_class, full_process, summary, get_package_info
from sauron.cli.checks import DOMAINS


LOG = logging.getLogger("sauron.backend.server.api.dashboard")
dashboard = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard.route("/", methods=["POST"])
def post():
    req = request.json
    LOG.info("Collecting dashboard data...") 
    data = {}
    for domain in DOMAINS:
        p = get_validated_class(domain, req.get("url"), req.get("name"), req.get("type"), req.get("github_token"))
        d = full_process(p)
        data[domain] = d
        LOG.info(data[domain])
        print(data[domain])
    final_score, final_desc = summary(data)
    data["description"] = get_package_info(p)
    data["final_score"] = final_score,
    data["final_desc"] = final_desc
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Request processed successfully",
        data=data,
    )
