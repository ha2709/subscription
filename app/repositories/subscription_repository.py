from app.models.user_subscription import UserSubscription
from app.extensions import db

class SubscriptionRepository:
    @staticmethod
    def create_subscription(user_id, plan_id):
        subscription = UserSubscription(user_id=user_id, plan_id=plan_id)
        db.session.add(subscription)
        db.session.commit()
        return subscription

    @staticmethod
    def cancel_subscription(subscription_id):
        sub = UserSubscription.query.get(subscription_id)
        if sub:
            sub.is_active = False
            db.session.commit()
        return sub

    @staticmethod
    def get_user_active_subscription(user_id):
        return UserSubscription.query.filter_by(user_id=user_id, is_active=True).first()

    
    @staticmethod
    def get_active_subscription(user_id):
        sql = text("""
            SELECT id, user_id, plan_id, start_date, end_date
            FROM subscriptions
            WHERE user_id = :user_id
              AND end_date IS NULL
            LIMIT 1
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchone()

    @staticmethod
    def list_all_subscriptions(user_id):
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM subscriptions
            WHERE user_id = :user_id
            ORDER BY start_date DESC
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchall()

    @staticmethod
    def get_subscription_history(user_id):
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM subscriptions
            WHERE user_id = :user_id
              AND end_date IS NOT NULL
            ORDER BY end_date DESC
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchall()
