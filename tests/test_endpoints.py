from datetime import datetime
import unittest
import requests
import uuid
import json
import random

class TestEndpoints(unittest.TestCase):
    
    def test_user_flow(self):

        base_url = 'http://localhost:5000/api'

        # Step 1: Register new user
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # random_username = f'testuser{uuid.uuid4().hex}_{timestamp}'
        random_username = f'testuser_{timestamp}'
        test_user = {
            'username' : random_username,
            'email' : f'{random_username}@softtek.com',
            'password' : 'testpass',
        }
        register_headers = {
            'Content-Type' : 'application/json',
            'accept' : 'application/json',
        }
        response = requests.post(f'{base_url}/register', headers=register_headers, json=test_user)
        print(response.json())
        self.assertEqual(response.status_code, 201)


        # Step 2: Log In
        login_headers = {
            'Content-Type' : 'application/json',
            'accept' : 'application/json',
        }
        response = requests.post(f'{base_url}/login', headers=login_headers, json=test_user)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        token = response.json().get('access_token')


        # Step 3: Check Profile (Initially Empty)
        headers = {
            'Authorization' : f'Bearer {token}',
            'Content-Type' : 'application/json',
            'accept' : 'application/json',
        }
        print(headers)
        response = requests.get(f'{base_url}/profile', headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.json.get('seen_pokemons')), 0)
        # self.assertEqual(len(response.json.get('caught_pokemons')), 0)


        # Step 4: Search and Catch 10 Pokemons
        pokemon_list = [
            "charmander", "bulbasaur", "squirtle", "pidgeotto", "alakazam",
            "jigglypuff", "gengar", "eevee", "snorlax", "dragonite",
            "totodile", "cyndaquil", "espeon", "tyranitar", "mudkip",
            "gardevoir", "lucario", "togekiss", "axew", "sylveon",
            "blastoise", "venusaur", "arbok", "raichu", "sandshrew",
            "nidoqueen", "nidoking", "clefable", "ninetales", "wigglytuff",
            "vileplume", "poliwrath", "marowak", "hitmonlee",
            "hitmonchan", "lickitung", "weezing", "rhydon", "chansey"
        ]

        # Get 10 random Pokemon names from the list
        random.shuffle(pokemon_list)
        for pokemon_name in pokemon_list[:5]:
            # Search
            pokemon_search = {'pokemon_name' : pokemon_name}
            response = requests.post(f'{base_url}/search', headers=headers, json=pokemon_search)
            print('/search')
            print(response.json())
            self.assertEqual(response.status_code, 201)

        random.shuffle(pokemon_list)
        for pokemon_name in pokemon_list[:4]:
            # Catch
            pokemon_search = {'pokemon_name' : pokemon_name}
            response = requests.post(f'{base_url}/catch', headers=headers, json=pokemon_search)
            print('/catch')
            print(response.json())
            self.assertEqual(response.status_code, 201)

        # Step 5: Check Profile (Should Have 10 Seen and Caught Pokemons)
        response = requests.get(f'{base_url}/profile', headers=headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('seen_pokemons')), 5)
        self.assertEqual(len(response.json().get('caught_pokemons')), 4)

if __name__ == '__main__':
    unittest.main()
