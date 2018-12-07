from flask import Flask
from flask_cors import CORS

app = Flask('hubitat_tools_server')
CORS(app)

# You must import in this order
from .views import api
from .views import static_files

