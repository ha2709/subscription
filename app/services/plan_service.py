# app/services/plan_service.py
from app.repositories.plan_repository import PlanRepository

class PlanService:
    @staticmethod
    def list_plans():
        return PlanRepository.list_plans()

    @staticmethod
    def create_plan(name, price):
        return PlanRepository.create_plan(name, price)
