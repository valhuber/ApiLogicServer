#!/usr/bin/env python3
"""
  ApiLogicServer v 02.00.00

  $ python3 api_logic_server_run.py [Listener-IP]

  This will run the example on http://Listener-Ip:5000

"""
import sys
from typing import TypedDict

import logic_bank_utils.util as logic_bank_utils
import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from api import expose_api_models, expose_services
from logic import logic_bank

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="api_logic_server", my_file=__file__)

from flask import render_template, request, jsonify, Flask
from safrs import ValidationError, SAFRSBase


def setup_logging():
    # Initialize Logging
    import logging
    import sys

    logic_logger = logging.getLogger('logic_logger')   # for debugging user logic
    logic_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
    handler.setFormatter(formatter)

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
    setup_logging()
    flask_app = Flask("API Logic Server")
    flask_app.config.from_object("config.Config")
    db = safrs.DB  # opens database per config, setting session
    detail_logging = False  # True will log SQLAlchemy SQLs
    if detail_logging:
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    Base: declarative_base = db.Model
    session: Session = db.session
    print("api_logic_server_run#create_app - got session: " + str(session))

    def constraint_handler(message: str, constraint: object, logic_row: LogicRow):
        if constraint.error_attributes:
            detail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
        else:
            detail = {"model": logic_row.name}
        raise ValidationErrorExt(message= message, detail=detail)

    LogicBank.activate(session=session, activator=logic_bank.declare_logic, constraint_event=constraint_handler)

    with flask_app.app_context():
        db.init_app(flask_app)
        safrs_api = expose_api_models.expose_models(flask_app, host)
        expose_services.expose_services(flask_app, safrs_api)
        SAFRSBase._s_auto_commit = False
        session.close()

    return flask_app, safrs_api


# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[1:] \
    else "localhost"  # 127.0.0.1 verify in swagger or your client.  You wight need cors support.

flask_app, safrs_api = create_app(host=host)
print(f'api_logic_server_run {type(flask_app)} created with safrs_api {type(safrs_api)}')


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


@flask_app.after_request
def after_request(response):
    """
    Enable CORS. Disable it if you don't need CORS or install Cors Libaray
    https://parzibyte.me/blog
    """
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = \
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    flask_app.run(host=host, threaded=False)
