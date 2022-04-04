from flask import request

from models import User




def login_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        user = User.get_by_username(username)
        print(user)
        return ""