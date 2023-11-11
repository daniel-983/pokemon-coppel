from typing             import List, Optional, Dict
from pydantic           import BaseModel
from pymongo.collection import Collection
from pymongo            import errors
from bson               import ObjectId
from flask              import Response
from datetime           import datetime
from enum               import Enum
# from src.config.utilities import WriteLog as log
import json

class EncounterStatus(str, Enum):
    SEEN   = "seen"
    CAUGHT = "caught"

class PokemonEncounterModel(BaseModel):
    user_id        : str
    pokemon_id     : str
    pokemon_name   : Optional[str] = None
    encounter_date : datetime
    status         : EncounterStatus

class PokemonEncounterRepository():

    def __init__(self, db: Collection):
        self.collection = db

    def encounter(self, encounter):
        try:
            result = self.collection.insert_one(encounter.dict())
            return result
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404
    
    def get_seen(self, user_id):
        try:
            seen_pokemons = self.collection.find({"user_id": user_id, "status" : "seen"})
            print(('get_seen', user_id))
            return self.serialize_pokemons(seen_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404

    def get_caught(self, user_id):
        try:
            caught_pokemons = self.collection.find({"user_id": user_id, "status" : "caught"})
            print(('get_caught', user_id))
            return self.serialize_pokemons(caught_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404

    def by_pokemon_id(self, user_id, pokemon_id):
        try:
            encounter = self.collection.find_one({"user_id": user_id, "pokemon_id" : pokemon_id})
            if encounter:
                return encounter['pokemon_name']
            else:
                return None
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404

    def serialize_pokemons(self, pokemons):
        # Convert each document's ObjectId to a string as 'encounter_id' and exclude '_id'
        return [
            {key: value for key, value in pokemon.items() if key != '_id'}
            | {'encounter_id': str(pokemon['_id'])} 
            for pokemon in pokemons if '_id' in pokemon
        ]
