# app/routes/user.py
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException
from app.services.user_service import UserService
from flask_jwt_extended import JWTManager, create_access_token

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
            required:
              - email
              - password
    responses:
      200:
        description: User registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
      400:
        description: Bad Request
    """
    try:
        data = request.get_json()
        user = UserService.register(data['email'], data['password'])
        return jsonify({'id': user.id, 'email': user.email})
    except HTTPException as e:
        return jsonify({'message': e.description}), e.code

@bp.route('/login', methods=['POST'])
def login():
    """
    Login a user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
            required:
              - email
              - password
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                user_id:
                  type: integer
      401:
        description: Unauthorized
    """
    try:
        data = request.get_json()
        user = UserService.login(data['email'], data['password'])
        if user and user.password == data["password"]:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        return jsonify({"msg": "Bad credentials"}), 401
        # return jsonify({'message': 'Login successful', 'user_id': user.id})
    except HTTPException as e:
        return jsonify({'message': e.description}), e.code
