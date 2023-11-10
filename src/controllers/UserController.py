from flask                 import jsonify, Response
from src.config.connection import userCollection
# from src.config.utilities import WriteLog as log
# from src.config.utilities import encrypt_password, validate_password
from src.models.ModelUser  import UserModel, UserRepository
from flask_jwt_extended    import create_access_token
from werkzeug.security     import generate_password_hash, check_password_hash
import json
import os

class UserController:
    ze_salt   = os.getenv("SALT")
    user_repo = UserRepository(userCollection)

    @classmethod
    def register(cls, user_data):
        #  ~ handle_register()
        # log.debug("========== Create User Controller ==========")
        try:
            new_user = UserModel(**user_data)
            prev_user = cls.user_repo.get_user_by_email(new_user.email)
            print(prev_user)
            if prev_user is None:
                # new_user.password = encrypt_password(new_user.password, cls.ze_salt)
                new_user.password = generate_password_hash(new_user.password)
                return cls.user_repo.create_user(new_user)
            elif prev_user[1] == 404:
                return Response(json.dumps({'message': 'Connection Error'}), mimetype='application/json'), 502
            else:
                return Response(json.dumps({'message': 'User already exists'}), mimetype='application/json'), 409
        except ValueError as e:
            log.set_log().debug(e)
            return Response(json.dumps({'message': 'Verify username and password'}), mimetype='application/json'), 400


    @classmethod
    def login(cls, user_data):
        # ~ handle_login()
        # log.set_log().debug("========== Authenticate User Controller ==========")

        unauth_user = UserModel(**user_data)
        prev_user = cls.user_repo.get_user_by_username(unauth_user.username)
        try:
            # hashed password is stored in the database
            # compare proviced password after hashing it with the stored hash
            # hashed_password = encrypt_password(unauth_user.password, ze_salt)
            is_password_valid = validate_password(unauth_user.password, prev_user.password, cls.ze_salt)
            if is_password_valid:
                # Assuming the user has a unique identifier, like an 'id'
                access_token = create_access_token(identity=str(user['id']))
                return Response(json.dumps({'access_token': access_token}), mimetype='application/json', status=200)
            else:
                # Handle invalid password
                return Response(json.dumps({'message': 'Invalid username or password'}), mimetype='application/json', status=401)
        except Exception as e:
            log.debug(e)


    @classmethod
    def get_user_profile(cls, user_id):
        # ~ handle_profile()

        user_id = get_jwt_identity()  # Retrieve the JWT identity, which should be the user's unique ID
        
        try:
            user = cls.user_repo.get_user_by_id(user_id)
            if user:
                # Prepare the user profile information to be returned
                # Exclude sensitive data like password hashes
                user_profile = {
                    "username": user.username,
                    "email": user.email,
                    # "pokemons": user.email,
                    # Add other fields that you want to return in the user profile
                }
                return jsonify(user_profile), 200
            else:
                # User not found with the provided identity
                return jsonify({"message": "User not found"}), 404

        except Exception as e:
            # log.error(f"Error fetching user profile: {e}")
            return jsonify({"message": "Unable to fetch user profile"}), 500
