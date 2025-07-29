from main import create_app
from app.extensions import db 
from app.models import User, Plan, UserSubscription
from datetime import datetime, timedelta
import random

app = create_app()

def seed_subscriptions():
    with app.app_context():
        print("Creating test users and plans...")

        # Clean up first (optional)
        db.session.query(UserSubscription).delete()
        db.session.query(User).delete()
        db.session.query(Plan).delete()
        db.session.commit()

        # Create test users
        users = [User(email=f"user{i}@example.com", password_hash="hashed") for i in range(1, 11)]
        db.session.bulk_save_objects(users)
        db.session.commit()

        user_ids = [user.id for user in User.query.all()]

        # Create test plan
        plan = Plan(name="Basic", price=9.99)
        db.session.add(plan)
        db.session.commit()
        plan_id = plan.id

        print(f"Seeding 50,000 subscriptions using {len(user_ids)} users and plan {plan_id}...")

        batch_size = 1000
        total = 50000
        for i in range(0, total, batch_size):
            batch = []
            for _ in range(batch_size):
                user_id = random.choice(user_ids)
                start_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
                end_date = (
                    start_date + timedelta(days=random.randint(30, 180))
                    if random.random() > 0.5 else None
                )
                batch.append(UserSubscription(
                    user_id=user_id,
                    plan_id=plan_id,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=(end_date is None)
                ))
            db.session.bulk_save_objects(batch)
            db.session.commit()
            print(f"Inserted {i + batch_size}/{total} subscriptions...")

        print(" Seeding completed.")

if __name__ == "__main__":
    seed_subscriptions()
