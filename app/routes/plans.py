
from flask import Blueprint, request, jsonify
from app.services.plan_service import PlanService

bp = Blueprint('plans', __name__, url_prefix='/plans')

@bp.route('/', methods=['GET'])
def list_plans():
    """
    List all subscription plans
    ---
    tags:
      - Plans
    responses:
      200:
        description: A list of available plans
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: Basic
                  price:
                    type: number
                    format: float
                    example: 9.99
    """
    plans = PlanService.list_plans()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in plans])


@bp.route('/', methods=['POST'])
def create_plan():
    """
    Create a new subscription plan
    ---
    tags:
      - Plans
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - price
            properties:
              name:
                type: string
                example: Premium
              price:
                type: number
                format: float
                example: 19.99
    responses:
      200:
        description: Plan created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 2
                name:
                  type: string
                  example: Premium
                price:
                  type: number
                  format: float
                  example: 19.99
    """
    data = request.get_json()
    plan = PlanService.create_plan(data['name'], data['price'])
    return jsonify({'id': plan.id, 'name': plan.name, 'price': plan.price})
