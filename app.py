# tässä on MCV: osa C eli controller

from flask import Flask, jsonify, make_response
from controllers.account_controller import AccountRouteHandler, account_password_route_handler
from controllers.login_controller import login_route_handler
from controllers.publications_controller import like_publication_route_handler, publication_route_handler, publications_route_handler, share_publication_route_handler
from controllers.register_controller import register_route_handler

from controllers.users_controller import user_route_handler, users_route_handler
from flask_jwt_extended import JWTManager

from errors.not_found import NotFound
from errors.validation_error import ValidationError



# Flask(__name__) merkitys selviää, kun päästään luokkiin asti
app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

@app.route('/hello_world')
def hello_world_route_handler():
    response = make_response ('Moi moi taa on sun eka appis')
    return response

@app.route('/another_route')
def another_route_route_handler():
    response = make_response('Moi taa on sun toka sivu')
    return response


@app.errorhandler(NotFound)
def handle_not_found(err):
    return jsonify(err=err.args), 404


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(err=err.args), 400

app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/<_id>', view_func=user_route_handler, methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/api/register', view_func=register_route_handler, methods=['POST'])
app.add_url_rule('/api/login', view_func=login_route_handler, 
methods=['POST'])

app.add_url_rule('/api/account', view_func=AccountRouteHandler.as_view('account_route_handler'))
app.add_url_rule('/api/account/password', 
view_func=account_password_route_handler, methods=['PATCH'])
app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/publications/<_id>', view_func=publication_route_handler, methods=['GET', 'DELETE'])
app.add_url_rule('/api/publications/<_id>/like', view_func=like_publication_route_handler, methods=['PATCH'])
app.add_url_rule('/api/publications/<_id>/share', view_func=share_publication_route_handler, methods=['PATCH'])



# __name__-muuttujan arvo riippuu siitä, miten app.py suoritetaan
# kun app.py suoritetaan python app.py kommennolla, __name__-muuttujan arvo on __main__
# kun app.py importataan, sen nimeksi tulee app, eli skriptin nimi

# jos ao. ehtoa ei olisi, flask web-serveri käynnistyisi aina, kun app.py importataan toiseen
# tiedostoon

# se, mitä @-merkki tekee, selviää myöhemmin
if __name__ == '__main__':
    # kun debug-muuttujan arvo on True, palvelin käynnistyy aina itsestään uudelleen
    # kun koodi muuttuu. Tämä on kätevää kehitysvaiheessa
    app.run(debug=True)
    

