import os
import secrets
from sauron import ROOT_SAURON_DIRECTORY


class Settings:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)
    SQLITE_DB_PATH = os.path.join(
        os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "sqlite.db"
    )
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{SQLITE_DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REFRESH_TOKEN_LIFE = "5"
    ACCESS_TOKEN_LIFE = "3"


class ProductionSettings(Settings):
    DEBUG = False


class StagingSettings(Settings):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentSettings(Settings):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Settings):
    TESTING = True
