import pytest
from main import create_app
from app.extensions import db 
from app.models import User, Plan, UserSubscription
from flask_jwt_extended import create_access_token, JWTManager
from datetime import datetime, timedelta

@pytest.fixture
def client():
 
    test_config = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret'
    }

    app = create_app(config_override=test_config)

    JWTManager(app)  # just to be safe in test env

    with app.app_context():
        db.create_all()
        yield app.test_client()

        # Clean up only if in-memory database is used
        uri = app.config["SQLALCHEMY_DATABASE_URI"]
        
        if "sqlite:///:memory:" in uri:
            print("Delete in DB")
            db.session.remove()
            db.drop_all()
        else:
            print("⚠️ Skipped drop_all to avoid deleting real DB.")


def create_user_and_token(app):
    with app.app_context():
        user = User(email="test1@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=str(user.id))
        return user, access_token


def create_plan(app):
    with app.app_context():
        plan = Plan(name="Basic", price=10.0)
        db.session.add(plan)
        db.session.commit()
        return plan.id  # Return the ID only


def test_create_subscription(client):
    print(client.application.url_map) 
    user, token = create_user_and_token(client.application)
    plan = create_plan(client.application)
 
    response = client.post(
        "api/subscriptions/",
        json={"plan_id": plan, "user_id":user.id},
        headers={"Authorization": f"Bearer {token}"}
    )
  
    assert response.status_code == 200


def test_active_subscription(client):
    with client.application.app_context():
        user, token = create_user_and_token(client.application)
        print(70, token)
        print("Available routes:")
        for rule in client.application.url_map.iter_rules():
            print(f"{rule.endpoint:30s} {rule.methods} {rule.rule}")

        plan = create_plan(client.application)
        print(57, plan)
        sub = UserSubscription(
            user_id=user.id, 
            plan_id=plan, 
            start_date=datetime.utcnow(),
           
        )

 
        db.session.add(sub)
        db.session.commit()
        print(75, sub)
        response = client.get(
            "api/subscriptions/active",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(78, response)
        assert response.status_code == 200
        data = response.get_json()
        assert data['plan_id'] == plan
