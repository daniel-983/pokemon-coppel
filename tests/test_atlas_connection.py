import unittest
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class TestDBConnection(unittest.TestCase):

    def test_mongo_connection(self):
        """Test the MongoDB Atlas connection."""
        uri = os.getenv('MONGO_ATLAS_HOST')
        client = MongoClient(uri)
        print(uri)

        try:
            # The list_database_names method will trigger a server selection which
            # will verify if the client can connect to Atlas.
            databases = client.list_database_names()
            print("Connection Successful!")
            print("Databases:", databases)
        except Exception as e:
            self.fail(f"MongoDB Atlas connection failed: {e}")

if __name__ == '__main__':
    unittest.main()
