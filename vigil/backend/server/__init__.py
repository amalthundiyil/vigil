import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from vigil.backend.settings import DevelopmentSettings
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()


def create_app(config_class=DevelopmentSettings):
    app = Flask(__name__, static_folder="/static")
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    if os.environ.get("FLASK_ENV") == "development":
        cors.init_app(app, resources=r"/*", origins="*", supports_credentials=True)

    from vigil.backend.server.api.auth import auth
    from vigil.backend.server.api.home import home
    from vigil.backend.server.api.dashboard import dashboard
    from vigil.backend.server.api.errors import errors

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(dashboard)
    app.register_blueprint(errors)

    return app
