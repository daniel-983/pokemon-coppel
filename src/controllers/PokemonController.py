from src                              import redis_client
from src.config.connection            import pokemonCollection
from src.services.PokemonService      import PokemonService
from src.models.PokemonModel          import PokemonModel, PokemonRepository, PokemonInsertException
from src.models.PokemonEncounterModel import PokemonEncounterRepository
from flask                            import jsonify, Response
import redis
import json
import os

class PokemonController:
	ze_salt = os.getenv("SALT")
	# caught_pokemon_repo = CaughtPokemonRepository(caughtPokemonCollection)

	def __init__(self):
		self.redis_client                 = redis_client
		self.repository                   = PokemonRepository(pokemonCollection)
		self.pokemon_encounter_repository = PokemonRepository(pokemonCollection)
		self.pokemon_service              = PokemonService(self.repository, self.redis_client)

	def search(self, pokemon_data):
		#  ~ handle_register()
		# log.debug("========== Create User Controller ==========")
		try:
			pokemon      = PokemonModel(**pokemon_data)
			prev_pokemon = self.repository.get_pokemon_by_name(pokemon.name)

			# self.pokemon_encounter_repository.seen()

			if prev_pokemon:
				prev_pokemon['_id'] = str(prev_pokemon['_id'])
				return jsonify(prev_pokemon), 200
			else :
				fetched_pokemon = self.pokemon_service.get_or_fetch_pokemon(pokemon.name)
				return jsonify(fetched_pokemon), 201
		# except UserCreationException as e:
			# return jsonify({'message' : f"Pokemon *{pokemon}* not found"}), 404
		except PokemonInsertException as e:
			return jsonify({'error' : str(e)}), 500
		except ValueError as e:
			return jsonify({'error' : f"Invalid data provided {str(e)}"}), 500


	def caught(cls, user_data):
		try:
			unauth_user = UserModel(**user_data)
			prev_user = cls.user_repo.get_user_by_email(unauth_user.email)

			# Check if a user with the provided email exists
			if prev_user:
				# Use check_password_hash to compare the stored hash with the provided password
				is_password_valid = check_password_hash(prev_user['password'], unauth_user.password)

				# print(str(prev_user))

				if is_password_valid:
					# Generate access token using the user's ID
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

	def pokemon(self, pokemon_name):
		pokemon_data = self.pokemon_service.get_pokemon_data(pokemon_name)
		return pokemon_data