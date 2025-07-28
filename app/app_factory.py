from flask import Flask
from app.extensions import db, migrate  
import app.models
from app.routes import  plans, subscription
from app.routes.auth import bp as auth_bp


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(plans.bp)
    app.register_blueprint(subscription.bp)
    return app
