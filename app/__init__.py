from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.settings import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints (empty for now — we will fill later)
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def index():
        return "SMS Version-1 Backend Running Successfully"

    return app
