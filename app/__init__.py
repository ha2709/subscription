from flask import Flask
from app.extensions import db, migrate  
import app.models
from app.routes import  plans, subscription
from app.routes.auth import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    # Register blueprints

    app.register_blueprint(auth_bp, url_prefix='/api/auth')

  
    app.register_blueprint(plans.bp)
    app.register_blueprint(subscription.bp)
    return app
