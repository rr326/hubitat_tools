import re
import requests
import flask
from flask import request
import json
from pathlib import Path
from datetime import datetime as dt
from ..lib.parse_hubitat_log import parse_log_line
from ..config import MANUAL_LOG_ENTRIES_PATH, FLASK_ROOT_PATH
from ..app import app


# Serve vue assets
@app.route('/vueassets/<path:rootpath>', methods={'GET'})
def serve_assets(rootpath):
    return flask.send_from_directory(FLASK_ROOT_PATH / 'static' / 'vue_built' / 'vueassets', rootpath)

# Special case for favicon. (Can't figure out how to link it properly in index.html)
@app.route('/favicon.ico', methods={'GET'})
def serve_favicon():
    return flask.send_from_directory(FLASK_ROOT_PATH / 'static' / 'vue_built', 'favicon.ico')


# Everything else, send to Vue's index.html
@app.route('/', methods={'GET'})
def serve_index():
    return flask.send_from_directory(FLASK_ROOT_PATH / 'static' / 'vue_built', 'index.html')

@app.route('/<path:rootpath>', methods={'GET'})
def serve_wildcard(rootpath):
    return flask.send_from_directory(FLASK_ROOT_PATH / 'static' / 'vue_built', 'index.html')

