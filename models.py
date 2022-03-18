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