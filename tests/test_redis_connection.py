import unittest
import redis
from dotenv import load_dotenv
import os

load_dotenv()

class TestRedisConnection(unittest.TestCase):

    def test_redis_connection(self):
        """Test the Redis connection."""
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', 6379)
        redis_db   = os.getenv('REDIS_DB', 0)

        try:
            # Create a Redis client
            r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

            # Test setting a value
            r.set('test_key', 'Hello, Redis!')

            # Test getting a value
            value = r.get('test_key')
            self.assertEqual(value, 'Hello, Redis!', "Redis connection test failed")

            print("Connection Successful!")
            print(f"The value of 'test_key' is: {value}")

        except Exception as e:
            self.fail(f"Redis connection failed: {e}")

if __name__ == '__main__':
    unittest.main()
