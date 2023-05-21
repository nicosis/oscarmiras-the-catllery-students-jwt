"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Cat
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


api = Blueprint('api', __name__)


@api.route("/signup", methods=["POST"])
def sign_up():
    # Ejercicio 2. Completar! Debemos obtener el usuario y password del cuerpo del a petición POST. Luego, añadir el usuario a la base de datos. Puedes comprobar si se ha creado bien el usuario en la pantalla de administración de Flask, o haciendo una consulta a la tabla User

    request_body_user = request.get_json()
    new_user = User(
        email=request_body_user['email'], password=request_body_user['password'])
    db.session.add(new_user)
    db.session.commit()

    # BONUS: ¿Cómo gestionamos si el usuario ha puesto un email ya presente en la tabla User?

    # Este return debe cambiarse adecuadamente para devolver un mensaje de OK cuando el usuario se haya creado
    return jsonify('user added:', request_body_user), 200
    # return jsonify({"msg": "Not implemented"}), 501


@api.route('/login', methods=['POST'])
def login():
    # Obtener los datos del usuario desde el cliente
    body = request.get_json()
    email = body['email']
    password = body['password']

    # Existe el usuario en la base de datos?
    user = User.query.filter_by(email=email, password=password).first()

    # si no existe, devuelve un mensaje de error y el código 401
    if user == None:
        return jsonify({"msg": "User or password, Not exist!"}), 401

    # Flask crea un nuevo token JWT. Se lo guarda en su base de datos y lo asocia al usuario que hemos recuperado de la base de datos
    access_token = create_access_token(identity=user.serialize())

    # Devolvemos el token (string) al cliente para que en futuras peticiones a nuestros endpoints protegidos se pueda autentificar
    # (cebolla_patata_queso)
    response_body = {
        "msg": "Token create successfully",
        "token": access_token,
        "email": email
    }

    return jsonify(response_body), 200


@api.route("/cat", methods=["POST"])
@jwt_required()
def post_cat():
    current_user = get_jwt_identity()

    # Obtén los datos del gato del cuerpo de la solicitud
    data = request.json
    print(data)
    name = data.get("name")
    image_url = data.get("imageUrl")

    # Verifica si se proporcionaron los datos del gato
    if not name or not image_url:
        return jsonify({"error": "Nombre e imagen del gato son obligatorios"}), 400

    # Crea un nuevo objeto Cat relacionado con el usuario actual
    cat = Cat(name=name, image_url=image_url, user_id=current_user['id'])

    # Guarda el nuevo gato en la base de datos
    db.session.add(cat)
    db.session.commit()

    return jsonify({"msg": "Gato agregado exitosamente"}), 200


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/cats", methods=["GET"])
@jwt_required()
def get_user_cats():

    # Obtengo el usuario al que pertenece el token JWT
    current_user = get_jwt_identity()

    # ID de usuario
    curre_user_id = current_user['id']

    # Crea una lista para almacenar los datos de los gatos
    cats_data = []

    # Ejercicio 5: COMPLETAR

    cats = Cat.query.filter(Cat.user_id == curre_user_id).all()
    for cat in cats:
            cat_data = {
                'id': cat.id,
                'name': cat.name,
                'image_url': cat.image_url,
            }
            cats_data.append(cat_data)
    

    # Busca todos los gatos asociados al usuario actual y añádelos a cats_data

    print(cats_data)
    return jsonify(cats_data), 200
