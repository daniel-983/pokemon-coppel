from pymongo.mongo_client  import MongoClient
from pymongo.server_api    import ServerApi
from dotenv                import load_dotenv
import os
# from flask_pymongo         import PyMongo

load_dotenv()

atlas_user     = os.getenv('MONGO_ATLAS_USER')
atlas_password = os.getenv('MONGO_ATLAS_PASSWORD')
atlas_host     = os.getenv('MONGO_ATLAS_HOST')

# app.config["MONGO_URI"] = "mongodb+srv://{}:{}@cluster0.stqtc4g.mongodb.net/?retryWrites=true&w=majority".format(atlas_user, atlas_password)

client = MongoClient(atlas_host, server_api=ServerApi('1'))
# mongo = PyMongo(app)

pokedex = client['PokedexDB']

# Crear colecciones
userCollection          = pokedex['Users']
pokemonCollection       = pokedex['Pokemons']
caughtPokemonCollection = pokedex['CaughtPokemons']