from flask import jsonify, request
from models import db
from bson.objectid import ObjectId


def users_route_handler():
    if request.method == 'GET':
        # users tarkoittaa collectionia / table
       users_cursor = db.users.find()
       users_list = list(users_cursor)
       for user in users_list:
           user['_id'] = str(user['_id'])
       return jsonify(users=users_list) 
    elif request.method == 'POST':
        request_body = request.get_json()
        new_user = {'username': request_body['username']}
        result = db.users.insert_one(new_user)
        return ""


def user_route_handler(_id):
    if request.method == 'GET':
        user = db.users.find_one({'_id': ObjectId(_id)})
        user['_id'] = str(user['_id'])
        return jsonify(user=user)
    elif request.method == 'DELETE':
        db.users.delete_one({'_id': ObjectId(_id)})
        return ""
    elif request.method == 'PATCH':
        request_body = request.get_json()
        username = request_body['username']
        db.users.update_one({'_id': ObjectId(_id)},
        {'$set': {'username': username}})
        return ""