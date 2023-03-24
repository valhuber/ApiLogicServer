#!/usr/bin/env python3

"""
==============================================================================

    This file initializes and starts the API Logic Server (v api_logic_server_version, api_logic_server_created_on):
        $ python3 api_logic_server_run.py [--help]

    Then, access the Admin App and API via the Browser, eg:  
        http://api_logic_server_host:api_logic_server_port

    You typically do not customize this file,
        except to override Creation Defaults and Logging, below.

    See Main Code (at end).
        Use log messages to understand API and Logic activation.

==============================================================================
"""

import os, logging, logging.config, sys, yaml
from flask_sqlalchemy import SQLAlchemy
import json
from pathlib import Path

def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    # assert path_result == env_result
    return path_result


# =======================================
#    Creation Defaults
#
#        Override as desired
#         Or specify in CLI arguments
# ======================================= 

# defaults from ApiLogicServer create command...
API_PREFIX = "/api"
flask_host   = "api_logic_server_host"  # where clients find  the API (eg, cloud server addr)
swagger_host = "api_logic_server_swagger_host"
if swagger_host == "":
    swagger_host = flask_host  # where swagger finds the API
if is_docker() and flask_host == "localhost":
    flask_host = "0.0.0.0"  # enables docker run.sh (where there are no args)
port = "api_logic_server_port"
swagger_port = port  # for codespaces - see values in launch config
http_type = "http"

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
project_dir = str(current_path)
os.chdir(project_dir)  # so admin app can find images, code
import util as util


# ==================================
#       LOGGING SETUP
# ================================== 

current_path = os.path.abspath(os.path.dirname(__file__))
with open(f'{current_path}/logging.yml','rt') as f:  # see also logic/declare_logic.py
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)  # log levels: critical < error < warning(20) < info(30) < debug
app_logger = logging.getLogger(__name__)
debug_value = os.getenv('APILOGICPROJECT_DEBUG')
if debug_value is not None:  # > export APILOGICPROJECT_DEBUG=True
    debug_value = debug_value.upper()
    if debug_value.startswith("F") or debug_value.startswith("N"):
        app_logger.setLevel(logging.INFO)
    else:
        app_logger.setLevel(logging.DEBUG)
        app_logger.debug(f'\nDEBUG level set from env\n')


args = ""
arg_num = 0
for each_arg in sys.argv:
    args += each_arg
    arg_num += 1
    if arg_num < len(sys.argv):
        args += ", "
project_name = os.path.basename(os.path.normpath(current_path))
app_logger.info(f'\nAPI Logic Project ({project_name}) Starting with args: \n.. {args}\n')
app_logger.info(f'Created api_logic_server_created_on at {str(current_path)}\n')

from typing import TypedDict
import safrs  # fails without venv - see https://apilogicserver.github.io/Docs/Project-Env/
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.rule_type.constraint import Constraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import socket
import warnings
from flask import Flask, redirect, send_from_directory, send_file
from safrs import ValidationError, SAFRSBase, SAFRSAPI
from config import Config
from ui.admin.admin_loader import admin_events
from security.system.authentication import configure_auth

def setup_logging(flask_app):
    setup_logic_logger = False
    if setup_logic_logger:
        logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        truncate_log = False  # useful for non-IDE run (e.g. console) to see logic indenting
        if truncate_log and flask_app.config['SQLALCHEMY_DATABASE_URI'].endswith("db.sqlite"):
            formatter = logging.Formatter('%(message).160s')  # lead tag - '%(name)s: %(message)s')
            handler.setFormatter(formatter)
            logic_logger = logging.getLogger("logic_logger")
            logic_logger.handlers = []
            logic_logger.addHandler(handler)
            app_logger.warning("\nLog width truncated for readability -- "
                               "see api_logic_server_run.py in your API Logic Project\n")
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

    do_safrs_logging = False
    if do_safrs_logging:
        safrs_init_logger = logging.getLogger('safrs.safrs_init')
        safrs_init_logger.setLevel(logging.DEBUG)
        safrs_logger = logging.getLogger('safrs')
        safrs_logger.setLevel(logging.DEBUG)

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


