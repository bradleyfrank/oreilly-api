import os

class Config:
    """Production config values."""

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@postgres/oreilly".format(
        os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
    )

class Production(Config):
    pass

class Testing(Config):
    """Testing config values."""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True