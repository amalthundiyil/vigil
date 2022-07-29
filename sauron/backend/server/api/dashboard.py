import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, make_response

from sauron.backend.server.commands.dashboard import get_validated_class, full_process, final_summary
from sauron.cli.checks import DOMAINS


LOG = logging.getLogger("sauron.backend.server.api.dashboard")
dashboard = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard.route("/", methods=["POST"])
def post():
    req = request.json
    LOG.info("Collecting dashboard data...") 
    data = []
    for domain in DOMAINS:
        p = get_validated_class(domain, req.get("url"), req.get("name"), req.get("type"), req.get("github_token"))
        d = full_process(p)
        data.append({"domain": domain, "data": d})
        print({"domain": domain, "data": d})
        LOG.info({"domain": domain, "data": d}) 
    import pdb; pdb.set_trace()
    final_score, final_desc = final_summary(data)
    data.append({"final_score": final_score, "final_desc": final_desc})
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Request processed successfully",
        data=data,
    )
