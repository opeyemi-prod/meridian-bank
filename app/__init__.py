"""Meridian Bank API — application factory."""

import traceback

from flask import Flask, request, Response

from app.config import config_by_name


def create_app(env="production"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])

    from app.auth.routes import auth_bp
    from app.accounts.routes import accounts_bp
    from app.transfers.routes import transfers_bp
    from app.admin.routes import admin_bp
    from app.statements.routes import statements_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(transfers_bp, url_prefix="/api/transfers")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(statements_bp, url_prefix="/api/statements")

    @app.after_request
    def apply_cors(response):
        origin = request.headers.get("Origin")
        response.headers["Access-Control-Allow-Origin"] = origin or "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    @app.errorhandler(500)
    def internal_error(e):
        return Response(traceback.format_exc(), mimetype="text/plain"), 500

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
