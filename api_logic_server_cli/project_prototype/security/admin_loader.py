import logging, sys, io
from flask import Flask, redirect, send_from_directory, send_file

app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.INFO)  # log levels: critical < error < warning(20) < info(30) < debug

did_send_spa = False

def admin_events(flask_app: Flask, swagger_host: str, swagger_port: str, API_PREFIX: str, ValidationError: object):
    """ events for serving minified safrs-admin, using admin.yaml
    """

    @flask_app.route("/admin/<path:path>")
    def start_custom_app_return_spa(path=None):
        """ Step 1 - Start Custom App, and return minified safrs-react-admin app (acquired from safrs-react-admin/build) 
            Custom url: http://localhost:5656/admin/custom_app
        """
        global did_send_spa
        if True or not did_send_spa:
            did_send_spa = True
            app_logger.info(f'\nStart Custom App ({path}): return spa "ui/safrs-react-admin", "index.html"\n')
        return send_from_directory('ui/safrs-react-admin', 'index.html')  # unsure how admin finds custom url

    @flask_app.route('/')
    def start_default_app():
        """ Step 1 - Start default Admin App 
            Default URL: http://localhost:5656/ 
        """
        app_logger.debug(f'API Logic Server - Start Default App - redirect /admin-app/index.html')
        return redirect('/admin-app/index.html')  # --> return_spa

    @flask_app.route("/admin-app/<path:path>")
    def return_spa(path=None):
        """ Step 2 - return minified safrs-react-admin app
            This is in ui/safrs-react-admin (ultimately acquired from safrs-react-admin/build) 
        """
        global did_send_spa
        if path == "home.js":
            directory = "ui/admin"
        else:
            directory = 'ui/safrs-react-admin'  # typical API Logic Server path (index.yaml)
        if not did_send_spa:
            did_send_spa = True
            app_logger.debug(f'return_spa - directory = {directory}, path= {path}')
        return send_from_directory(directory, path)

    @flask_app.route('/ui/admin/<path:path>')
    def admin_yaml(path=None):
        """ Step 3 - return admin file response: /ui/admin/<path:path> (to now-running safrs-react-admin app)
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
            app_logger.debug(f'loading ui/admin/admin.yaml')
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
        # app_logger.debug(f'cors after_request - response: {str(response)}')
        return response
