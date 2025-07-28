from app.models.user import User
from app.extensions import db

class UserRepository:
    @staticmethod
    def create_user(email, password):
        user = User(email=email)
        user.password = password 
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
