from flask              import Flask, jsonify, request
from flask_pymongo      import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger           import Swagger, swag_from
from werkzeug.security  import generate_password_hash, check_password_hash
from dotenv             import load_dotenv
# from app.routes         import * # Importar rutas
import requests
import os

# Cargar variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

atlas_user     = os.getenv('MONGO_ATLAS_USER')
atlas_password = os.getenv('MONGO_ATLAS_PASSWORD')
jwt_secret     = os.getenv('JWT_SECRET_KEY')


# app.config["MONGO_URI"]    = "mongodb+srv://{atlas_user}:{atlas_password}@cluster0.stqtc4g.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGO_URI"]      = "mongodb+srv://{}:{}@cluster0.stqtc4g.mongodb.net/?retryWrites=true&w=majority".format(atlas_user, atlas_password)
app.config['JWT_SECRET_KEY'] = jwt_secret  

mongo = PyMongo(app)
jwt = JWTManager(app)
Swagger(app)

@app.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Registrar nuevo usuario',
    'parameters': [
        {
            'name': 'credentials',
            'in': 'body',
            'description': 'Credenciales nuevo usuario',
            'schema': {
                'type' : 'object',
                'properties' : {
                    'email' : {
                        'type' : 'string',
                        'format' : 'email',
                        'example' : 'user@yourdomain.com',
                    },
                    'password' : {
                        'type' : 'string',
                        'example' : 'yourpassword',
                    }
                },
                'required': ['email', 'password'],
            },
        },
    ],
    'responses': {
        201: {
            'description': 'Nuevo usuario registrado exitosamente',
            'schema': {
                'type' : 'object',
                'properties' : {
                    'message' : {
                        'type' : 'string',
                        'example' : 'Usuario registrado exitosamente',
                    }
                }
            },
        },
        409: {
            'description': 'Usuario ya existe',
        },
        400: {
            'description': 'Falta email o password',
        }
    },
})
def register():
    email    = request.json.get('email', None)
    password = request.json.get('password', None)
    if email and password:
        # Checar si el usuario ya existe
        if mongo.db.users.find_one({'email': email}):
            return jsonify(message='Usuario ya existe'), 409
        
        # Hashear la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            'email'    : email,
            'password' : hashed_password
        })
        return jsonify(message='Usuario registrado exitosamente'), 201
    else:
        return jsonify(message='Falta contraseña o correo'), 400


@app.route('/login', methods=['POST'])
def login():

    email    = request.json.get('email', None)
    password = request.json.get('password', None)
    user     = mongo.db.users.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200

    else:
        return jsonify(message='Usuario o contraseña incorrectos'), 401


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user            = mongo.db.users.find_one({'_id': current_user_id})

    if not user:
        return jsonify(message='Usuario no encontrado'), 404
    
    user_data = {
        'email': user['email'],
        # Incluir otras propiedades del perfil de usuario
    }

    return jsonify(user_data=user_data), 200


@app.route('/search', methods=['POST'])
def search():
    pokemon_name = request.args.get('name')
    if not pokemon_name:
        return jsonify(message='Proporcional el nombre de un pokemon'), 400
    
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if response.ok:
        return jsonify(pokemon_data=response.json()), 200
    else:
        return jsonify(message='Pokemon no encontrado'), 404

