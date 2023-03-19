""" flask event handlers for the admin app
        * return minified app
        * return admin.yaml file
"""

import logging, sys, io
from flask import Flask, redirect, send_from_directory, send_file
from config import Config
from pathlib import Path
import os, inspect
from safrs import ValidationError

admin_logger = logging.getLogger(__name__)  # log levels: critical < error < warning(20) < info(30) < debug

did_send_spa = False

def get_sra_directory() -> str:
    """
    return location of minified sra, which can be...

    1. in the venv (from install or Docker) -- the normal case (small projects, less git)
    2. local to project: ui/safrs-react-admin
    3. for internal dev use, in env(APILOGICSERVER_HOME) (dev venv does not contain ALS)
    """
    directory = 'ui/safrs-react-admin'  # local project sra typical API Logic Server path (index.yaml)
    if Path(directory).joinpath('robots.txt').is_file():
        admin_logger.debug("return_spa - using local directory")
    else:     # else use installed sra - from venv, or, for dev, in APILOGICSERVER_HOME
        try:  # works for installed, docker, codespaces.  not Azure
            from api_logic_server_cli.create_from_model import api_logic_server_utils as api_logic_server_utils
        except:
            dev_home = os.getenv('APILOGICSERVER_HOME')
            if dev_home:
                admin_logger.debug("ApiLogicServer not in venv, trying APILOGICSERVER_HOME")
            else:
                dev_home = os.getenv('HOME')
                if not dev_home:
                    raise Exception('ApiLogicServer not in venv, env APILOGICSERVER_HOME or HOME must be set')
            sys.path.append(dev_home)
            from api_logic_server_cli.create_from_model import api_logic_server_utils as api_logic_server_utils
        admin_logger.debug("return_spa - install directory")
        utils_str = inspect.getfile(api_logic_server_utils)
        sra_path = Path(utils_str).parent.joinpath('safrs-react-admin-npm-build')
        directory = str(sra_path)
    return directory


def admin_events(flask_app: Flask, swagger_host: str, swagger_port: str, API_PREFIX: str, validation_error: ValidationError, http_type: str):
    """ events for serving minified safrs-admin, using admin.yaml
    """

    @flask_app.route("/admin/<path:path>")
    def start_custom_app_return_spa(path=None):
        """ Step 1 - Start Custom App, and return minified safrs-react-admin app (acquired from safrs-react-admin/build) 
            Custom url: http://localhost:5656/admin/custom_app
        """
        global did_send_spa
        admin_logger.debug(f'API Logic Server - Start Custom App, return minified sra')
        if True or not did_send_spa:
            did_send_spa = True
            admin_logger.info(f'\nStart Custom App ({path}): return spa "ui/safrs-react-admin", "index.html"\n')
        directory = get_sra_directory()
        return send_from_directory(directory, 'index.html')  # unsure how admin finds custom url

    @flask_app.route('/')
    def start_default_app():
        """ Step 1 - Start default Admin App 
            Default URL: http://localhost:5656/ 
        """
        admin_logger.info(f'API Logic Server - Start Default App - redirect /admin-app/index.html')
        return redirect('/admin-app/index.html')  # --> return_spa

    @flask_app.route("/admin-app/<path:path>")
    def return_spa(path=None):
        """ Step 2 - return minified sra for default admin app
        """
        global did_send_spa
        if path == "home.js":
            directory = "ui/admin"
        else:
            directory = get_sra_directory()

        if not did_send_spa:
            did_send_spa = True
            admin_logger.debug(f'return_spa - directory = {directory}, path= {path}')

        return send_from_directory(directory, path)


    @flask_app.route('/ui/admin/<path:path>')
    def admin_yaml(path=None):
        """ Step 3 - return admin file response (to now-running safrs-react-admin app)
            and text-substitutes to get url args from startup args (avoid specify twice for *both* server & admin.yaml)

            api_root: {http_type}://{swagger_host}:{swagger_port} (from ui_admin_creator)

            e.g. http://localhost:5656/ui/admin/admin.yaml
        """
        use_type = "mem"
        if use_type == "mem":
            with open(f'ui/admin/{path}', "r") as f:  # path is admin.yaml for default url/app
                content = f.read()
            content = content.replace("{http_type}", http_type)
            content = content.replace("{swagger_host}", swagger_host)
            content = content.replace("{port}", str(swagger_port))  # note - codespaces requires 443 here (typically via args)
            content = content.replace("{api}", API_PREFIX[1:])
            if Config.SECURITY_ENABLED == False:
                content = content.replace("authentication", 'no-authentication')
            admin_logger.debug(f'loading ui/admin/admin.yaml')
            mem = io.BytesIO(str.encode(content))
            return send_file(mem, mimetype='text/yaml')
        else:
            response = send_file("ui/admin/admin.yaml", mimetype='text/yaml')
            return response

    @flask_app.route('/ui/images/<path:path>')
    def get_image(path=None):
        """ return requested image
            data: Employee/janet.jpg
            url:  http://localhost:5656/ui/images/Employee/janet.jpg
        """
        response = send_file(f'ui/images/{path}', mimetype='image/jpeg')
        return response


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
        '''
        Enable CORS. Disable it if you don't need CORS or install Cors Library
        https://parzibyte.me/blog
        '''
        response.headers[
            "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
        response.headers["Access-Control-Allow-Headers"] = \
            "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
        # admin_logger.debug(f'cors after_request - response: {str(response)}')
        return response
