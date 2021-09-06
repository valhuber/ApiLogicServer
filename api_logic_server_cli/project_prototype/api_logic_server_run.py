#!/usr/bin/env python3
"""
  ApiLogicServer v api_logic_server_version

  Created on api_logic_server_created_on GMT

  $ python3 api_logic_server_run.py [Listener-IP]

  This will run on http://Listener-Ip:5000

"""
import os
import sys
if len(sys.argv) > 1 and sys.argv[1].__contains__("help"):
    print("")
    print("API Logic Server - run instructions (default is localhost):")
    print("  python api_logic_server_run.py [host]")
    print("")
    sys.exit()

import logging
app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.INFO)  # use WARNING to reduce output

import threading
import time
import requests
from typing import TypedDict

import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket

from api import expose_api_models, expose_services
from logic import logic_bank

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)

from flask import render_template, request, jsonify, Flask
from safrs import ValidationError, SAFRSBase
import test.server_startup_test as self_test


def setup_logging():
    setup_logic_logger = True
    if setup_logic_logger:
        # util.log("api_logic_server_run - setup_logging()")
        logic_logger = logging.getLogger('logic_logger')   # for debugging user logic
        logic_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        logic_logger.addHandler(handler)
        logic_logger.propagate = True

    do_engine_logging = False
    engine_logger = logging.getLogger('engine_logger')  # for internals
    if do_engine_logging:
        engine_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        engine_logger.addHandler(handler)


class ValidationErrorExt(ValidationError):
    """
    This exception is raised when invalid input has been detected (client side input)
    Always send back the message to the client in the response
    """

    def __init__(self, message="", status_code=400, api_code=2001, detail=None, error_attributes=None):
        Exception.__init__(self)
        self.error_attributes = error_attributes
        self.status_code = status_code
        self.message = message
        self.api_code = api_code
        self.detail: TypedDict = detail


def create_app(config_filename=None, host="localhost"):
    flask_app = Flask("API Logic Server")
    flask_app.config.from_object("config.Config")
    setup_logging()
    db = safrs.DB  # opens database per config, setting session
    detail_logging = False  # True will log SQLAlchemy SQLs
    if detail_logging:
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    Base: declarative_base = db.Model
    session: Session = db.session
    # util.log("api_logic_server_run#create_app - got session: " + str(session))

    def constraint_handler(message: str, constraint: object, logic_row: LogicRow):
        if constraint.error_attributes:
            detail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
        else:
            detail = {"model": logic_row.name}
        raise ValidationErrorExt(message= message, detail=detail)

    LogicBank.activate(session=session, activator=logic_bank.declare_logic, constraint_event=constraint_handler)

    with flask_app.app_context():
        db.init_app(flask_app)
        safrs_api = expose_api_models.expose_models(flask_app, HOST=host)  # services from models
        expose_services.expose_services(flask_app, safrs_api, project_dir)  # custom services
        SAFRSBase._s_auto_commit = False
        session.close()

    return flask_app, safrs_api

""" old code - remove
host = sys.argv[1] if sys.argv[1:] \
    else local_ip  # "api_logic_server_host"  # 127.0.0.1 verify in swagger or your client.
"""

# address where the api will be hosted, change this if you're not running the app on localhost!
network_diagnostics = True
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
app_logger.debug(f'==> Network diagnostic - Warning -- local_ip ({local_ip}) != "api_logic_server_host"')
if sys.argv[1:]:
    host = sys.argv[1]  # you many need to enable cors support, below
    app_logger.debug(f'==> Network Diagnostic - using specified ip: {sys.argv[1]}')
    if host == "docker":
        host = "localhost"
        app_logger.debug(f'==> Network Diagnostic - docker = {host}')
    if host == "SWAGGER_HOST":
        host = os.getenv('SWAGGER_HOST', "0.0.0.0")
        app_logger.debug(f'==> Network Diagnostic - SWAGGER_HOST = {host}')
    if host == "dockerhost":
        host = "0.0.0.0"
        app_logger.debug(f'==> Network Diagnostic - dockerhost using {host}')
    if host == "dockerip":
        host = local_ip
        app_logger.debug(f'==> Network Diagnostic - dockerip using {host}')
else:
    host = "0.0.0.0"  # local_ip?  local_host?
    if network_diagnostics:
        app_logger.debug(f'==> Network Diagnostic - using default ip: 0.0.0.0')
port = "api_logic_server_port"
flask_app, safrs_api = create_app(host=host)


@flask_app.route('/')
def welcome():
    return render_template('index.html')


@flask_app.errorhandler(ValidationError)
def handle_exception(e: ValidationError):

    res = {'code': e.status_code,
           'errorType': 'Validation Error',
           'errorMessage': e.message}
#    if debug:
#        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return res, 400


""" enable for cors support
@flask_app.after_request
def after_request(response):
    '''
    Enable CORS. Disable it if you don't need CORS or install Cors Libaray
    https://parzibyte.me/blog
    '''
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = \
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    # print(f'cors aftter_request - response: {str(response)}')
    return response
"""


@flask_app.before_first_request
def run_before_first_request():
    ''' start_runner pings server, starts this (1 ping only, Visily)
    '''
    def run_server_start_test():
        self_test.server_tests(host, port, "api_logic_server_version")

    thread = threading.Thread(target=run_server_start_test)
    thread.start()


def one_ping_on_server_start_for_server_start_tests():
    """
    On server start: 1 ping only, Visily

    This executes @flask_app.before_first_request
    """
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get(f'http://{host}:5000/')
                if r.status_code == 200:
                    not_started = False
            except:
                pass  # server not started, not a problem
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == "__main__":
    if self_test.server_tests_enabled:  # see test/server_startup_test.py
        one_ping_on_server_start_for_server_start_tests()
    app_logger.info(f'Starting ApiLogicServer project, version api_logic_server_version')
    flask_app.run(host=host, threaded=False, port=port)
