from src                               import csrf, jwt_required, get_jwt_identity
from src.controllers.UserController    import UserController
from src.controllers.PokemonController import PokemonController
from flask                             import Blueprint, request, Response
from flasgger                          import Swagger, swag_from
import json

users_bp = Blueprint('user', __name__)
userController = UserController()

@users_bp.route('/register', methods=['POST'])
@csrf.exempt
@swag_from('docs\\api\\register.yaml')
def register():
    try:
        user_data = request.get_json()
        return userController.register(user_data)
    except ValueError as e:
        return Response(json.dumps({"message": "Incorrect data."}), status=400, mimetype='application/json')
    except KeyError as e:
        return Response(json.dumps({"message": "Incorrect data."}), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": "Server error", "error" : e}), mimetype='application/json'), 500

@users_bp.route('/login', methods=['POST'])
@csrf.exempt
@swag_from('docs\\api\\login.yaml')
def login():
    try:
        user_data = request.get_json()
        if 'email' in user_data and 'password' in user_data:
            return userController.login(user_data)
        else:
            return Response(json.dumps({'message': 'Missing email or password'}), mimetype='application/json'), 400
    except ValueError as e:
        return Response(json.dumps({"message": "Incorrect data."}), status=400, mimetype='application/json')
    except KeyError as e:
        return Response(json.dumps({"message": "Incorrect data."}), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": "Login failed"}), mimetype='application/json'), 500


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
@swag_from('docs\\api\\profile.yaml')
def profile():
    return userController.profile()


@users_bp.route('/search', methods=['POST'])
@jwt_required()
@swag_from('docs\\api\\search.yaml')
def search():
    pokemon_data = request.get_json()
    resp = pokemonController.search(pokemon_data)
    return resp


@users_bp.route('/catch', methods=['POST'])
@jwt_required()
@swag_from('docs\\api\\catch.yaml')
def catch():
    pokemon_data = request.get_json()
    resp = userController.catch(pokemon_data)
    return resp
    