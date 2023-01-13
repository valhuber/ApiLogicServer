import logging, sys
from flask import Flask
from security import declare_security  # activate security
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from datetime import timedelta
import database.authentication_models as authentication_models


app_logger = logging.getLogger('api_logic_server_app')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
app_logger.addHandler(handler)
app_logger.propagate = True

app_logger.setLevel(logging.INFO)  # log levels: critical < error < warning(20) < info(30) < debug


def configure_auth(flask_app: Flask, database: object, method_decorators: object):
    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config["JWT_SECRET_KEY"] = "ApiLogicServerSecret"  # Change this!
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=222)  # th longer exp
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(flask_app)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return authentication_models.User.query.filter_by(id=identity).one_or_none()  # th currently re-reading
    
    @flask_app.route("/auth/login", methods=["POST"])
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = authentication_models.User.query.filter_by(id=username).one_or_none()
        if not user:  # FIXME or not user.check_password(password): avoid model method?
            return jsonify("Wrong username or password"), 401

        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)

    @flask_app.route("/auth/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    method_decorators.append(jwt_required())
    app_logger.info("Declare Security complete - security/declare_security.py"
        + f' -- {len(database.authentication_models.metadata.tables)} tables loaded')

