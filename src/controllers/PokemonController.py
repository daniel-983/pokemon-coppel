from src                              import redis_client
from src.config.connection            import pokemonCollection, pokemonEncounterCollection
from src.services.PokemonService      import PokemonService
from src.models.PokemonModel          import PokemonModel, PokemonRepository, PokemonInsertException
from src.models.PokemonEncounterModel import PokemonEncounterModel, PokemonEncounterRepository
from flask_jwt_extended               import get_jwt_identity
from flask                            import jsonify, Response
from datetime                         import datetime
import redis
import json
import os

class PokemonController:
	ze_salt = os.getenv("SALT")
	# caught_pokemon_repo = CaughtPokemonRepository(caughtPokemonCollection)

	def __init__(self):
		self.redis_client                 = redis_client
		self.repository                   = PokemonRepository(pokemonCollection)
		self.pokemon_encounter_repository = PokemonEncounterRepository(pokemonEncounterCollection)
		self.pokemon_service              = PokemonService(self.repository, self.redis_client)

	def search(self, pokemon_data):
		#  ~ handle_register()
		# log.debug("========== Create User Controller ==========")
		try:
			pokemon      = PokemonModel(**pokemon_data)
			prev_pokemon = self.repository.get_pokemon_by_name(pokemon.name)

			if prev_pokemon:
				prev_pokemon['_id'] = str(prev_pokemon['_id'])
			else :
				fetched_pokemon = self.pokemon_service.get_or_fetch_pokemon(pokemon.name)
				prev_pokemon = fetched_pokemon
			
			encounter = {
				'user_id' : get_jwt_identity(),
				'pokemon_id' : prev_pokemon['_id'],
				'pokemon_name' : pokemon.name,
				'encounter_date' : datetime.now(),
				'status' : 'seen',
			}
			encounter_model = PokemonEncounterModel(**encounter)
			self.pokemon_encounter_repository.encounter(encounter_model)

			return jsonify(prev_pokemon), 201

		except PokemonInsertException as e:
			return jsonify({'error' : str(e)}), 500
		except ValueError as e:
			return jsonify({'error' : f"Invalid data provided {str(e)}"}), 500


	def catch(self, pokemon_data):
		#  ~ handle_register()
		# log.debug("========== Create User Controller ==========")
		try:
			pokemon_data['name'] = pokemon_data['pokemon_name'] 
			pokemon      = PokemonModel(**pokemon_data)
			prev_pokemon = self.repository.get_pokemon_by_name(pokemon.name)

			if prev_pokemon:
				prev_pokemon['_id'] = str(prev_pokemon['_id'])
			else :
				fetched_pokemon = self.pokemon_service.get_or_fetch_pokemon(pokemon.name)
				prev_pokemon = fetched_pokemon
			
			encounter = {
				'user_id' : get_jwt_identity(),
				'pokemon_id' : prev_pokemon['_id'],
				'pokemon_name' : pokemon.name,
				'encounter_date' : datetime.now(),
				'status' : 'caught',
			}
			encounter_model = PokemonEncounterModel(**encounter)
			self.pokemon_encounter_repository.encounter(encounter_model)
			
			return jsonify(prev_pokemon), 201

		except PokemonInsertException as e:
			return jsonify({'error' : str(e)}), 500
		except ValueError as e:
			return jsonify({'error' : f"Invalid data provided {str(e)}"}), 500

	def by_id(self, pokemon_id):
		user_id = get_jwt_identity()
		pokemon_name = self.pokemon_encounter_repository.by_pokemon_id(user_id, pokemon_id)
		if pokemon_name:
			pokemon_data = self.repository.get_pokemon_by_name(pokemon_name)
			#date seen
			#date caught
			return pokemon_data

	def by_type(self, pokemon_type):
		pokemons = self.repository.by_type(pokemon_id)
		return pokemons

