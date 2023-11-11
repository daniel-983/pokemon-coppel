from src.models.PokemonModel import PokemonModel
import requests
import json

class PokemonService:
    def __init__(self, repository, redis_client):
        self.repository = repository
        self.redis_client = redis_client

    def fetch_from_pokeapi(self, pokemon_name: str):
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get data from PokeAPI for {pokemon_name}")

    def get_or_fetch_pokemon(self, pokemon_name):
        try:
            # Check for Pokemon data in Redis cache
            cached_pokemon = self.redis_client.get(pokemon_name)

            if cached_pokemon:
                print(f"pokemon data for *{pokemon_name}* retrieved from Redis!")
                return json.loads(cached_pokemon)

            else :
                # Fetch from PokeAPI
                pokemon_data = self.fetch_from_pokeapi(pokemon_name)

                # Transform the data to match PokemonModel
                pokemon_model = PokemonModel(**pokemon_data)

                # Serialize and store in Redis
                # serialized_data = json.dumps(pokemon_data)
                serialized_data = pokemon_model.json()
                self.redis_client.set(pokemon_name, serialized_data, ex=24 * 60 * 60)

                # Store in the repository
                result = self.repository.insert_pokemon(pokemon_model)
                pokemon_data['new_id'] = str(result.inserted_id)

                # pokemon_model = PokemonModel(**pokemon_data)
                # self.redis_client.set(pokemon_name, pokemon_model.json(), ex=24 * 60 * 60)
                print(f"Data for {pokemon_name} stored in Redis!")
                return pokemon_data

        except Exception as e:
            print(f"An error occurred in PokemonService with Redis or PokeAPI: {e}")
            raise e