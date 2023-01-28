from safrs import SAFRSAPI
import logging as logging

app_logger = logging.getLogger("api_logic_server_app")

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

def open_databases(flask_app, session, safrs_api, method_decorators):
    """ called by api_logic_server_run to open each additional database, and expose APIs """

    # Begin Bind URLs

    # End Bind URLs

    flask_app.config.update(SQLALCHEMY_BINDS = {
    })  # make multiple databases available to SQLAlchemy
    return