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
            return list(seen_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404

    def get_caught(self, name: str):
        try:
            caught_pokemons = self.collection.find({"user_id": user_id, "status" : "caught"})
            return list(seen_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"message": "Connection error"}), mimetype='application/json'), 404
