from flask import Blueprint, jsonify, request
from http import HTTPStatus
from pandas import DataFrame
from sauron.backend.server.commands.auth import tokens_required
from sauron.backend.server.api.errors import BadRequestError

users = Blueprint("user", __name__, url_prefix="/api/user")


@users.route("/classifier", methods=["POST"])
@tokens_required
def classify(user_id):
    req = request.json
    if not req:
        raise BadRequestError("No data to classify.")
    features, values = [], []
    for feature, value in req.items():
        features.append("log_" + feature)
        values.append(log1p(value))
    prediction = int(classifier.predict(DataFrame([values], columns=features)))
    return (
        jsonify(
            status_code=HTTPStatus.OK,
            message="Prediction successful",
            data={"prediction": prediction},
        ),
        HTTPStatus.OK,
    )
