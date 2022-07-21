from flask import Blueprint, jsonify, request, current_app, make_response
from sauron.backend.server import bcrypt, db
from sauron.backend.server.models.user import User
from sauron.backend.server.commands.auth import clear_tokens, refresh_tokens
from sauron.backend.server.api.errors import (
    BadRequestError,
    NoContentError,
    ForbiddenError,
    UnauthorizedError,
)
from http import HTTPStatus
import jwt


auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.route("/register", methods=["POST"])
def register():
    req = request.json
    if not req:
        raise BadRequestError("Fields cannot be empty.")
    user = User.query.filter_by(username=req["username"]).first()
    if user:
        raise BadRequestError("Please choose a unique username.")
    user = User.query.filter_by(email=req["email"]).first()
    if user:
        raise BadRequestError("Please choose a unique email.")

    hashed_password = bcrypt.generate_password_hash(
        req["password"],
    ).decode("utf-8")
    user = User(username=req["username"], email=req["email"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        status_code=HTTPStatus.CREATED,
        message="Your account has been created",
        data={"user_id": user.id},
    )


@auth.route("/login", methods=["POST"])
def login():
    req = request.json
    if not req:
        raise BadRequestError("Fields cannot be empty.")
    user = User.query.filter_by(email=req["email"]).first()
    if not user:
        raise BadRequestError("Sorry. No user was found with this email.")
    if not bcrypt.check_password_hash(user.password, req["password"]):
        raise BadRequestError("Please enter valid password.")

    tokens = user.generate_tokens()
    access_token, xsrf_token, expires_in = tokens[0], tokens[1], tokens[2]
    refresh_token = user.generate_refresh_token()
    refresh_tokens[refresh_token] = xsrf_token
    data = {"user_id": user.id, "token": access_token, "expires_in": expires_in}
    res = make_response(data)
    res.set_cookie("XSRF-TOKEN", xsrf_token, httponly=True)
    res.set_cookie("refresh_token", refresh_token, httponly=True)
    return res, HTTPStatus.OK


@auth.route("/verify", methods=["POST"])
def verify():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise NoContentError("No session found.")
    xsrf_token = request.cookies.get("XSRF-TOKEN")
    if not xsrf_token or not refresh_tokens.get(xsrf_token) != xsrf_token:
        clear_tokens()
        raise ForbiddenError("Access denied.")
    try:
        old_token = jwt.decode(refresh_token, current_app.config["SECRET_KEY"])
        user = User.query.get(old_token.get("user_id"))
        if not user:
            raise UnauthorizedError("Authorization failed")
    except:
        clear_tokens()
        raise UnauthorizedError("blip")
    tokens = user.generate_tokens()
    access_token, xsrf_token, expires_in = tokens[0], tokens[1], tokens[2]
    refresh_tokens[refresh_token] = xsrf_token
    data = {"user_id": user.id, "token": access_token, "expires_in": expires_in}
    res = make_response(data)
    res.set_cookie("XSRF-TOKEN", xsrf_token, httponly=True)
    return res, HTTPStatus.OK


@auth.route("/logout", methods=["GET"])
def logout():
    clear_tokens()
    data = {"status_code": HTTPStatus.OK, "message": "You have sucessfully logged out"}
    res = make_response(data)
    res.set_cookie("XSRF-TOKEN", "", expires=0)
    res.set_cookie("refresh_token", "", expires=0)
    return res, HTTPStatus.OK
