#!/usr/bin/env python3
"""
"""
import sys
import logging
import safrs
import time
import datetime
import flask_login as login
from flask_login import UserMixin, LoginManager
from flask import Flask, request, has_request_context, abort, g
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

"""
As of release 4.20, this file is for future expansion, not currently used.
"""

db = SQLAlchemy()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class User(SAFRSBase, db.Model, UserMixin):
    """
    description: Users
    """

    __tablename__ = "Users"
    __bind_key__ = 'admin'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    username = db.Column(db.String, default="", unique=True)
    email = db.Column(db.String, default="")
    _password_hash = db.Column(db.String(200))
    apis = db.relationship("Api", back_populates="owner", lazy="dynamic")

    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def hash_password(self, password):
        """
            args:
                password: password
            ---
            :param password: plain-text password to be hashed
            :return: hashed password

            Set the password hash
            >> User.query.filter(User.username == 'admin').first().hash_password('newpass')
        """
        if login.current_user != self:
            abort(403)
        log.info(f"Changing password for {self}")
        self._password_hash = pwd_context.encrypt(password)
        return {"msg": "password set"}

    def verify_password(self, password):
        """
            Hash the password and compare it to the stored hash
            or
            authenticate the user with radius
            :param password:
            :return: True or False depending on whether the password matched the hashed password or radius authenticatipn was successful
        """
        if password and self._password_hash and pwd_context.verify(password, self._password_hash):
            login.login_user(self)
            return True

        log.warning(f"Password verification failed for {self.username} - {password}")
        return False

    @classmethod
    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def login_user(cls, username, password):
        """
            args:
                username: user
                password: password
        """
        result = False
        user = cls.query.filter_by(username=username).one_or_none()
        if user:
            result = user.verify_password(password)
            if result:
                login.login_user(user)
                g.user = user

        return user.generate_auth_token()

    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def generate_auth_token(self, expiration=15000000):
        """
            description: Generate a token that can be used to authenticate this user
            ---
            :param expiration: expiration time in seconds
            :return: token string
        """
        if login.current_user != self:
            abort(403)
        srlz = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        result = srlz.dumps({"id": self.id, "iat": time.time()})
        return {"auth_token": result.decode('utf-8')}

    @classmethod
    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def verify_auth_token(cls, token):
        """
            description: Verify an authentication token
            args:
                token : token_val
            ---
            :param token: token, generated by `generate_auth_token`
            :return: User object if the token is valid, None otherwise
        """
        srlz = Serializer(app.config["SECRET_KEY"])
        try:
            data = srlz.loads(token)
        except SignatureExpired:
            log.error("SignatureExpired")
            return None  # valid token, but expired
        except BadSignature:
            log.error("BadSignature")
            return None  # invalid token

        user = cls.query.get(data["id"])
        if not user:
            return False
        return user

    @classmethod
    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def logout(self):
        login.logout_user()

    def __repr__(self) -> str:
        """
        """
        return f"{self.username} - {self.id}"


class Api(SAFRSBase, db.Model):
    """
    description: Api configuration info
    """

    __tablename__ = "Apis"
    __bind_key__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    connection_string = db.Column(db.String, default="")
    owner_id = db.Column(db.String, db.ForeignKey("Users.id"))
    owner = db.relationship("User", back_populates="apis")


# create the api endpoints
def create_admin_api(app, host="localhost", port=5000, api_prefix="/admin-api"):
    api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix)
    api.expose_object(User)
    api.expose_object(Api)
    api.expose_als_schema(api_root=f"//{host}:{port}{api_prefix}")
    print(f"Created API: http://{host}:{port}/{api_prefix}")


def create_app(config_filename=None, host="localhost"):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:////tmp/4LSBE.sqlite",
                      SESSION_COOKIE_SAMESITE="Lax",  # <<--- Strict
                      SQLALCHEMY_BINDS={'admin': 'sqlite:////tmp/4LSBE.sqlite.admin'},
                      SECRET_KEY="Change me !!",
                      SQLALCHEMY_TRACK_MODIFICATIONS=False,
                      FLASK_DEBUG=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.create_all(bind='admin')
        create_admin_api(app, port=port, host=host)
        user = db.session.query(User).filter_by(username="admin").one_or_none()
        if not user:
            user = User(username="admin")
            db.session.commit()
        # db.session.commit()

    return app


# address where the api will be hosted, change this if you're not running the app on localhost!
host = "localhost"
port = 5656
app = create_app(host=host)
login_manager = LoginManager(app)

_insecure_views = ["swagger_ui.show", "swagger", "api.Users.login_user"]


@app.before_request
def verify_login():
    if request.endpoint in _insecure_views:
        # endpoints in the _insecure_views lists are ok
        return
    if request.method == "OPTIONS":
        return

    log.debug(f"Endpoint: {request.endpoint}")

    # check cookie-based authentication
    if login.current_user and login.current_user.is_authenticated:
        g.user = login.current_user
        return

    # check token-based authentication
    auth_header = request.headers.get("Authorization", None)

    if auth_header and auth_header.upper().startswith("BEARER "):
        token = auth_header.split()[1]
        user = User.verify_auth_token(token)
        if user:
            login.login_user(user)
            g.user = user
            return

    log.warning("Auth error")
    abort(403)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.after_request
def per_request_callbacks(response):
    """
        Execute the request callbacks
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
        Cleanup when the session is terminated
    """

    if exception:
        db.session.rollback()
    db.session.remove()


if __name__ == "__main__":
    app.run(host=host)
