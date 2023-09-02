from http import HTTPStatus

import os
from flask import Blueprint, jsonify, current_app
from vigil.backend.settings import DevelopmentSettings

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def error_handler(e):
    err = {
        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
        "message": "Something went wrong, please try again later.",
    }

    if isinstance(e, APIError):
        err["status_code"] = e.status_code
        err["message"] = e.message
    elif e.__class__.__name__ == "NotFound":
        err["status_code"] = HTTPStatus.NOT_FOUND
        err["message"] = "Route not found."
    else:
        if os.environ.get("FLASK_ENV") == "development":
            err["message"] = repr(e)
    return jsonify(err), err["status_code"]


class APIError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        if status_code:
            self.status_code = status_code
        self.message = message
        self.payload = payload


class BadRequestError(APIError):
    def __init__(self, message):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class ForbiddenError(APIError):
    def __init__(self, message):
        super().__init__(message, status_code=HTTPStatus.FORBIDDEN)


class MethodNotAllowedError(APIError):
    def __init__(self, message):
        super().__init__(message, status_code=HTTPStatus.METHOD_NOT_ALLOWED)


class NoContentError(APIError):
    def __init__(self, message):
        super().__init__(message, HTTPStatus.NO_CONTENT)


class UnauthorizedError(APIError):
    def __init__(self, message):
        super().__init__(message, HTTPStatus.UNAUTHORIZED)
