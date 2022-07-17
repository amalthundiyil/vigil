import datetime
from sauron.backend.server import db
from flask import current_app, request
import jwt
import secrets
from sauron.backend.server.api.errors import UnauthorizedError


class User(db.Model):
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def generate_tokens(self):
        expires_in = datetime.datetime.utcnow().timestamp() + int(
            current_app.config["ACCESS_TOKEN_LIFE"] * 60
        )
        access_token = jwt.encode(
            payload={"user_id": self.id, "exp": expires_in},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")
        xsrf_token = secrets.token_hex(16)
        return [access_token, xsrf_token, expires_in]

    def generate_refresh_token(self):
        refresh_token = jwt.encode(
            payload={
                "user_id": self.id,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=int(current_app.config["REFRESH_TOKEN_LIFE"])
                ),
            },
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return refresh_token

    def __repr__(self):
        return f"User({self.username}, {self.email}"
