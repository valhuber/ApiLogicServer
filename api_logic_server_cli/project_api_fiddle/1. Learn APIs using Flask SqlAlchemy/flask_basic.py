import os
import logging, logging.config
from flask import Flask  # fails without venv - see https://apilogicserver.github.io/Docs/Project-Env/
from config import Config
from flask_sqlalchemy import SQLAlchemy
from config import Config
import yaml

"""
This illustrates a hand-coded) Flask application.

See: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

"""

"""
Logging configuration
"""
current_path = os.path.abspath(os.path.dirname(__file__))
with open(f'{current_path}/logging.yml','rt') as f:  # see also api/end_points
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)  # log levels: critical < error < warning(20) < info(30) < debug
app_logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy()      # database access

app = Flask(__name__)  # server creation

app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI  # db location

db.init_app(app)        # initialize the app with the extension

import api.end_points as api_end_points
api_end_points.flask_events(app, db)  # register endpoints

logging.info("Server started: test by copying the cURL commands to a terminal window...")
logging.info('  curl -X GET "http://localhost:8080/hello_world"')
logging.info('  curl -X GET "http://localhost:8080/order?Id=10643"')
logging.info('')

app.run(host="localhost", port=8080, debug=True)  # start the server (does not return)

