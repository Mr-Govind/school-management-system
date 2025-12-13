def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)



    @app.route("/")
    def index():
        return "SMS Version-1 Backend Running Successfully"

    return app
