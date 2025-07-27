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
    def get_user_active_subscription(user_id):
        return UserSubscription.query.filter_by(user_id=user_id, is_active=True).first()

    
    @staticmethod
    def get_active_subscription(user_id):
        sql = text("""
            SELECT id, user_id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id
              AND end_date IS NULL
            LIMIT 1
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchone()

    @staticmethod
    def list_all_subscriptions(user_id):
        """
        Get all subscriptions for a user ordered by start date descending.
        
        Performance Optimized:
        - Uses `user_id` and `start_date` index (idx_user_start_date).
        - Efficient for dashboards or subscription timelines.

        Returns: List of subscription rows (id, plan_id, start_date, end_date).
        """
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id
            ORDER BY start_date DESC
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchall()

    @staticmethod
    def get_subscription_history(user_id):
        """
        Get all **ended** subscriptions for a user, ordered by end date descending.

        Performance Optimized:
        - Filters by `user_id` and `end_date IS NOT NULL`.
        - Leverages composite index: (user_id, end_date) → speeds up both filtering & sorting.

        Why filter `end_date IS NOT NULL`?
        - Only subscriptions with an end date are considered "past" or "historical".
        - This avoids mixing in current/active subscriptions.

        Returns: List of past subscription rows (id, plan_id, start_date, end_date).
        """
        sql = text("""
            SELECT id, plan_id, start_date, end_date
            FROM user_subscription
            WHERE user_id = :user_id
              AND end_date IS NOT NULL
            ORDER BY end_date DESC
        """)
        return db.session.execute(sql, {'user_id': user_id}).fetchall()
