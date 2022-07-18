import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sauron.backend.settings import DevelopmentSettings
from flask_cors import CORS
from flask_migrate import Migrate, stamp, migrate, upgrade

MIGRATION_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "models", "migrations"
)
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
mgr = Migrate()


def create_app(config_class=DevelopmentSettings):
    app = Flask(__name__, static_folder="/static")
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    mgr.init_app(app, db, directory=MIGRATION_DIR)
    if os.environ.get("FLASK_ENV") == "development":
        cors.init_app(app, resources=r"/*", origins="*", supports_credentials=True)

    from sauron.backend.server.api.auth import auth
    from sauron.backend.server.api.users import users
    from sauron.backend.server.api.dashboard import dashboard
    from sauron.backend.server.api.health import health
    from sauron.backend.server.api.vulns import vulns
    from sauron.backend.server.api.errors import errors

    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(dashboard)
    app.register_blueprint(health)
    app.register_blueprint(vulns)
    app.register_blueprint(errors)

    @app.before_first_request
    def deploy():
        # create databse and tables
        db.create_all()
        # migrate databsae to latest revision
        stamp()
        migrate()
        upgrade()

    return app
