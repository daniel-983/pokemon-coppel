from src                               import csrf
from flask                             import Blueprint, request, Response
from flask_jwt_extended                import jwt_required, get_jwt_identity
from src.controllers.PokemonController import PokemonController
from flasgger                          import Swagger, swag_from

pokemons_bp = Blueprint('pokemons_bp', __name__)

pokemonController = PokemonController()

@pokemons_bp.route('/pokemon/<int:id>', methods=['GET'])
@csrf.exempt
@jwt_required()
@swag_from('docs\\api\\pokemon.yaml')
def get_pokemon_by_id(id):
    pokemon_id = request.args.get('id')
    return pokemonController.by_id(pokemon_type)

@pokemons_bp.route('/pokemon', methods=['GET'])
@csrf.exempt
@swag_from('docs\\api\\pokemon_by_type.yaml')
def get_pokemons_by_type():
    # user_id = get_jwt_identity()
    pokemon_type = request.args.get('type')
    return pokemonController.by_type(pokemon_type)