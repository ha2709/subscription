from app import db, create_app
from app.repositories.subscription_repository import SubscriptionRepository
import time

app = create_app()  

def test_list_subscriptions_performance():
    user_id = 1  

    with app.app_context():
        start = time.perf_counter()
        results = SubscriptionRepository.list_all_subscriptions(user_id)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000
        print(f"[PERF] list_all_subscriptions took {duration_ms:.2f}ms for user_id={user_id}")
        assert duration_ms < 200


def test_subscription_history_performance():
    user_id = 1

    with app.app_context():
        start = time.perf_counter()
        results = SubscriptionRepository.get_subscription_history(user_id)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000
        print(f"[PERF] get_subscription_history took {duration_ms:.2f}ms for user_id={user_id}")
        assert duration_ms < 200
