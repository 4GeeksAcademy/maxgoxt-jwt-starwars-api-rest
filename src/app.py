"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Personajes, Planetas, Favorito, Vehiculos, Usuario
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


    # endpoints INICIO





"""-----------------------------------------------_<Personajes>_-------------------------------------"""

@app.route('/personajes', methods=['GET'])
def handle_personajes():

    allpersonajes = Personajes.query.all()
    personajesList = list(map(lambda p: p.serialize(),allpersonajes))

    if personajesList == []:
        return { 'msj' : 'no hay personajes'}, 404

    return jsonify(personajesList), 200



@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def handle_personajes_id(personajes_id):

    onepersonaje = Personajes.query.filter_by(id=personajes_id).first() #peter = User.query.filter_by(username='peter').first()

    if onepersonaje is None:
        return { 'msj' : 'El personaje no existe, verifica el ID de la URL'}, 404

    return jsonify(onepersonaje.serialize()), 200



@app.route('/personajes', methods=['POST'])
def create_personaje():
    request_body = json.loads(request.data)

    existing_personaje = Personajes.query.filter_by(**request_body).first()

    if existing_personaje:
        return jsonify({"message": "El personaje ya existe"}), 400

    new_personaje = Personajes(**request_body)
    db.session.add(new_personaje)
    db.session.commit()
    
    return jsonify(new_personaje.serialize()), 200



"""-----------------------------------------------_<Personajes>_-------------------------------------"""

"""-----------------------------------------------_<Planetas>_-------------------------------------"""


@app.route('/planetas', methods=['GET'])
def handle_planetas():

    allplanetas = Planetas.query.all()
    planetasList = list(map(lambda p: p.serialize(),allplanetas))

    if planetasList == []:
        return { 'msj' : 'no hay planetas'}, 404

    return jsonify(planetasList), 200



@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def handle_planetas_id(planetas_id):

    oneplaneta = Personajes.query.filter_by(id=planetas_id).first() #peter = User.query.filter_by(username='peter').first()

    if oneplaneta is None:
        return { 'msj' : 'El planeta no existe, verifica el ID de la URL'}, 404

    return jsonify(oneplaneta.serialize()), 200


"""-----------------------------------------------_<Planetas>_-------------------------------------"""
"""-----------------------------------------------_<Usuario>_-------------------------------------"""

@app.route('/usuarios', methods=['GET'])
def handle_usuarios():

    allusuarios = Usuario.query.all()
    usuariosList = list(map(lambda p: p.serialize(),allusuarios))

    if usuariosList == []:
        return { 'msj' : 'no hay usuarios'}, 404

    return jsonify(usuariosList), 200



@app.route('/<usuarios>/favoritos', methods=['GET'])
def handle_favoritos(usuarios):

    allfavoritos = Favorito.query.all()
    favoritosList = list(map(lambda p: p.serialize(),allfavoritos))
    # print(favoritosList[0]['planetas_id'].serialize())
    # print(favoritosList[0]['usuario'].serialize())
    print(favoritosList[2])

    if favoritosList == []:
        return { 'msj' : 'no hay favoritos'}, 404

    return favoritosList #favoritosList.serialize(), 200





@app.route('/favoritos', methods=['GET'])
def handle_favs():

    allfavoritos = Favorito.query.all()
    favoritosList = list(map(lambda p: p.serialize(),allfavoritos))

    if favoritosList == []:
        return { 'msj' : 'no hay usuarios'}, 404

    return favoritosList, 200

"""-----------------------------------------------_<Usuario>_-------------------------------------"""





    # endpoints FINAL

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