def get_args():
    """
    returns tuple: (flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run)
    """

    global flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run

    network_diagnostics = True
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = f"Warning - Failed local_ip = socket.gethostbyname(hostname) with hostname: {hostname}"
        app_logger.debug(f"Failed local_ip = socket.gethostbyname(hostname) with hostname: {hostname}")

    app_logger.debug(f"Getting args, with hostname={hostname} on local_ip={local_ip}")
    verbose = False
    create_and_run = False

    def make_wide(formatter, w=120, h=36):
        """ Return a wider HelpFormatter, if possible."""
        try:
            # https://stackoverflow.com/a/5464440
            # beware: "Only the name of this class is considered a public API."
            kwargs = {'width': w, 'max_help_position': h}
            formatter(None, **kwargs)
            return lambda prog: formatter(prog, **kwargs)
        except TypeError:
            warnings.warn("argparse help formatter failed, falling back.")
            return formatter

    if __name__ != "__main__":  
        app_logger.debug(f"WSGI - no args, using creation default host/port..  sys.argv = {sys.argv}\n")
    else:   # gunicorn-friendly host/port settings ()
        # thanks to https://www.geeksforgeeks.org/command-line-arguments-in-python/#argparse
        import argparse
        # Initialize parser
        if len(sys.argv) == 1:
            app_logger.debug("No arguments - using creation default host/port")
        else:
            msg = "API Logic Project"
            parser = argparse.ArgumentParser(
                formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter))
            parser.add_argument("--port",
                                help = f'port (Flask)', default = port)
            parser.add_argument("--flask_host", 
                                help = f'ip to which flask will be bound', 
                                default = flask_host)
            parser.add_argument("--swagger_host", 
                                help = f'ip clients use to access API',
                                default = swagger_host)
            parser.add_argument("--swagger_port", 
                                help = f'swagger port (eg, 443 for codespaces)',
                                default = port)
            parser.add_argument("--http_type", 
                                help = f'http or https',
                                default = "http")
            parser.add_argument("--verbose", 
                                help = f'for more logging',
                                default = False)
            parser.add_argument("--create_and_run", 
                                help = f'system use - log how to open project',
                                default = False)
            
            parser.add_argument("flask_host_p", nargs='?', default = flask_host)
            parser.add_argument("port_p", nargs='?', default = port)
            parser.add_argument("swagger_host_p", nargs='?', default = swagger_host)
            
            args = parser.parse_args()

            """
                accepting both positional (compatibility) and keyword args... 
                cases that matter:
                    no args
                    kw only:        argv[1] starts with -
                    pos only
                positional values always override keyword, so decide which parsed values to use...
            """
            if sys.argv[1].startswith("-"):     # keyword arguments
                port = args.port
                flask_host = args.flask_host
                swagger_host = args.swagger_host
                swagger_port = args.swagger_port
                http_type = args.http_type
                verbose = args.verbose in ["True", "true"]
                create_and_run = args.create_and_run
            else:                               # positional arguments (compatibility)
                port = args.port_p
                flask_host = args.flask_host_p
                swagger_host = args.swagger_host_p
        if swagger_host.startswith("https://"):
            swagger_host = swagger_host[8:]
        if swagger_host.endswith("/"):
            swagger_host = swagger_host[0:len(swagger_host)-1]

    use_codespace_defaulting = True  # experimental support to run default launch config
    if use_codespace_defaulting and os.getenv('CODESPACES') and swagger_host == 'localhost':
        app_logger.info('\n Applying Codespaces default port settings')
        swagger_host = os.getenv('CODESPACE_NAME') + '-5656.githubpreview.dev'
        swagger_port = 443
        http_type = 'https'

    return flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run


# ==========================================================
# Creates flask_app, Opens Database, Activates API and Logic 
# ==========================================================

