from flask import Flask, jsonify, request
import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# tätä voi käyttää, jos on paikallinen mongodb-palvelin asennettuna
# mongodb://localhost:27017/

client = pymongo.MongoClient("mongodb+srv://web_nosql_db:a1XiUzqY9kHqxOed@cluster0.rr8t2.mongodb.net/?retryWrites=true&w=majority", 
server_api=ServerApi('1'))
# db nimi voi olla muukin kuin group1
db = client.group1

# jokaiselle MongoDB:n collectionille / esim. MySQL tablelle
# tehdään luokka (tämä luokka on ns. model-luokka)
# jokainen model-luokka sisältää samat tiedot, kuin tietokannan 
# collection / table (esim. username)

# model-luokkaan kuuluu CRUD:n toiminallisuudet, joista jokainen
# on model-luokan funktio / metodi

# CRUD
# C => create()
# R => get_all() ja get_by_id()
# U => update()
# D => delete()

# mitä hyötyä modelista sitten on, 
# jos CRUD:n voi tehdä suoraan controlleriinkin?

# koska Separation of Concerns
# Käytännössä Separation of Corncerns tarkoittaa tässä sitä, että 
# controllerin tehtävä on huolehtia route_handlereista, 
# eikä tietokantahauista

class User:
    def __init__(self, username, _id=None):
        self.username = username
        
        if _id is not None:
            _id = str(_id)
        self._id = _id
    
    # CRUD:n U
    def update(self):
        db.users.update_one(
            {'_id': ObjectId(self._id)}, {
            '$set': {'username': self.username}
        })
    # kun classin funktio / metodi ei ole @staticmethod
    # sen ensimmäinen argumentti on self
    # selfin kautta pääsee kaikkiin luokan muuttujiin käsiksi
    # self.username
    def create(self):
        result = db.users.insert_one({'username': self.username})
        self._id = str(result.inserted_id)
    
    @staticmethod
    def create_user(username):
        result = db.users.insert_one({'username': username})
        return User(username, _id=result.inserted_id)
        
    # CRUD:n R (kaikki käyttäjät)
    @staticmethod
    def get_all():
        
        users = []
        users_cursor = db.users.find()
        for user in users_cursor:
            users.append(User(user['username'], _id=str(user['_id'])))
        return users
    
    # CRUD:n D (staattisella metodilla)
    @staticmethod
    def delete_by_id(_id):
        db.users.delete_one({'_id': ObjectId(_id)})

    #CRUD:n R (yksi käyttäjä _id:llä haettuna)
    @staticmethod
    def get_by_id(_id):
        user = db.users.find_one({'_id': ObjectId(_id)})
        return User(user['username'], _id=str(user['_id']))
    
    # CRUD:n D (Delete, eli yksittäisen käyttäjän poisto)
    def delete(self):
        db.users.delete_one({'_id': ObjectId(self._id)})

    
    @staticmethod
    def list_to_json(user_list):
        json_list = []
        for user in user_list:
            user_in_json_format = user.to_json()
            json_list.append(user_in_json_format)
        return json_list
    
    def to_json(self):
        user_in_json_format = {
            '_id': str(self._id),
            'username': self.username
        }
        return user_in_json_format
    
    









