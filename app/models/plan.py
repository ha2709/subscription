from app.extensions import db

class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    subscriptions = db.relationship('UserSubscription', back_populates="plan")
 

    
