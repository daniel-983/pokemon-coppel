from typing             import List, Optional, Dict
from pydantic           import BaseModel
from pymongo.collection import Collection
from pymongo            import errors
from bson               import ObjectId
from flask              import Response
from datetime           import date
from enum               import Enum
# from src.config.utilities import WriteLog as log
import json

class EncounterStatus(str, Enum):
    SEEN   = "seen"
    CAUGHT = "caught"

class PokemonEncounterModel(BaseModel):
    user_id        : str
    pokemon_id     : int
    pokemon_name   : Optional[str] = None
    encounter_date : date
    status         : EncounterStatus

class PokemonEncounterRepository():

    def __init__(self, db: Collection):
        self.collection = db

    def encounter(self, encounter_data):
        try:
            return self.collection.find_one({"id": id})
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0048", "message": "Connection error pksee"}), mimetype='application/json'), 404
        except TypeError as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0049", "message": "Verify data pksee"}), mimetype='application/json'), 404
        except Exception as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0050", "message": "Verify data pksee"}), mimetype='application/json'), 404
    
    def get_seen(self, user_id):
        try:
            seen_pokemons = self.collection.find({"user_id": user_id, "status" : "seen"})
            return list(seen_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0048", "message": "Connection error pksee"}), mimetype='application/json'), 404
        except TypeError as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0049", "message": "Verify data pksee"}), mimetype='application/json'), 404
        except Exception as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0050", "message": "Verify data pksee"}), mimetype='application/json'), 404

    def get_caught(self, name: str):
        try:
            caught_pokemons = self.collection.find({"user_id": user_id, "status" : "caught"})
            return list(seen_pokemons)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0051", "message": "Connection error pksee"}), mimetype='application/json'), 404
        except TypeError as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0052", "message": "Verify data pksee"}), mimetype='application/json'), 404
        except Exception as e:
            log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0053", "message": "Verify data pksee"}), mimetype='application/json'), 404
