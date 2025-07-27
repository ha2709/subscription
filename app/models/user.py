from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    subscriptions = db.relationship("UserSubscription", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password_plain):
        self.password_hash = generate_password_hash(password_plain)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
