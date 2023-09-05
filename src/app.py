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
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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
        return jsonify({'msj' : 'no hay personajes'}), 404

    return jsonify(personajesList), 200



@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def handle_personajes_id(personaje_id):

    onepersonaje = Personajes.query.filter_by(id=personaje_id).first()

    if onepersonaje is None:
        return jsonify({'msj' : 'El personaje no existe'}), 404

    return jsonify(onepersonaje.serialize()), 200



@app.route('/personaje', methods=['POST'])
def create_personaje():
    request_body = json.loads(request.data)

    existing_personaje = Personajes.query.filter_by(name=request_body["name"]).first()

    if existing_personaje:
        return jsonify({"msj": "El personaje ya existe"}), 404

    new_personaje = Personajes(
        name= request_body['name'],
        mass= request_body['mass'],
        hair_color= request_body['hair_color'],
        skin_color= request_body['skin_color'],
        eye_color= request_body['eye_color'],
        birth_year= request_body['birth_year'],
        gender= request_body['gender'],
        height= request_body['height']
        )
    db.session.add(new_personaje)
    db.session.commit()
    return jsonify(new_personaje.serialize()), 200



@app.route('/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):

    existing_personaje = Personajes.query.filter_by(id=personaje_id).first()

    if existing_personaje:
        db.session.delete(existing_personaje)
        db.session.commit()
        return jsonify({"msj": "El personaje ha sido eliminado"}), 200

    return jsonify({"msj": "El personaje que intenta eliminar no existe"}), 404



@app.route('/favorito/<int:usuario_id>/personaje/<int:personajes_id>', methods=['POST'])
def create_fav_personaje(usuario_id, personajes_id):

    existing_favorito = Favorito.query.filter_by(personajes_id=personajes_id, usuario_id=usuario_id).first()

    if existing_favorito:
        return jsonify({"msj": "El personaje ya está en favoritos"}), 404
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario al que le quiere añadir un favoritos no existe"}), 404
    
    elif not Personajes.query.filter_by(id=personajes_id).first():
        return jsonify({"msj": "El personaje que quiere añadir a favoritos no existe"}), 404
    
    new_favorito = Favorito(
        usuario_id= usuario_id,
        personajes_id= personajes_id,
        vehiculos_id= None,
        planetas_id= None
    )
    db.session.add(new_favorito)
    db.session.commit()
    
    return jsonify(new_favorito.serialize()), 200



@app.route('/favorito/<int:usuario_id>/personaje/<int:personajes_id>', methods=['DELETE'])
def delete_fav_personaje(usuario_id, personajes_id):

    existing_favorito = Favorito.query.filter_by(personajes_id=personajes_id, usuario_id=usuario_id).first()
    if existing_favorito:
        db.session.delete(existing_favorito)
        db.session.commit()
        return jsonify({"msj": "El personaje ha sido eliminado de favoritos"}), 200
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario no existe"}), 404
    
    elif not Personajes.query.filter_by(id=personajes_id).first():
        return jsonify({"msj": "El personaje que quiere eliminar de favoritos no existe"}), 404
    
    return jsonify({"msj": "El personaje no está en los favoritos"}), 404


"""-----------------------------------------------_<Personajes>_-------------------------------------"""

"""-----------------------------------------------_<Planetas>_-------------------------------------"""


@app.route('/planetas', methods=['GET'])
def handle_planetas():

    allplanetas = Planetas.query.all()
    planetasList = list(map(lambda p: p.serialize(),allplanetas))

    if planetasList == []:
        return jsonify({'msj' : 'no hay planetas'}), 404

    return jsonify(planetasList), 200



@app.route('/planeta/<int:planeta_id>', methods=['GET'])
def handle_planeta_id(planeta_id):

    oneplaneta = Planetas.query.filter_by(id=planeta_id).first()

    if oneplaneta is None:
        return jsonify({'msj' : 'El planeta no existe'}), 404

    return jsonify(oneplaneta.serialize()), 200



@app.route('/planeta', methods=['POST'])
def create_planeta():
    request_body = json.loads(request.data)

    existing_planeta = Planetas.query.filter_by(name=request_body["name"]).first()

    if existing_planeta:
        return jsonify({"msj": "El planeta ya existe"}), 404

    new_planeta = Planetas(
        name=request_body['name'],
        diameter=request_body['diameter'],
        rotation_period=request_body['rotation_period'],
        orbital_period=request_body['orbital_period'],
        gravity=request_body['gravity'],
        population=request_body['population'],
        climate=request_body['climate'],
        terrain=request_body['terrain'],
        surface_water=request_body['surface_water']
        )
    db.session.add(new_planeta)
    db.session.commit()
    return jsonify(new_planeta.serialize()), 200



@app.route('/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_planeta(planeta_id):

    existing_planeta = Planetas.query.filter_by(id=planeta_id).first()

    if existing_planeta:
        db.session.delete(existing_planeta)
        db.session.commit()
        return jsonify({"msj": "El planeta ha sido eliminado"}), 200

    return jsonify({"msj": "El planeta que intenta eliminar no existe"}), 404



@app.route('/favorito/<int:usuario_id>/planeta/<int:planetas_id>', methods=['POST'])
def create_fav_planeta(usuario_id, planetas_id):

    existing_favorito = Favorito.query.filter_by(planetas_id=planetas_id, usuario_id=usuario_id).first()

    if existing_favorito:
        return jsonify({"msj": "El planeta ya está en favoritos"}), 404
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario al que le quiere añadir un favoritos no existe"}), 404
    
    elif not Planetas.query.filter_by(id=planetas_id).first():
        return jsonify({"msj": "El planeta que quiere añadir a favoritos no existe"}), 404

    new_favorito = Favorito(
        usuario_id= usuario_id,
        personajes_id= None,
        vehiculos_id= None,
        planetas_id= planetas_id
    )
    db.session.add(new_favorito)
    db.session.commit()
    
    return jsonify(new_favorito.serialize()), 200



@app.route('/favorito/<int:usuario_id>/planeta/<int:planetas_id>', methods=['DELETE'])
def delete_fav_planeta(usuario_id, planetas_id):

    existing_favorito = Favorito.query.filter_by(planetas_id=planetas_id, usuario_id=usuario_id).first()

    if existing_favorito:
        db.session.delete(existing_favorito)
        db.session.commit()
        return jsonify({"msj": "El planeta ha sido eliminado de favoritos"}), 200
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario no existe"}), 404
    
    elif not Planetas.query.filter_by(id=planetas_id).first():
        return jsonify({"msj": "El planeta que quiere eliminar de favoritos no existe"}), 404
    
    return jsonify({"msj": "El planeta no está en favoritos"}), 404

"""-----------------------------------------------_<Planetas>_-------------------------------------"""

"""-----------------------------------------------_<Vehiculos>_-------------------------------------"""


@app.route('/vehiculos', methods=['GET'])
def handle_vehiculos():

    allvehiculos = Vehiculos.query.all()
    vehiculosList = list(map(lambda p: p.serialize(),allvehiculos))

    if vehiculosList == []:
        return jsonify({'msj' : 'no hay vehiculos'}), 404

    return jsonify(vehiculosList), 200



@app.route('/vehiculo/<int:vehiculo_id>', methods=['GET'])
def handle_vehiculo_id(vehiculo_id):

    onevehiculo = Vehiculos.query.filter_by(id=vehiculo_id).first()

    if onevehiculo is None:
        return jsonify({'msj' : 'El vehiculo no existe'}), 404

    return jsonify(onevehiculo.serialize()), 200



@app.route('/vehiculo', methods=['POST'])
def create_vehiculo():
    request_body = json.loads(request.data)

    existing_vehiculo = Vehiculos.query.filter_by(name=request_body["name"]).first()

    if existing_vehiculo:
        return jsonify({"msj": "El vehiculo ya existe"}), 404

    new_vehiculo = Vehiculos(
        name=request_body['name'],
        model=request_body['model'],
        vehicle_class=request_body['vehicle_class'],
        manufacturer=request_body['manufacturer'],
        cost_in_credits=request_body['cost_in_credits'],
        length=request_body['length'],
        crew=request_body['crew'],
        passengers=request_body['passengers'],
        max_atmosphering_speed=request_body['max_atmosphering_speed'],
        cargo_capacity=request_body['cargo_capacity'],
        consumables=request_body['consumables'],
        films=request_body['films'],
        pilots=request_body['pilots']
        )
    db.session.add(new_vehiculo)
    db.session.commit()
    return jsonify(new_vehiculo.serialize()), 200



@app.route('/vehiculo/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo(vehiculo_id):

    existing_vehiculo = Vehiculos.query.filter_by(id=vehiculo_id).first()

    if existing_vehiculo:
        db.session.delete(existing_vehiculo)
        db.session.commit()
        return jsonify({"msj": "El vehiculo ha sido eliminado"}), 200

    return jsonify({"msj": "El vehiculo que intenta eliminar no existe"}), 404



@app.route('/favorito/<int:usuario_id>/vehiculo/<int:vehiculos_id>', methods=['POST'])
def create_fav_vehiculo(usuario_id, vehiculos_id):

    existing_favorito = Favorito.query.filter_by(vehiculos_id=vehiculos_id, usuario_id=usuario_id).first()

    if existing_favorito:
        return jsonify({"msj": "El vehiculo ya está en favoritos"}), 404
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario al que le quiere añadir un favoritos no existe"}), 404
    
    elif not Vehiculos.query.filter_by(id=vehiculos_id).first():
        return jsonify({"msj": "El vehiculo que quiere añadir a favoritos no existe"}), 404
    
    new_favorito = Favorito(
        usuario_id= usuario_id,
        personajes_id= None,
        vehiculos_id= vehiculos_id,
        planetas_id= None
    )
    db.session.add(new_favorito)
    db.session.commit()
    
    return jsonify(new_favorito.serialize()), 200



@app.route('/favorito/<int:usuario_id>/vehiculo/<int:vehiculos_id>', methods=['DELETE'])
def delete_fav_vehiculo(usuario_id, vehiculos_id):

    existing_favorito = Favorito.query.filter_by(vehiculos_id=vehiculos_id, usuario_id=usuario_id).first()

    if existing_favorito:
        db.session.delete(existing_favorito)
        db.session.commit()
        return jsonify({"msj": "El vehiculo ha sido eliminado de favoritos"}), 200
    
    elif not Usuario.query.filter_by(id=usuario_id).first():
        return jsonify({"msj": "El usuario no existe"}), 404
    
    elif not Vehiculos.query.filter_by(id=vehiculos_id).first():
        return jsonify({"msj": "El vehiculo que quiere eliminar de favoritos no existe"}), 404
    
    return jsonify({"msj": "El vehiculo ya está en favoritos"}), 404

"""-----------------------------------------------_<Vehiculos>_-------------------------------------"""


"""-----------------------------------------------_<Usuario>_-------------------------------------"""

@app.route('/usuarios', methods=['GET'])
def handle_usuarios():

    allusuarios = Usuario.query.all()
    usuariosList = list(map(lambda p: p.serialize(),allusuarios))

    if usuariosList == []:
        return jsonify({'msj' : 'no hay usuarios'}), 404

    return jsonify(usuariosList), 200



@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def handle_usuario_id(usuario_id):

    oneusuario = Usuario.query.filter_by(id=usuario_id).first()

    if oneusuario is None:
        return jsonify({'msj' : 'El usuario no existe'}), 404

    return jsonify(oneusuario.serialize()), 200



@app.route('/<int:usuario_id>/favoritos', methods=['GET'])
def handle_favoritos(usuario_id):

    allfavoritos = Favorito.query.filter_by(usuario_id=usuario_id).all()
    favoritosList = list(map(lambda p: p.serialize(),allfavoritos))

    if favoritosList == []:
        return { 'msj' : 'no hay favoritos'}, 404

    return jsonify({'results' : favoritosList}),200



@app.route('/favoritos', methods=['GET'])
def handle_favs():

    allfavoritos = Favorito.query.all()
    favoritosList = list(map(lambda p: p.serialize(),allfavoritos))

    if favoritosList == []:
        return jsonify({'msj' : 'no hay usuarios'}), 404

    return favoritosList, 200

"""-----------------------------------------------_<Usuario>_-------------------------------------"""

"""-----------------------------------------------_<SingUp>_-------------------------------------"""



@app.route('/signup', methods=['POST'])
def signup():
    request_body = json.loads(request.data)

    existing_usuario = Usuario.query.filter_by(email=request_body["email"]).first()

    if existing_usuario:
        return jsonify({"msj": "El usuario ya existe"}), 404

    new_usuario = Usuario(
        nombre=request_body["nombre"],
        apellido=request_body["apellido"],
        email=request_body["email"],
        password=request_body["password"]
        )
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify(new_usuario.serialize()), 200



"""-----------------------------------------------_<SingUp>_-------------------------------------"""

"""-----------------------------------------------_<Login>_-------------------------------------"""


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    usuario_query = Usuario.query.filter_by(email=email).first()

    if usuario_query is None:
        return jsonify({"msj": "No se econtró una cuenta vinculada al email dado"}), 404

    elif email != usuario_query.serialize()['email'] or password != usuario_query.serialize()['password']:
        return jsonify({"msj": "Contraseña incorrecta"}), 404

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


"""-----------------------------------------------_<Login>_-------------------------------------"""

"""-----------------------------------------------_<Perfil>_-------------------------------------"""


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



@app.route("/valid-token", methods=["GET"])
@jwt_required()
def valid_token():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify({ 'is_logged' : True}), 200


"""-----------------------------------------------_<Perfil>_-------------------------------------"""





    # endpoints FINAL

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msj": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