def create_app(swagger_host: str = "localhost", swagger_port: str = "5656"):
    """ Creates flask_app, Opens Database, Activates API and Logic """ 

    from sqlalchemy import exc as sa_exc

    with warnings.catch_warnings():

        flask_app = Flask("API Logic Server", template_folder='ui/templates')  # templates to load ui/admin/admin.yaml

        setup_logging(flask_app)        
        safrs_log_level = safrs.log.getEffectiveLevel()
        db_logger = logging.getLogger('sqlalchemy')
        db_log_level = db_logger.getEffectiveLevel()
        do_hide_chatty_logging = True
        if do_hide_chatty_logging and app_logger.getEffectiveLevel() <= logging.INFO:
            safrs.log.setLevel(logging.WARN)  # debug is 10, warn is 20, info 30
            db_logger.setLevel(logging.WARN)
        flask_app.config.from_object("config.Config")

        # https://stackoverflow.com/questions/34674029/sqlalchemy-query-raises-unnecessary-warning-about-sqlite-and-decimal-how-to-spe
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)  # alert - disable for safety msgs

        def constraint_handler(message: str, constraint: Constraint, logic_row: LogicRow):
            """ format LogicBank constraint exception for SAFRS """
            if constraint.error_attributes:
                detail = {"model": logic_row.name, "error_attributes": constraint.error_attributes}
            else:
                detail = {"model": logic_row.name}
            raise ValidationErrorExt(message=message, detail=detail)

        admin_enabled = os.name != "nt"
        admin_enabled = False
        """ internal use, for future enhancements """
        if admin_enabled:
            flask_app.config.update(SQLALCHEMY_BINDS={'admin': 'sqlite:////tmp/4LSBE.sqlite.4'})

        db = SQLAlchemy()
        db.init_app(flask_app)
        with flask_app.app_context():

            with open(Path(current_path).joinpath('security/system/custom_swagger.json')) as json_file:
                custom_swagger = json.load(json_file)
            safrs_api = SAFRSAPI(flask_app, app_db= db, host=swagger_host, port=swagger_port, prefix = API_PREFIX, custom_swagger=custom_swagger)

            db = safrs.DB  # valid only after is initialized, above
            session: Session = db.session

            if admin_enabled:  # unused (internal dev use)
                db.create_all()
                db.create_all(bind='admin')
                session.commit()

            from api import expose_api_models, customize_api

            import database.models
            app_logger.info("Data Model Loaded, customizing...")
            from database import customize_models

            from logic import declare_logic
            app_logger.info("")
            LogicBank.activate(session=session, activator=declare_logic.declare_logic, constraint_event=constraint_handler)
            app_logger.info("Declare   Logic complete - logic/declare_logic.py (rules + code)"
                + f' -- {len(database.models.metadata.tables)} tables loaded\n')  # db opened 1st access
            
            method_decorators : list = []
            expose_api_models.expose_models(safrs_api, method_decorators)
            app_logger.info(f'Declare   API - api/expose_api_models, endpoint for each table on {swagger_host}:{swagger_port}, customizing...')
            customize_api.expose_services(flask_app, safrs_api, project_dir, swagger_host=swagger_host, PORT=port)  # custom services

            if Config.SECURITY_ENABLED:
                configure_auth(flask_app, database, method_decorators)

            from database.bind_databases import open_databases
            open_databases(flask_app, session, safrs_api, method_decorators)

            if Config.SECURITY_ENABLED:
                from security import declare_security  # activate security
                app_logger.info("..declare security - security/declare_security.py"
                    + f' -- {len(database.authentication_models.metadata.tables)} authentication tables loaded')

            SAFRSBase._s_auto_commit = False
            session.close()
        
        safrs.log.setLevel(safrs_log_level)
        db_logger.setLevel(db_log_level)
        return flask_app


# ==================================
#        MAIN CODE
# ================================== 

(flask_host, swagger_host, port, swagger_port, http_type, verbose, create_and_run) = get_args()
if os.getenv('SWAGGER_HOST'):
    swagger_host = os.getenv('SWAGGER_HOST')  # type: ignore # type: str
if os.getenv('VERBOSE'):
    verbose = True  # type: ignore # type: str

if verbose:
    app_logger.setLevel(logging.DEBUG)
    safrs.log.setLevel(logging.DEBUG)  # debug is 10, warn is 20, info 30
if True or app_logger.getEffectiveLevel() == logging.DEBUG:
    util.sys_info()

flask_app = create_app(swagger_host = swagger_host, swagger_port = swagger_port)

admin_events(flask_app = flask_app, swagger_host = swagger_host, swagger_port = swagger_port,
    API_PREFIX=API_PREFIX, validation_error=ValidationError, http_type = http_type)

if __name__ == "__main__":
    msg = f'API Logic Project loaded (not WSGI), version api_logic_server_version\n'
    if is_docker():
        msg += f' (running from docker container at flask_host: {flask_host} - may require refresh)\n'
    else:
        msg += f' (running locally at flask_host: {flask_host})\n'
    app_logger.info(f'\n{msg}')

    if create_and_run:
        app_logger.info(f'==> Customizable API Logic Project created and running:\n'
                    f'..Open it with your IDE at {project_dir}\n')

    if os.getenv('CODESPACES'):
        app_logger.info(f'API Logic Project (name: {project_name}) starting on Codespaces:\n'
                f'..Explore data and API on codespaces, swagger_host: {http_type}://{swagger_host}/\n')
    else:
        app_logger.info(f'API Logic Project (name: {project_name}) starting:\n'
                f'..Explore data and API at swagger_host: {http_type}://{swagger_host}:{port}/\n')

    flask_app.run(host=flask_host, threaded=True, port=port)
else:
    msg = f'API Logic Project Loaded (WSGI), version api_logic_server_version\n'
    if is_docker():
        msg += f' (running from docker container at {flask_host} - may require refresh)\n'
    else:
        msg += f' (running locally at flask_host: {flask_host})\n'
    app_logger.info(f'\n{msg}')
    app_logger.info(f'API Logic Project (name: {project_name}) starting:\n'
            f'..Explore data and API at swagger_host: {http_type}://{swagger_host}:{port}/\n')
