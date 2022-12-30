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

    """
    Sample Binding (for each add-db):

    from api import expose_api_models_Todo
    from database import Todo_models

    flask_app.config.update(SQLALCHEMY_BINDS = \
        {'Todo': flask_app.config['SQLALCHEMY_DATABASE_URI_TODO']})
    
    app_logger.info(f"\nTODOs Config complete - database/Todo_models.py"
        + f'\n -- with bind: {session.bind}'
        + f'\n -- {len(database.Todo_models.BaseToDo.metadata.tables)} tables loaded')
    
    expose_api_models_Todo.expose_models(safrs_api)
    todos = session.query(Todo_models.Todo).all()

    """

    return