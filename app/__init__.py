from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from config.settings import Config
from flask_cors import CORS



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    
    # -------------------------
    # CORS CONFIGURATION
    # -------------------------
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True
    )

    # Import models AFTER db init
    from app import models

    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.teacher import teacher_bp
    from app.routes.parent import parent_bp
    from app.routes.attendance import attendance_bp
    from app.routes.cms import cms_bp


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cms_bp, url_prefix="/cms")
    app.register_blueprint(parent_bp, url_prefix="/parent")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")

    @app.route("/")
    def index():
        return "SMS Version-1 Backend successfully"

    @app.route("/health/db")
    def db_health_check():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "details": str(e)}, 500

    return app
