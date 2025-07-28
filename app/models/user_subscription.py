from datetime import datetime
from app.extensions import db


class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # __table_args__ = (
    #         db.Index('idx_user_active', 'user_id', 'is_active'),
    #         db.Index('idx_user_start_date', 'user_id', 'start_date'),
    #         db.Index('idx_user_plan', 'user_id', 'plan_id'),
    #         db.Index('idx_user_end_date', 'user_id', 'end_date')

    #     )
    # Relationships
    user = db.relationship("User", back_populates="subscriptions")    
    plan = db.relationship("Plan", back_populates="subscriptions")




 