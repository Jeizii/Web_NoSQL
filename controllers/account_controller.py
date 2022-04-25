from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from errors.not_found import NotFound
from errors.validation_error import ValidationError
from models import User
from validators.account import validate_account
from passlib.hash import pbkdf2_sha256 as sha256

# /api/account/password
@jwt_required()
def account_password_route_handler():
    user_id = get_jwt()['sub']
    request_body = request.get_json()
    if request_body:
        if 'password' in request_body:
            account = User.get_by_id(user_id)
            # 3 päivitä löydetyn käyttäjän (account eli oma käyttäjätili) password sillä, joka on request_bodyssa
            account.password = sha256.hash(request_body['password'])
            # 4 kutsu päivityksen jälkeen update-metodia
            account.update()
            # 5 palauta päivitetty user (account eli oma tili) jsonifylla
            return jsonify(account=account.to_json())
        raise ValidationError(message='password is required')
    raise ValidationError(message='request body is required')

# /api/account
class AccountRouteHandler(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt()['sub']
        account = User.get_by_id(user_id)
        return jsonify(account=account.to_json())
    
    @jwt_required()
    def patch(self):
        
        # 1 ota request_body vastaan
        request_body = request.get_json()
        if request_body:
            if 'username' in request_body:

                # 2 hae käyttäjä jwt:n subilla katso mallia getistä
                user_id = get_jwt()['sub']
                account = User.get_by_id(user_id)
                # 3 päivitä löydetyn käyttäjän (account eli oma käyttäjätili) username sillä, joka on request_bodyssa
                account.username = request_body['username']
                # 4 kutsu päivityksen jälkeen update-metodia
                account.update()
                # 5 palauta päivitetty user (account eli oma tili) jsonifylla
                return jsonify(account=account.to_json())
            raise ValidationError(message='username is required')
        raise ValidationError(message='body is required')
            
            

