#!/usr/bin/env python3
"""
  ApiLogicServer v api_logic_server_version

  Created on api_logic_server_created_on

  $ python3 api_logic_server_run.py [Listener-IP] [port]  # this starts your ApiLogicServer project

  Access the server via the Browser: http://Listener-Ip:api_logic_server_port

"""
import os
import sys

if len(sys.argv) > 1 and sys.argv[1].__contains__("help"):
    print("")
    print("API Logic Server - run instructions (default is localhost):")
    print("  python api_logic_server_run.py [host]")
    print("")
    sys.exit()

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)
os.chdir(project_dir)  # so admin app can find images, code

import logging

app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.INFO)  # use WARNING to reduce output
app_logger.info(f'app started: {__file__}\n')

logging.getLogger('safrs').setLevel(logging.INFO)
logging.getLogger('safrs.safrs_init').setLevel(logging.INFO)

from typing import TypedDict

import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket

from api import expose_api_models, customize_api
from logic import declare_logic

from flask import Flask, redirect, send_from_directory, send_file
from safrs import ValidationError, SAFRSBase


def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    return os.path.isdir(path)


def setup_logging(flask_app):
    setup_logic_logger = True
    if setup_logic_logger:
        logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        if flask_app.config['SQLALCHEMY_DATABASE_URI'].endswith("db.sqlite"):
            formatter = logging.Formatter('%(message).160s')  # lead tag - '%(name)s: %(message)s')
            handler.setFormatter(formatter)
            logic_logger = logging.getLogger("logic_logger")
            logic_logger.handlers = []
            logic_logger.addHandler(handler)
            app_logger.warning("\nLog width truncated for readability -- "
                               "see https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python#debugging\n")
        else:
            formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        logic_logger.addHandler(handler)
        logic_logger.setLevel(logging.INFO)
        logic_logger.propagate = True

    do_engine_logging = False
    engine_logger = logging.getLogger('engine_logger')  # for internals
    if do_engine_logging:
        engine_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        engine_logger.addHandler(handler)
        engine_logger.setLevel(logging.DEBUG)

    do_sqlalchemy_info = False  # True will log SQLAlchemy SQLs
    if do_sqlalchemy_info:
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


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


import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI

db = safrs.DB  # opens database per config, setting session




def create_app(config_filename=None):
    admin_enabled = os.name != "nt"
    def constraint_handler(message: str, constraint: object, logic_row: LogicRow):
        if constraint.error_attributes:
            detail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
        else:
            detail = {"model": logic_row.name}
        raise ValidationErrorExt(message=message, detail=detail)

    flask_app = Flask("API Logic Server", template_folder='ui/templates')  # templates to load ui/admin/admin.yaml
    flask_app.config.from_object("config.Config")
    if admin_enabled:
        flask_app.config.update(SQLALCHEMY_BINDS={'admin': 'sqlite:////tmp/4LSBE.sqlite.4'})
    # flask_app.config.update(SQLALCHEMY_BINDS = {'admin': 'sqlite:///'})
    setup_logging(flask_app)
    # ?? db = safrs.DB  # opens database per config, setting session
    Base: declarative_base = db.Model
    session: Session = db.session

    LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)

    db.init_app(flask_app)
    with flask_app.app_context():
        if admin_enabled:
            db.create_all()
            db.create_all(bind='admin')
            session.commit()
        safrs_api = expose_api_models.expose_models(flask_app, HOST=host, PORT=port, API_PREFIX=API_PREFIX)
        customize_api.expose_services(flask_app, safrs_api, project_dir, HOST=host, PORT=port)  # custom services
        SAFRSBase._s_auto_commit = False
        session.close()

    return flask_app, safrs_api


# address where the api will be hosted, change this if you're not running the app on localhost!
network_diagnostics = True
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
host = "api_logic_server_host"
port = "api_logic_server_port"
if __name__ == "__main__":  # gunicorn-friendly host/port settings
    if sys.argv[1:]:
        host = sys.argv[1]  # you many need to enable cors support, below
        app_logger.debug(f'==> Network Diagnostic - using specified host: {sys.argv[1]}')
    else:
        app_logger.debug(f'==> Network Diagnostic - defaulting host: {host}')
    flask_host = host
    if is_docker() and host == "localhost":
        flask_host = "0.0.0.0"
        app_logger.debug(f'==> Network Diagnostic - using docker flask_host: {flask_host}')
    if sys.argv[2:]:
        port = sys.argv[2]  # you many need to enable cors support, below
        app_logger.debug(f'==> Network Diagnostic - using specified port: {sys.argv[2]}')

API_PREFIX = "/api_logic_server_api_name"
did_send_spa = False
flask_app, safrs_api = create_app()


@flask_app.route('/')
def index():
    app_logger.debug(f'API Logic Server - redirect /admin-app/index.html')
    return redirect('/admin-app/index.html')

"""
@flask_app.route('/ui/admin/admin.yaml')
def admin(path=None):  # test http://localhost/ui/admin/admin.yaml
    with open("ui/admin/admin.yaml", "r") as f:
        content = f.read()
    app_logger.debug(f'loading ui/admin/admin.yaml')
    return render_template('content.html', content=content)
"""


@flask_app.route('/ui/admin/admin.yaml')
def admin_yaml():
    response = send_file("ui/admin/admin.yaml", mimetype='text/yaml')
    return response


@flask_app.route("/admin-app/<path:path>")
def send_spa(path=None):
    global did_send_spa
    if path == "home.js":
        directory = "ui/admin"
    else:
        directory = 'ui/safrs-react-admin'
    if not did_send_spa:
        did_send_spa = True
        app_logger.debug(f'send_spa - directory = {directory}, path= {path}')
    return send_from_directory(directory, path)


@flask_app.errorhandler(ValidationError)
def handle_exception(e: ValidationError):
    res = {'code': e.status_code,
           'errorType': 'Validation Error',
           'errorMessage': e.message}
    #    if debug:
    #        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return res, 400


""" uncomment to disable cors support"""


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


""" """


if __name__ == "__main__":
    user_host = flask_host
    if is_docker():
        user_host = "localhost"
    msg = f'Starting ApiLogicServer project, version api_logic_server_version, available at http://{user_host}:{port}'
    if is_docker():
        msg += f' on docker container'
    app_logger.info(msg)
    flask_app.run(host=flask_host, threaded=False, port=port)
