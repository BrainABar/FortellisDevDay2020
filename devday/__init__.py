from flask import Flask
from flasgger import Swagger
from devday.config import Config

# initialize flask
app = Flask(__name__)
Swagger(app)

from devday import routes
