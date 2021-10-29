import os
from typing import Optional

from flask import Flask, jsonify


def create_app(test_config: Optional[dict] = None) -> Flask:
    # pylint: disable=import-outside-toplevel, too-many-locals
    app = Flask(__name__, static_folder="staticfiles")

    from flask_cors import CORS

    CORS(app)

    from datetime import timedelta

    app.config.from_mapping(
        SECRET_KEY="dev",
        PROPAGATE_EXCEPTIONS=True,
        # SQLAlchemy Setup
        SQLALCHEMY_DATABASE_URI=os.path.join(app.instance_path, "db.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # JWT Setup
        JWT_SECRET_KEY="dev",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=7),
        JWT_ERROR_MESSAGE_KEY="message",
    )

    if not test_config:
        from .config import config

        app.secret_key = config.get_secret()
        app.config["SQLALCHEMY_DATABASE_URI"] = config.get_db_address()
        app.config["JWT_SECRET_KEY"] = app.secret_key
    else:
        app.config.update(test_config)

    from .db import db

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    from flask_jwt_extended import JWTManager

    from .security import user_identity_lookup, user_lookup_callback

    jwt = JWTManager(app)
    jwt.user_identity_loader(user_identity_lookup)
    jwt.user_lookup_loader(user_lookup_callback)

    from flask import json, redirect
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = json.dumps({"message": e.description})
        response.content_type = "application/json"
        return response

    from .routers import user, swagger

    app.register_blueprint(user.router, url_prefix="/users")
    app.register_blueprint(swagger.router)

    @app.route("/")
    def hello_world():
        return redirect("/docs")

    # from .sc_memory.helpers.user import create_user_in_memory, check_user_in_memory

    @app.route("/im_teapot")
    def test_memory():
        # create_user_in_memory(1)
        # check_user_in_memory(1)

        return jsonify({"message": "I'm a teapot"}), 418

    return app
