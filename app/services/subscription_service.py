from app.repositories.subscription_repository import SubscriptionRepository

class SubscriptionService:
    @staticmethod
    def create_subscription(user_id: int, plan_id: int):
        return SubscriptionRepository.create_subscription(user_id, plan_id)

    @staticmethod
    def cancel_subscription(subscription_id: int):
        return SubscriptionRepository.cancel_subscription(subscription_id) 

    @staticmethod
    def list_all_subscriptions(user_id, page, page_size):
        return SubscriptionRepository.get_paginated_subscriptions(user_id, page, page_size)

    @staticmethod
    def count_subscriptions(user_id):
        return SubscriptionRepository.count_subscriptions(user_id)

    @staticmethod
    def get_subscription_history(user_id, page, page_size):
        return SubscriptionRepository.get_paginated_subscription_history(user_id, page, page_size)

    @staticmethod
    def count_subscription_history(user_id):
        return SubscriptionRepository.count_subscription_history(user_id)

    @staticmethod
    def get_active_subscriptions(user_id, page, page_size):
        return SubscriptionRepository.get_active_subscriptions_paginated(user_id, page, page_size)

    @staticmethod
    def count_active_subscriptions(user_id):
        return SubscriptionRepository.count_active_subscriptions(user_id)