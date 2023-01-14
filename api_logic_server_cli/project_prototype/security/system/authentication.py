"""
System support for login / authentication.

Applications POST to login to obtain an access token,
which they provide in the header of subsequent requests.

e.g. 
def login():
    post_uri = 'http://localhost:5656/auth/login'
    post_data = {"username": "aneu"}
    r = requests.post(url=post_uri, json = post_data)
    response_text = r.text
    status_code = r.status_code
    if status_code > 300:
        raise Exception(f'POST login failed with {r.text}')
    result_data = json.loads(response_text)
    result_map = DotMap(result_data)
    token = result_map.access_token
    header = {'Authorization': 'Bearer {}'.format(f'{token}')}
    return header

"""

import logging, sys
from flask import Flask
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from datetime import timedelta
import config

authentication_provider = config.Config.SECURITY_PROVIDER

security_logger = logging.getLogger('API Logic Security')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(name)s: %(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
security_logger.addHandler(handler)
security_logger.propagate = False
security_logger.setLevel(logging.DEBUG)  # log levels: critical < error < warning(20) < info(30) < debug


def configure_auth(flask_app: Flask, database: object, method_decorators: object):
    """_summary_
    Called on server start by api_logic_server_run to 
    
    - initialize jwt
    - establish Flask end points for login.

    Args:
        flask_app (Flask): _description_
        database (object): _description_
        method_decorators (object): _description_

    Returns:
        _type_: (no return)
    """
    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config["JWT_SECRET_KEY"] = "ApiLogicServerSecret"  # Change this!
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=222)  # th longer exp
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(flask_app)
    
    @flask_app.route("/auth/login", methods=["POST"])
    def login():
        """
        Post id/password, returns token to be placed in header of subsequent requests.

        Returns:
            string: access token
        """
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = authentication_provider.get_user(username, password)  # val - use auth_provider
        if not user:  # FIXME or not user.check_password(password): avoid model method? += provider?
            return jsonify("Wrong username or password"), 401

        access_token = create_access_token(identity=user)  # serialize and encode
        return jsonify(access_token=access_token)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return authentication_provider.get_user(identity, "")  # val - use auth_provider

    @flask_app.route("/auth/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    method_decorators.append(jwt_required())
    security_logger.info("authentication loaded")

