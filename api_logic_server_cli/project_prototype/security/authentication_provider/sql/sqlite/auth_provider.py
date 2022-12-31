from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider
import sqlalchemy as sqlalchemy
import database.authentication_models as authentication_models
from flask import Flask
import safrs

# **********************
# sql auth provider
# **********************

db = safrs.DB         # Use the safrs.DB, not db!
session = db.session  # sqlalchemy.orm.scoping.scoped_session

class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def get_user(id: str, password: str) -> object:
        """
        Must return a row object with attributes name and role_list
        role_list is a list of row objects with attribute name

        oops - password missing TODO

        TP: id / pwd or token

        row object is a SQLAlchemy row (could have been a DotMap)
        """

        user = session.query(authentication_models.User).filter(authentication_models.User.id == id).one()
        return user


