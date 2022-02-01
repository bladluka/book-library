from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.commands import db_manage_bp
    from app.authors import authors_bp
    from app.books import books_bp
    from app.errors import errors_bp

    app.register_blueprint(db_manage_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(errors_bp)

    return app
