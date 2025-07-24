from app.repositories.user_repository import UserRepository
from werkzeug.exceptions import BadRequest, Unauthorized

class UserService:
    @staticmethod
    def register(email, password):
        if UserRepository.get_by_email(email):
            raise BadRequest("Email already registered")
        return UserRepository.create_user(email, password)

    @staticmethod
    def login(email, password):
        user = UserRepository.get_by_email(email)
        if not user or not user.check_password(password):
            raise Unauthorized("Invalid credentials")
        return user
