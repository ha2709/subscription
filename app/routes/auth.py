from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException
from app.services.user_service import UserService
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import swag_from
from app.utils.swagger_docs import register_user_doc,login_user_doc

 

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/register', methods=['POST'])
@swag_from(register_user_doc)
def register():
    
    try:
        data = request.get_json()
        user = UserService.register(data['email'], data['password'])
        return jsonify({'id': user.id, 'email': user.email})
    except HTTPException as e:
        return jsonify({'message': e.description}), e.code
@bp.route('/login', methods=['POST'])
@swag_from(login_user_doc)
 
def login():
  
    try:
        data = request.get_json()
        user = UserService.login(data['email'], data['password'])
        if user and user.check_password(data["password"]):
          # Successful login
          
          access_token = create_access_token(identity=str(user.id))
          return jsonify(access_token=access_token), 200
          # return jsonify({"message": "Login successful", "user_id": user.id}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
 
   
        return jsonify({"msg": "Bad credentials"}), 401
        # return jsonify({'message': 'Login successful', 'user_id': user.id})
    except HTTPException as e:
        return jsonify({'message': e.description}), e.code
