from sqlalchemy.sql import text
from app.models.user_subscription import UserSubscription
from app.extensions import db

class SubscriptionRepository:
    """
    Repository for performing optimized database operations on UserSubscription table.

    Optimization Highlights:
    -------------------------
    1. Custom SQL with parameter binding avoids ORM overhead and is faster for large datasets.
    2. Indexed columns (`user_id`, `end_date`, `start_date`) allow efficient filtering and sorting.
    3. Composite indexes (e.g., `user_id` + `end_date`) directly match query filters.
    4. Sorted queries use the same columns as indexes → minimizes disk I/O and CPU sort.
    """
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
    def get_paginated_subscriptions(user_id, page, page_size):
        offset = (page - 1) * page_size
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id
            ORDER BY start_date DESC
            LIMIT :limit OFFSET :offset
        """)
        return db.session.execute(sql, {
            'user_id': user_id,
            'limit': page_size,
            'offset': offset
        }).fetchall()

    @staticmethod
    def count_subscriptions(user_id):
        sql = text("""
            SELECT COUNT(*) FROM user_subscription WHERE user_id = :user_id
        """)
        result = db.session.execute(sql, {'user_id': user_id}).scalar()
        return result

    @staticmethod
    def get_paginated_subscription_history(user_id, page, page_size):
        offset = (page - 1) * page_size
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id AND end_date IS NOT NULL
            ORDER BY end_date DESC
            LIMIT :limit OFFSET :offset
        """)
        return db.session.execute(sql, {
            'user_id': user_id,
            'limit': page_size,
            'offset': offset
        }).fetchall()

    @staticmethod
    def count_subscription_history(user_id):
        sql = text("""
            SELECT COUNT(*) FROM user_subscription
            WHERE user_id = :user_id AND end_date IS NOT NULL
        """)
        return db.session.execute(sql, {'user_id': user_id}).scalar()
    
    @staticmethod
    def get_active_subscriptions_paginated(user_id, page=1, page_size=10):
        offset = (page - 1) * page_size

        query = text("""
            SELECT id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id
              AND is_active = TRUE
            ORDER BY start_date DESC
            LIMIT :limit OFFSET :offset
        """)
        result = db.session.execute(query, {
            'user_id': user_id,
            'limit': page_size,
            'offset': offset
        }).fetchall()

        return result

    @staticmethod
    def count_active_subscriptions(user_id):
        sql = text("""
            SELECT COUNT(*) FROM user_subscription
            WHERE user_id = :user_id AND is_active = true
        """)
        return db.session.execute(sql, {'user_id': user_id}).scalar()
    
   