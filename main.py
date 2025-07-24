# main.py

from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, jwt, migrate
from app.routes.plans import bp as plan_bp
from app.routes.subscription import bp as subscription_bp
from flasgger import Swagger
from app.routes.auth import bp as auth_bp
from app import models   
 


def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

 
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plan_bp,url_prefix='/api/plans')
    app.register_blueprint(subscription_bp, url_prefix='/api/subscriptions')
  

    @app.route("/", methods=["GET"])
    def hello():
        return {"message": "Hello, World!"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
