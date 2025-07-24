from app.models.plan import Plan
from app.extensions import db

class PlanRepository:
    @staticmethod
    def create_plan(name, price):
        plan = Plan(name=name, price=price)
        db.session.add(plan)
        db.session.commit()
        return plan

    @staticmethod
    def list_plans():
        return Plan.query.all()
