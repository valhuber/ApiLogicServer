#!/usr/bin/env python3
"""
Run the app:
gunicorn -w 4 admin-api:app -b 0.0.0.0:5656  --threads 5 --error-logfile - --access-logfile - --reload

Authentication uses both bearer jwt tokens and cookies.
Tokens for API authentication
Cookies because it's easier to use the swagger
"""
import logging
import time
import flask_login as login
import subprocess
from flask_login import UserMixin, LoginManager
from flask import Flask, request, has_request_context, abort, g, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc, jsonapi_attr
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from pathlib import Path

db = SQLAlchemy()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class User(SAFRSBase, db.Model, UserMixin):
    """
    description: Users
    """

    __tablename__ = "Users"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    username = db.Column(db.String, default="", unique=True)
    email = db.Column(db.String, default="")
    _password_hash = db.Column(db.String(200)) # underscore prefix means it's hidden from serialization
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
        return {"msg" : "password set"}

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
    def login_user(cls, username=None, password=None):
        """
            args:
                username: user
                password: password
        """
        user = getattr(g, "user", None)
        if user is None:
            user = cls.query.filter_by(username=username).one_or_none()
            if not user:
                abort(403)
            result = user.verify_password(password)
            if result:
                login.login_user(user)
                g.user = user
        
        return user.generate_auth_token()
        
    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def generate_auth_token(self, expiration=48*60*60):
        """
            description: Generate a token that can be used to authenticate this user
            ---
            :param expiration: expiration time in seconds
            :return: token string
        """
        if login.current_user != self:
            abort(403)
        srlz = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        result = srlz.dumps({"id": self.id, "iat" : time.time()})
        return {"auth_token" : result.decode('utf-8')}

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
        srlz = Serializer(current_app.config["SECRET_KEY"])
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
        
    def __repr__(self):
        """
        """
        return f"{self.username} - {self.id}"


class Api(SAFRSBase, db.Model):
    """
    description: Api configuration info
    """

    __tablename__ = "Apis"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    prefix = db.Column(db.String, default="")
    port = db.Column(db.Integer, default=5656)
    hostname = db.Column(db.String, default="localhost")
    connection_string = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey("Users.id"))
    owner = db.relationship("User", back_populates="apis")
    
    @staticmethod
    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def test_conn(connection_string = ""):
        print(connection_string)
        from sqlalchemy import create_engine, inspect
        try:
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                pass
            insp = inspect(engine)
            tablenames = "\n".join(insp.get_table_names())
            return f"# Tables:\n{tablenames}" if tablenames else "# Empty DB"
        except Exception as exc:
            return str(exc)


    @jsonapi_rpc(http_methods=["POST"], valid_jsonapi=False)
    def generate():
        output  = "Creating API"
        als_args = {
            "--project_name" : self.name,
            "--db_url" : self.connection_string,
            "--port" : str(self.port),
            "--host" : self.hostname
        }
        proc_args = ['ApiLogicServer','create']
        for a, v in als_args.items():
            proc_args += [f'{a}={v}']
        output += " ".join(proc_args)
        print(output)
        process = subprocess.run(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output += str(process.stdout)
        output += "\n\n"
        output += str(process.stderr)
        print('OUT '*40)
        print(output)
        return output
    
    @jsonapi_attr
    def path(self):
        return f"{self.name}"


def create_app(config_filename=None, host="localhost", port="5656", app_prefix="/admin"):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:////tmp/4LSBE.sqlite.admin",
                      SESSION_COOKIE_SAMESITE="Strict",
                      SECRET_KEY = "Change me for PROD !!",
                      SQLALCHEMY_TRACK_MODIFICATIONS=False,
                      FLASK_DEBUG=True,
                      SQLALCHEMY_COMMIT_ON_TEARDOWN=True)

    db.init_app(app)
    app.db = db
    # address where the api will be hosted, change this if you're not running the app on localhost!
    login_manager = LoginManager(app)

    _insecure_views = ["swagger_ui.show", "swagger", "api.Users.login_user"]

    @app.before_request
    def verify_login():
        
        if request.method == "OPTIONS":
            return
        
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
        
        if request.endpoint in _insecure_views:
            # endpoints in the _insecure_views lists are ok
            return
        
        log.debug(f"Endpoint: {request.endpoint}")
        
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
        engine_container = db.get_engine(app)    
        db.session.close()
        engine_container.dispose()
        
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

    def init_user():
        user = db.session.query(User).filter_by(username="admin").one_or_none()
        if not user:
            print('Creating admin user')
            user = User(username = "admin", _password_hash = pwd_context.encrypt("p"))
            try:# this try/except is a stupid workaround because I didn't implemented sessions properly
                # and it behaves differently between werkzeug and gunicorn
                db.session.add(user)
                db.session.commit()
            except Exception as exc:
                print('Commit Failed ', exc)
            

    with app.app_context():
        db.create_all()
        init_user()
    
    return app

if __name__ == "__main__":
    host = "localhost"
    port = 5656
    app = create_app(host=host)
    app.run(host=host, port=5656)