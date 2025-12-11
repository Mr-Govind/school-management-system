from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object("config.settings.Config")

    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.routes.teacher import teacher_bp
    app.register_blueprint(teacher_bp, url_prefix="/teacher")

    from app.routes.parent import parent_bp
    app.register_blueprint(parent_bp, url_prefix="/parent")

    @app.route("/")
    def index():
        return "SMS Version-1 Backend Running"

    return app
