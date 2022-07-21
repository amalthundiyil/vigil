from flask import request, current_app
from functools import wraps
from sauron.backend.server.api.errors import ForbiddenError, NoContentError, UnauthorizedError
from sauron.backend.server.models.user import User
import jwt

refresh_tokens = {}


def clear_tokens():
    refresh_token = request.cookies.get("refresh_token")
    del refresh_token


def tokens_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers["authorization"].split("Bearer ")[1]
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
            refresh_token = request.cookies.get("refresh_token")
            if not refresh_token:
                raise NoContentError("No session found.")
            xsrf_token = request.cookies.get("XSRF-TOKEN")
            if not xsrf_token or not refresh_tokens.get(xsrf_token) != xsrf_token:
                raise ForbiddenError("Access denied.")
            old_token = jwt.decode(refresh_token, current_app.config["SECRET_KEY"])
            user = User.query.get(old_token.get("user_id"))
            if not user:
                raise UnauthorizedError("Authorization failed")
        except:
            clear_tokens()
            raise UnauthorizedError("Authorization failed.")
        return f(user.id, *args, **kwargs)

    return wrapper
