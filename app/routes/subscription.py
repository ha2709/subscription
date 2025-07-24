from flask import Blueprint, request, jsonify
from app.services.subscription_service import SubscriptionService
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')

@bp.route('/', methods=['POST'])
@jwt_required()
def subscribe():
    """
    Create a new subscription
    ---
    tags:
      - Subscriptions
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_id
              - plan_id
            properties:
              user_id:
                type: integer
              plan_id:
                type: integer
    responses:
      200:
        description: Subscription created
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                user_id:
                  type: integer
                plan_id:
                  type: integer
    """
    data = request.get_json()
    user_id = get_jwt_identity()
    sub = SubscriptionService.create_subscription(user_id, data['plan_id'])
    return jsonify({
        'id': sub.id,
        'user_id': sub.user_id,
        'plan_id': sub.plan_id
    })

@bp.route('/<int:subscription_id>/cancel', methods=['POST'])
def cancel(subscription_id):

    """
    Cancel a subscription
    ---
    tags:
      - Subscriptions
    parameters:
      - name: subscription_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Subscription cancelled
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Subscription not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """

    sub = SubscriptionService.cancel_subscription(subscription_id)
    if sub:
        return jsonify({'message': 'Subscription cancelled'})
    return jsonify({'message': 'Subscription not found'}), 404


@bp.route('/<int:subscription_id>', methods=['PUT'])
def upgrade(subscription_id):
    """
    Upgrade or change a user's subscription plan
    ---
    tags:
      - Subscriptions
    parameters:
      - name: subscription_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - plan_id
            properties:
              plan_id:
                type: integer
    responses:
      200:
        description: Subscription updated
      404:
        description: Subscription not found
    """
    data = request.get_json()
    updated_sub = SubscriptionService.update_subscription(subscription_id, data['plan_id'])
    if updated_sub:
        return jsonify({
            'id': updated_sub.id,
            'user_id': updated_sub.user_id,
            'plan_id': updated_sub.plan_id
        })
    return jsonify({'message': 'Subscription not found'}), 404

  
@bp.route('/active', methods=['GET'])
def active_subscription():
    """
    Retrieve the active subscription for a user
    ---
    tags:
      - Subscriptions
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: Active subscription retrieved
        content:
          application/json:
            schema:
              type: object
              properties:
                subscription_id:
                  type: integer
                plan_id:
                  type: integer
                status:
                  type: string
                  example: active
                started_at:
                  type: string
                  format: date-time
                expires_at:
                  type: string
                  format: date-time
      404:
        description: No active subscription found
    """
    # user_id = request.args.get('user_id')
    user_id = get_jwt_identity()
    sub = SubscriptionService.get_active_subscription(user_id)
    if sub:
        return jsonify(dict(sub))
    return jsonify({"message": "No active subscription"}), 404

@bp.route('/', methods=['GET'])
def list_subscriptions():

    """
    List all subscriptions in the system (admin or diagnostic use)
    ---
    tags:
      - Subscriptions
    responses:
      200:
        description: List of subscriptions
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  subscription_id:
                    type: integer
                  user_id:
                    type: integer
                  plan_id:
                    type: integer
                  status:
                    type: string
                  started_at:
                    type: string
                    format: date-time
                  expires_at:
                    type: string
                    format: date-time
    """
    # user_id = request.args.get('user_id')
    user_id = get_jwt_identity()
    subs = SubscriptionService.list_subscriptions(user_id)
    return jsonify([dict(row) for row in subs])

@bp.route('/history', methods=['GET'])
def subscription_history():


    """
    Retrieve subscription history for a user
    ---
    tags:
      - Subscriptions
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: Subscription history retrieved
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  subscription_id:
                    type: integer
                  plan_id:
                    type: integer
                  status:
                    type: string
                  started_at:
                    type: string
                    format: date-time
                  expires_at:
                    type: string
                    format: date-time
    """
 
    user_id = get_jwt_identity()
    subs = SubscriptionService.get_subscription_history(user_id)
    return jsonify([dict(row) for row in subs])