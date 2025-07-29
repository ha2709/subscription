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
bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')


@bp.route('/', methods=['GET'])
@jwt_required()
@log_execution
@swag_from(list_subscriptions_doc)
def list_subscriptions():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    subscriptions = SubscriptionService.list_all_subscriptions(user_id, page, page_size)
    total = SubscriptionService.count_subscriptions(user_id)

    logger.info("Fetching active subscription", extra={"user_id": user_id})
     
    return jsonify({
        'subscriptions': [dict(row) for row in subscriptions],
        'total': total,
        'page': page,
        'page_size': page_size
    })



@bp.route('/', methods=['POST'])
@jwt_required()
@log_execution
@swag_from(create_subscription_doc)
def subscribe(): 

    data = request.get_json()
    user_id = get_jwt_identity()
   
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
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    active_subs = SubscriptionService.get_active_subscriptions(user_id, page, page_size)
    total = SubscriptionService.count_active_subscriptions(user_id)

    return jsonify({
        'active_subscriptions': [dict(row) for row in active_subs],
        'total': total,
        'page': page,
        'page_size': page_size
    })
    

@bp.route('/history', methods=['GET'])
@jwt_required()
@log_execution
@swag_from(subscription_history_doc)
def subscription_history():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    history = SubscriptionService.get_subscription_history(user_id, page, page_size)
    total = SubscriptionService.count_subscription_history(user_id)

    return jsonify({
        'history': [dict(row) for row in history],
        'total': total,
        'page': page,
        'page_size': page_size
    })

 
