"""Flask configuration variables."""
from os import environ, path
from pathlib import Path
import os
import typing
from dotenv import load_dotenv
import logging
from enum import Enum

#  for complete flask_sqlachemy config parameters and session handling,
#  read: file flask_sqlalchemy/__init__.py AND flask/config.py
'''
app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
app.config.setdefault('SQLALCHEMY_BINDS', None)
app.config.setdefault('SQLALCHEMY_NATIVE_UNICODE', None)
app.config.setdefault('SQLALCHEMY_ECHO', False)
app.config.setdefault('SQLALCHEMY_RECORD_QUERIES', None)
app.config.setdefault('SQLALCHEMY_POOL_SIZE', None)
app.config.setdefault('SQLALCHEMY_POOL_TIMEOUT', None)
app.config.setdefault('SQLALCHEMY_POOL_RECYCLE', None)
app.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', None)
app.config.setdefault('SQLALCHEMY_COMMIT_ON_TEARDOWN', False)
'''

class ExtendedEnum(Enum):
    """
    enum that supports list() to print allowed values

    Thanks: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class OptLocking(ExtendedEnum):
    IGNORED = "ignored"
    OPTIONAL = "optional"
    REQUIRED = "required"


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "default.env"))
app_logger = logging.getLogger('api_logic_server_app')


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    DEBUG = environ.get("DEBUG")

    running_at = Path(__file__)
    project_abs_dir = running_at.parent.absolute()

    # Database
    SQLALCHEMY_DATABASE_URI : typing.Optional[str] = f"replace_db_url"
    # override SQLALCHEMY_DATABASE_URI here as required

    app_logger.debug(f'config.py - SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}')

    # as desired, use env variable: export SQLALCHEMY_DATABASE_URI='sqlite:////Users/val/dev/servers/docker_api_logic_project/database/db.sqliteXX'
    if os.getenv('SQLALCHEMY_DATABASE_URI'):  # e.g. export SECURITY_ENABLED=true
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
        app_logger.debug(f'.. overridden from env variable: {SQLALCHEMY_DATABASE_URI}')

    SECURITY_ENABLED = False  # you must also: ApiLogicServer add-db --db_url=auth --bind_key=authentication
    SECURITY_PROVIDER = None
    if os.getenv('SECURITY_ENABLED'):  # e.g. export SECURITY_ENABLED=true
        security_export = os.getenv('SECURITY_ENABLED')  # type: ignore # type: str
        security_export = security_export.lower()  # type: ignore
        if security_export in ["false", "no"]:  # NO SEC
            SECURITY_ENABLED = False
        else:
            SECURITY_ENABLED = True
        app_logger.debug(f'Security .. overridden from env variable: {SECURITY_ENABLED}')
    if SECURITY_ENABLED:
        from security.authentication_provider.sql.sqlite.auth_provider import Authentication_Provider
        SECURITY_PROVIDER = Authentication_Provider
        app_logger.debug(f'config.py - security enabled')
    else:
        app_logger.info(f'config.py - security disabled')

    # Begin Multi-Database URLs (from ApiLogicServer add-db...)

    # End Multi-Database URLs (from ApiLogicServer add-db...)

    # SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = False

    OPT_LOCKING = "replace_opt_locking"
    if os.getenv('OPT_LOCKING'):  # e.g. export OPT_LOCKING=required
        opt_locking_export = os.getenv('OPT_LOCKING')  # type: ignore # type: str
        opt_locking = opt_locking_export.lower()  # type: ignore
        if opt_locking in OptLocking.list():
            OPT_LOCKING = opt_locking
        else:
            print(f'\n{__name__}: Invalid OPT_LOCKING.\n..Valid values are {OptLocking.list()}')
            exit(1)
        app_logger.debug(f'Opt Locking .. overridden from env variable: {OPT_LOCKING}')

