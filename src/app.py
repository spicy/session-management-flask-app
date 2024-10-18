import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from config import config_by_name
from flask_session import Session
from forms.login_form import csrf
from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint


def create_app():
    app = Flask(__name__)

    # Determine the configuration based on the FLASK_ENV environment variable
    flask_env = os.environ.get("FLASK_ENV", "development").lower()
    app.config.from_object(config_by_name[flask_env])

    Session(app)
    csrf.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Server Error: {e}")
        return render_template("500.html"), 500

    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/flask_app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Flask app startup")

    return app


def setup_logging(app):
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/error.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)


if __name__ == "__main__":
    app = create_app()
    setup_logging(app)
    app.run()
