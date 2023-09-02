import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, make_response

from vigil.backend.server.commands.dashboard import (
    get_validated_class,
    full_process,
    summary,
    get_package_info,
    get_es_data,
)
from vigil.cli.checks import DOMAINS
from vigil.cli.db_utils import add_data, connect_es


LOG = logging.getLogger("vigil.backend.server.api.dashboard")
dashboard = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard.route("/", methods=["POST"])
def post():
    req = request.json
    LOG.info("Collecting dashboard data...")
    data = {}
    es_data = get_es_data(
        req.get("url"), req.get("name"), req.get("type"), req.get("github_token")
    )
    if es_data:
        return jsonify(
            status_code=HTTPStatus.CREATED,
            message="Request processed successfully",
            data=es_data,
        )

    for domain in DOMAINS:
        p = get_validated_class(
            domain,
            req.get("url"),
            req.get("name"),
            req.get("type"),
            req.get("github_token"),
        )
        d = full_process(p)
        data[domain] = d
        LOG.info(data[domain])
        print(data[domain])
    data["final_score"], data["final_desc"] = summary(data)
    pkg_info = get_package_info(p)
    data["name"], data["type"], data["description"], data["url"] = (
        pkg_info["name"],
        pkg_info["type"],
        pkg_info["desc"],
        pkg_info["url"],
    )
    es = connect_es()
    res = add_data(es, data)
    print(res)
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Request processed successfully",
        data=data,
    )
