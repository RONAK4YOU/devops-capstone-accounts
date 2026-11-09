"""Accounts microservice application factory."""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()


def create_app(test_config=None):
    """Build and configure the Flask application."""
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///accounts.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app, resources={r"/accounts*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    Talisman(app, force_https=app.config.get("FORCE_HTTPS", False))

    from service.routes import accounts_bp

    app.register_blueprint(accounts_bp)

    @app.get("/")
    def health():
        return jsonify({"service": "accounts", "status": "ok"}), 200

    with app.app_context():
        db.create_all()
    return app
