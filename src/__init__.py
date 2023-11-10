from flask              import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_wtf.csrf     import CSRFProtect
from flasgger           import Swagger
from redis              import Redis, exceptions
from dotenv             import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.debug = True

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
jwt_secret = os.getenv('JWT_SECRET_KEY')
secret     = os.getenv('SECRET_KEY')

cache = Redis(host=redis_host, port=redis_port, db=0)

app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_SECRET_KEY"] = jwt_secret
app.config["SECRET_KEY"] = secret

jwt  = JWTManager(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
Swagger(app)

from src.routes.RouterUser    import users_bp
# from src.routes.RouterPokemon import pokemons_bp

app.register_blueprint(users_bp, url_prefix='/api')

