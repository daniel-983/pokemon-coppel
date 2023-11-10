from typing               import List, Optional, Dict
from pydantic             import BaseModel
from pymongo.collection   import Collection
from pymongo              import errors
from bson                 import ObjectId
from flask                import Response
# from src.config.utilities import WriteLog as log
import json

class UserModel(BaseModel):
    email    : str
    password : str
    username : Optional[str] = None

class UserRepository:

    def __init__(self, db: Collection):
        self.collection = db

    def create_user(self, user: UserModel):
        try:
            user_data = user.dict()
            result = self.collection.insert_one(user_data)
            return result
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            raise UserCreationException(f"Database error {e}")


    def update_user(self, user_id: str, user_data: dict):
        try:
            result = self.collection.update_one({"_id": user_id}, {"$set": user_data})
            if result.modified_count > 0:
                return Response(json.dumps({"message": "User updated"}), mimetype='application/json'), 200
            else:
                return Response(json.dumps({"message": "User not found or no changes made"}), mimetype='application/json'), 404
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0039", "message": "Connection error usr"}), mimetype='application/json'), 404
        except TypeError as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0040", "message": "Verify data usr"}), mimetype='application/json'), 404
        except Exception as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0041", "message": "Verify data usr"}), mimetype='application/json'), 404


    def delete_user(self, user_id: str):
        try:
            result = self.collection.delete_one({"_id": user_id})
            if result.deleted_count > 0:
                return json.dumps({"message": "User deleted"}), 200
            else:
                return json.dumps({"message": "User not found"}), 404
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0042", "message": "Connection error usr"}), mimetype='application/json'), 404
        except TypeError as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0043", "message": "Verify data usr"}), mimetype='application/json'), 404
        except Exception as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0044", "message": "Verify data usr"}), mimetype='application/json'), 404

    def get_user_by_email(self, email: str):
        try:
            user = self.collection.find_one({"email": email})
            if user:
                return user
            else:
                return None
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            return Response(json.dumps({"id": "EX-0033", "message": "Connection error usr"}), mimetype='application/json'), 404
        except TypeError as e:
            return Response(json.dumps({"id": "EX-0034", "message": "Verify data usr"}), mimetype='application/json'), 404
        except Exception as e:
            return Response(json.dumps({"id": "EX-0035", "message": "Verify data usr"}), mimetype='application/json'), 404

    def get_user_by_data(self, user: UserModel):
        try:
            user = self.collection.find_one({"_id": user.id})
            if user:
                return user
            else:
                return Response(json.dumps({"message": "User not found"}), 404)
        except (errors.ConnectionFailure, errors.PyMongoError) as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0036", "message": "Connection error usr"}), mimetype='application/json'), 404
        except TypeError as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0037", "message": "Verify data usr"}), mimetype='application/json'), 404
        except Exception as e:
            # log.set_log().debug(e)
            return Response(json.dumps({"id": "EX-0038", "message": "Verify data usr"}), mimetype='application/json'), 404

class UserCreationException(Exception):
    def __init__(self, message="User Creation unsuccessful"):
        self.message = message
        super().__init__(message, *args)