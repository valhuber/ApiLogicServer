from typing import TypedDict

import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from api import expose_api_models
from database import db  # , session
from flask import Flask
from api.json_encoder import SAFRSJSONEncoderExt
from logic import logic_bank
from safrs import SAFRSAPI, ValidationError
from database import models

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")


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
    app = Flask("API Logic Server")
    app.config.from_object("config.Config")
    db = safrs.DB  # opens (what?) database, returning session
    Base: declarative_base = db.Model
    session: Session = db.session
    print("app/__init__#create_app - got session: " + str(session))

    def constraint_handler(message: str, constraint: object, logic_row: LogicRow):
        theDetail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
        raise ValidationErrorExt(message= message, detail=theDetail)

    LogicBank.activate(session=session, activator=logic_bank.declare_logic, constraint_event=constraint_handler)

    with app.app_context():
        db.init_app(app)
        expose_api_models.expose_models(app, host)

    return app
