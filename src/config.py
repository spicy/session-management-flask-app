import os
from datetime import timedelta


class BaseConfig:
    # Common configurations
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True

    ERROR_404_TITLE = "404 Not Found"
    ERROR_500_TITLE = "500 Internal Server Error"
    ERROR_404_MESSAGE = "The requested page could not be found."
    ERROR_500_MESSAGE = "An unexpected error has occurred. Please try again later."

    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.getcwd(), "flask_session")
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    COOKIE_LIFETIME = timedelta(minutes=30)
    SESSION_USE_SIGNER = True

    USERNAME_REGEX = r"^[A-Z][a-z]+_[A-Z][a-z]+$"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(BaseConfig):
    TESTING = True


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
