from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.subscription_service import SubscriptionService
from app.utils.logging_config import setup_logger, log_execution
 
from app.utils.swagger_docs import (
    create_subscription_doc,
    cancel_subscription_doc,
    upgrade_subscription_doc,
    active_subscription_doc,
    list_subscriptions_doc,
    subscription_history_doc,
)

logger = setup_logger("subscription", "logs/subscription.log")
bp = Blueprint('subscriptions', __name__, )


@bp.route('/', methods=['GET'])
@jwt_required()
@log_execution
@swag_from(list_subscriptions_doc)
def list_subscriptions():
    user_id = get_jwt_identity()
    logger.info("Listing subscriptions", extra={"user_id": user_id})
    subs = SubscriptionService.list_subscriptions(user_id)
    print(28, subs)
    return jsonify([
    {
        "id": row[0],
        "user_id": row[1],
        "created_at": row[2].isoformat() if row[2] else None,
        "ended_at": row[3].isoformat() if row[3] else None
    }
    for row in subs
])


@bp.route('/', methods=['POST'])
@jwt_required()
@log_execution
@swag_from(create_subscription_doc)
def subscribe(): 

    data = request.get_json()
    user_id = get_jwt_identity()
    print(38, user_id)
    logger.info("Creating subscription", extra={"user": f"user:{user_id}", "plan_id": data.get("plan_id")})
    sub = SubscriptionService.create_subscription(user_id, data['plan_id'])
    return jsonify({'id': sub.id, 'user_id': sub.user_id, 'plan_id': sub.plan_id})


@bp.route('/<int:subscription_id>/cancel', methods=['POST'])
@log_execution
@swag_from(cancel_subscription_doc)
def cancel(subscription_id):
    logger.info("Cancelling subscription", extra={"subscription_id": subscription_id})
    sub = SubscriptionService.cancel_subscription(subscription_id)
    if sub:
        return jsonify({'message': 'Subscription cancelled'})
    return jsonify({'message': 'Subscription not found'}), 404


@bp.route('/<int:subscription_id>', methods=['PUT'])
@log_execution
@swag_from(upgrade_subscription_doc)
def upgrade(subscription_id):
    data = request.get_json()
    logger.info("Upgrading subscription", extra={"subscription_id": subscription_id, "plan_id": data.get("plan_id")})
    updated_sub = SubscriptionService.update_subscription(subscription_id, data['plan_id'])
    if updated_sub:
        return jsonify({'id': updated_sub.id, 'user_id': updated_sub.user_id, 'plan_id': updated_sub.plan_id})
    return jsonify({'message': 'Subscription not found'}), 404


@bp.route('/active', methods=['GET'])
@jwt_required()
@log_execution
@swag_from(active_subscription_doc)
def active_subscription():
    user_id = get_jwt_identity()
    logger.info("Fetching active subscription", extra={"user_id": user_id})
    sub = SubscriptionService.get_active_subscription(user_id)
    if sub:
        return jsonify(dict(sub))
    return jsonify({"message": "No active subscription"}), 404




@bp.route('/history', methods=['GET'])
@jwt_required()
@log_execution
@swag_from(subscription_history_doc)
def subscription_history():
    user_id = get_jwt_identity()
    print(98, user_id)
    logger.info("Fetching subscription history", extra={"user_id": user_id})
    subs = SubscriptionService.get_subscription_history(user_id)
    return jsonify([
        {
            "id": row[0],
            "user_id": row[1],
            "created_at": row[2].isoformat() if row[2] else None,
            "ended_at": row[3].isoformat() if row[3] else None
        }
        for row in subs
    ])

 
