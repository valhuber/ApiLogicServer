"""
System support for login / authentication.

Applications POST to login to obtain an access token,
which they provide in the header of subsequent requests.

e.g. 
def login():
    post_uri = 'http://localhost:5656/auth/login'
    post_data = {"username": "_user_","password": "_password_"}
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
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required as jwt_required_ori
from flask_jwt_extended import create_access_token
from datetime import timedelta
from functools import wraps
import config
from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider

authentication_provider : Abstract_Authentication_Provider = config.Config.SECURITY_PROVIDER  # type: ignore

security_logger = logging.getLogger(__name__)

JWT_EXCLUDE = 'jwt_exclude'

def jwt_required(*args, **kwargs):
    from flask import request
    _jwt_required_ori = jwt_required_ori(*args, **kwargs)
    def _wrapper(fn):
        if request.endpoint == 'api.authentication-User.login':
            return fn
        return _jwt_required_ori(fn)
    return _wrapper


def configure_auth(flask_app: Flask, database: object, method_decorators: list[object]):
    """
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
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=222)  #  change as you see fit
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(flask_app)
    
    @flask_app.route("/api/auth/login", methods=["POST"])
    def login():
        """
        Post id/password, returns token to be placed in header of subsequent requests.

        Returns:
            string: access token
        """
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = authentication_provider.get_user(username, password)
        if not user or not user.check_password(password):
            return jsonify("Wrong username or password"), 401

        access_token = create_access_token(identity=user)  # serialize and encode
        return jsonify(access_token=access_token)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return authentication_provider.get_user(identity, "")

    method_decorators.append(jwt_required())
    security_logger.info("\nAuthentication loaded -- api calls now require authorization header")
