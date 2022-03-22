import json
from flask import jsonify, request
from models import db, User

from bson.objectid import ObjectId


def users_route_handler():
    if request.method == 'GET':
        # users tarkoittaa collectionia / table
       users_list = User.get_all()
       return jsonify(users=User.list_to_json(users_list)) 
    elif request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        new_user = User(username)
        new_user.create()
        return jsonify(user=new_user.to_json())


def user_route_handler(_id):
    if request.method == 'GET':
        user = User.get_by_id(_id)
        return jsonify(user=user.to_json())
    elif request.method == 'DELETE':
        # user = User.get_by_id(_id)
        # user.delete()
        User.delete_by_id(_id)
        return ""
    elif request.method == 'PATCH':
        request_body = request.get_json()
        username = request_body['username']
        user = User.get_by_id(_id)
        user.username = username
        user.update()
        return jsonify(user=user.to_json())
