from typing             import List, Optional, Dict
from pydantic           import BaseModel
from pymongo.collection import Collection
from pymongo            import errors
from bson               import ObjectId

class PokemonModel(BaseModel):
    name          : str
    forms         : Optional[List] = None
    types         : Optional[List] = None
    sprites       : Optional[Dict] = None
    abilities     : Optional[List] = None
    game_versions : Optional[List] = None

    class Config:
        arbitrary_types_allowed = True

class PokemonRepository:

    def __init__(self, db: Collection):
        self.collection = db

    def insert_pokemon(self, pokemon: PokemonModel):
        try:
            result = self.collection.insert_one(pokemon.dict())
            return result
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            raise PokemonInsertException('Conection error')
        except TypeError as e:
            raise PokemonInsertException('Verify pokemon data')

    def get_pokemon_by_name(self, pokemon_name):
        try:
            pokemon = self.collection.find_one({'name' : pokemon_name})
            if pokemon:
                return pokemon
            else:
                return None

        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            raise PokemonInsertException('Conection error')
        except TypeError as e:
            raise PokemonInsertException('Verify pokemon data')

    def get_pokemons_by_type(self, pokemon_type : str):
        try:
            pokemons = self.collection.find({'types' : pokemon_type})
            return list(pokemon)

        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            raise PokemonInsertException('Conection error')
        except TypeError as e:
            raise PokemonInsertException('Could not retrieve pokemon by type. Verify pokemon data')


class PokemonInsertException(Exception):
    def __init__(self, message="User Creation unsuccessful"):
        self.message = message
        super().__init__(message, *args)