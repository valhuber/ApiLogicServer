from safrs import SAFRSAPI
import safrs
import importlib
import pathlib
import logging as logging

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

app_logger = logging.getLogger('api_logic_server_app')
app_logger.debug("\napi/expose_api_models.py - endpoint for each table")
