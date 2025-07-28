import random
from datetime import datetime, timedelta
from app.app_factory import create_app
from app.extensions import db
from app.models import UserSubscription

app = create_app()
app.app_context().push()

def seed_subscriptions(n=50000):
    subscriptions = []
    user_ids = list(range(1, 1001))  # 1,000 fake users
    plan_ids = [1, 2, 3]  # Assume 3 plans exist

    for _ in range(n):
        user_id = random.choice(user_ids)
        plan_id = random.choice(plan_ids)
        start_date = datetime.utcnow() - timedelta(days=random.randint(0, 1000))

        # Randomly assign end_date (None or a date)
        if random.random() < 0.7:  # 70% have ended
            end_date = start_date + timedelta(days=random.randint(30, 365))
        else:
            end_date = None

        subscriptions.append(UserSubscription(
            user_id=user_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            is_active=(end_date is None)
        ))

    db.session.bulk_save_objects(subscriptions)
    db.session.commit()
    print(f"Inserted {n} subscriptions.")

if __name__ == '__main__':
    seed_subscriptions()
