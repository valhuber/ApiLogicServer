from safrs import SAFRSAPI
import safrs
import flask
import importlib
import pathlib
import logging as logging

app_logger = logging.getLogger("api_logic_server_app")

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

def open_databases(flask_app, session, safrs_api):
    """ called by api_logic_server_run to open each additional database, and expose APIs """

    # Begin Bind Databases

    # End Bind Databases

    return