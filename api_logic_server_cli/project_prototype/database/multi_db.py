from safrs import SAFRSAPI
import logging as logging  # additional per-database imports

app_logger = logging.getLogger("api_logic_server_app")


def bind_dbs(flask_app):
    """ called by api_logic_server_run to open/bind each additional database"""

    flask_app.config.update(SQLALCHEMY_BINDS = {
    })  # make multiple databases available to SQLAlchemy

    return


def expose_db_apis(flask_app, session, safrs_api, method_decorators):
    """ called by api_logic_server_run to expose APIs for each additional database """

    # Begin Expose APIs

    # End Expose APIs
    return