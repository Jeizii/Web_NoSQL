import json
from flask import jsonify, request
from models import db
# from mysql_models import User
from models import User
from flask_jwt_extended import jwt_required

#from bson.objectid import ObjectId

from validators.account import validate_account
users = []

# /api/users
# POST-ehtoon pääsee vaan admin

def users_handler():
    # jos request.method == 'GET' tarkoittaa,
    # että insomiasta/ postmanista on valittu GET-metodi
    if request.method == 'GET':
    #jsonify-funktio on osa flask pakettia
    #Se muuttaa python-objektin JSON-muotoon.
    #Lisäksi muuttaa HTTP-responsen content-type headerin application/jsoniksi
    # katsotaan tästä esimerkki insomialla.
        return jsonify(users=users)
    
    elif request.method == 'POST':
        req_body = request.get_json()
        new_user = {'_id': len(users) + 1, 'username': req_body['username']}
        users.append(new_user)
        return jsonify(user=new_user)
    

def users_route_handler():
    if request.method == 'GET':
        # users tarkoittaa collectionia / table
        # kun luokan funktio / metodi on @staticmethod
        # sitä kutsutaan käyttäen luokan nimeä (isolla kirjaimella) 
       users_list = User.get_all()
       return jsonify(users=User.list_to_json(users_list)) 
    elif request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        password  = request_body['password']
        role = request_body['role']
        new_user = User(username, password=password, role=role)
        # koska create ei ole @staticmethod
        # sille ei anneta argumenttina selfiä, vaikka
        # se createssa otetaankin ensimmäisenä vastaan
        # self viittaa create-funktion kutsun vasemmalla puolella
        # olevaan muuttujaan (new_user)
        new_user.create()
        return jsonify(user=new_user.to_json())


def user_route_handler(_id):
    if request.method == 'GET':
        user = User.get_by_id(_id)
        return jsonify(user=user.to_json())
    elif request.method == 'DELETE':
        user = User.get_by_id(_id)
        user.delete()
        #User.delete_by_id(_id)
        return ""
    elif request.method == 'PATCH':
        request_body = request.get_json()
        username = request_body['username']
        user = User.get_by_id(_id)
        user.username = username
        user.update()
        return jsonify(user=user.to_json())
