
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from models import Publication

@jwt_required(optional=True)
def publications_route_handler():
    logged_in_user = get_jwt()
    if request.method == 'GET':
        if logged_in_user: # jos on kirjauduttu sisään
            if logged_in_user['role'] == 'admin':
                publications = Publication.get_all()
            elif logged_in_user['role'] == 'user':
                # haetaan kaikki omat + ne joissa visibility = 1 tai 2
                publications = Publication.get_by_owner_and_visibility(user=logged_in_user, visibility=[1,2])
        # print("########## publications", publications)

        publications_in_json_format = Publication.list_to_json(publications)
        return jsonify(publications=publications_in_json_format)
        
    elif request.method == 'POST':
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url']
        new_publication = Publication(title, description, url)
        new_publication.create()
        
        return jsonify(publication=new_publication.to_json())