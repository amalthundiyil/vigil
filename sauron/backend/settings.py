import os


class Settings:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REFRESH_TOKEN_LIFE = os.environ.get("REFRESH_TOKEN_LIFE")
    ACCESS_TOKEN_LIFE = os.environ.get("ACCESS_TOKEN_LIFE")


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