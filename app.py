# tässä on MCV: osa C eli controller

from flask import Flask
from controllers.publications_controller import publications_route_handler

from controllers.users_controller import user_route_handler, users_route_handler



# Flask(__name__) merkitys selviää, kun päästään luokkiin asti
app = Flask(__name__)

app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/<_id>', view_func=user_route_handler, methods=['GET', 'DELETE', 'PATCH'])

app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])



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
    

