
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from errors.not_found import NotFound

from models import Publication

@jwt_required(optional=True)
def publication_route_handler(_id):
    logged_in_user = get_jwt()
    if request.method == 'GET':
        publication = Publication.get_by_id(_id)
        return jsonify(publication=publication.to_json())
    elif request.method == 'DELETE':
        publication = Publication.get_by_id(_id)
        if logged_in_user: # onko käyttäjä kirjautunut sisään 
            # (löytyy authorization header ja jwt on typea access ja on voimassa)
            if logged_in_user['role'] == 'admin': # admin voi poistaa kaikki riippumatta omistajasta
                pass
            elif logged_in_user['role'] == 'user':
                # tarkistetaan, että käyttäjän _id (logged_in_user['sub']) 
                # on sama kuin publication.owner
                if publication.owner is not None and str(publication.owner) == logged_in_user['sub']:
                    publication.delete()
                raise NotFound(message='Publication not found')
        raise NotFound(message='Publication not found')

@jwt_required()
def share_publication_route_handler(_id):
    publication = Publication.get_by_id(_id)
    publication.share()
    return jsonify(publication=publication.to_json())


@jwt_required()
def like_publication_route_handler(_id):
    if request.method == 'PATCH':
        logged_in_user = get_jwt()
        found_index = -1 # jos found_index = -1, niin käyttäjää ei ole likes listassa
        publication = Publication.get_by_id(_id)
        for count, user_id in enumerate(publication.likes):
            if str(user_id) == logged_in_user['sub']: # jos sisäänkirjautuneen käyttäjän 
                # _id on listassa
                found_index = count # found_index sisältää nyt sisäänkirjautuneen käyttäjän indexin
                # likes listassa
                break
        if found_index > -1: # jos käyttäjän id on likes listassa, se poistetaan siitä
            del publication.likes[found_index]
        else: # jos käyttäjän id ei ole vielä listassa, se lisätään sinne
            publication.likes.append(ObjectId(logged_in_user['sub']))

        publication.like() # tallennetaan uusi likes lista tietokantaan
        return jsonify(publication=publication.to_json()) 






       
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
        
        else: # käyttäjä ei ole kirjautunut sisään
            publications = Publication.get_by_visibility(visibility=2)

        publications_in_json_format = Publication.list_to_json(publications)
        return jsonify(publications=publications_in_json_format)
        
    elif request.method == 'POST':
        owner = None
        if logged_in_user:
            owner = ObjectId(logged_in_user['sub'])
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        visibility = request_body.get('visibility', 2)
        url = request_body['url']
        new_publication = Publication(title, description, url, visibility=visibility, owner=ObjectId(owner))
        new_publication.create()
        
        return jsonify(publication=new_publication.to_json())