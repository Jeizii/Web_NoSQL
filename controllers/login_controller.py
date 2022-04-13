from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token
from errors.not_found import NotFound
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from models import User



# /api/login
@jwt_required(refresh=True)
#jorma = 'jorma'
def login_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user = User.get_by_username(username)
        password_ok = sha256.verify(password, user.password)
        if password_ok is True:
            access_token = create_access_token(
                str(user._id), 
                additional_claims={'username': user.username, 'role': user.role})
            
            return jsonify(access_token=access_token)
        raise NotFound(message='User not found')
    
    

""" class LoginRouteHandler(MethodView):
    def post(self):
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user = User.get_by_username(username)
        password_ok = sha256.verify(password, user.password)
        if password_ok is True:
            access_token = create_access_token(
                str(user._id), 
                additional_claims={'username': user.username, 'role': user.role})
            
            return jsonify(access_token=access_token)
        raise NotFound(message='User not found')
    
    @jwt_required(refresh=True)
    def patch(self):
        pass """

        
        