from flask                 import jsonify, Response
from src.config.connection import userCollection
from src.models.UserModel  import UserModel, UserRepository, UserCreationException
from flask_jwt_extended    import create_access_token, get_jwt_identity
from werkzeug.security     import generate_password_hash, check_password_hash
from bson                  import ObjectId
import json
import os

class UserController:
    ze_salt   = os.getenv("SALT")
    user_repo = UserRepository(userCollection)

    def __init__(self):
        self.repository = UserRepository(userCollection)

    def register(self, user_data):
        #  ~ handle_register()
        # log.debug("========== Create User Controller ==========")
        try:
            new_user = UserModel(**user_data)
            prev_user = self.repository.get_user_by_email(new_user.email)
            if prev_user is None:
                # new_user.password = encrypt_password(new_user.password, cls.ze_salt)
                hashed_password = generate_password_hash(new_user.password)
                new_user.password = hashed_password
                result = self.repository.create_user(new_user)
                resp = {
                    'message': 'User created successfully',
                    'user_id': str(result.inserted_id)
                }
                return jsonify(resp), 201
            else:
                return jsonify({'message' : f"This email {new_user.email} was registered previously"}), 409
        except UserCreationException as e:
            return jsonify({'error' : str(e)}), 500
        except ValueError as e:
            return jsonify({'error' : 'Invalid data provided'}), 500


    def login(self, user_data):
        try:
            unauth_user = UserModel(**user_data)
            prev_user = self.repository.get_user_by_email(unauth_user.email)

            # Check if a user with the provided email exists
            if prev_user:
                # Use check_password_hash to compare the stored hash with the provided password
                is_password_valid = check_password_hash(prev_user['password'], unauth_user.password)

                # print(str(prev_user))

                if is_password_valid:
                    # Generate access token using the user's ID
                    print({'user_id' : prev_user['_id']})
                    access_token = create_access_token(identity=str(prev_user['_id']))
                    resp = {'access_token': access_token}
                    return jsonify(resp), 200
                else:
                    raise InvalidCredentialsException()
            else:
                return jsonify({'message':f"user *{unauth_user.email}* not found"}), 404

        except InvalidCredentialsException as e:
            return jsonify({'message':str(e)}), 401

        except Exception as e:
            return jsonify({'message':'Login failed due to an unexpected error', 'error':str(e)}), 500


    def profile(self):
        # ~ handle_profile()

        user_id = get_jwt_identity()  # Retrieve the JWT identity, which should be the user's unique ID
        print({'token_id' : user_id})
        user_id = ObjectId(user_id)
        
        try:
            user = self.repository.get_user_by_id(user_id)
            if user:
                # Prepare the user profile information to be returned
                # Exclude sensitive data like password hashes
                user_profile = {
                    "user_id"  : str(user['_id']),
                    "username" : user['username'],
                    "email"    : user['email'],
                    # "pokemons": user.email,
                    # Add other fields that you want to return in the user profile
                }
                return jsonify(user_profile), 200
            else:
                # User not found with the provided identity
                return jsonify({"message": "User not found"}), 404

        except Exception as e:
            # log.error(f"Error fetching user profile: {e}")
            return jsonify({"message": f"Unable to fetch user profile {str(e)}"}), 500


class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid username or password", *args):
        super().__init__(message, *args)
