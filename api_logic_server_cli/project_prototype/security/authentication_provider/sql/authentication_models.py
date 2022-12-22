# coding: utf-8
from sqlalchemy import Column, String, ForeignKey, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://valhuber.github.io/ApiLogicServer/Project-Rebuild/#rebuilding

from safrs import SAFRSBase

import safrs
db = SQLAlchemy()
BaseSecurity = declarative_base()
metadata = BaseSecurity.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *
########################################################################################################################


class Role(SAFRSBase, BaseSecurity, db.Model, UserMixin):
    __tablename__ = 'Role'
    __bind_key__ = 'security_bind'

    name = Column(String(64), primary_key=True)
    allow_client_generated_ids = True

    UserRoleList = relationship('UserRole', cascade_backrefs=True, backref='Role')


class User(SAFRSBase, BaseSecurity, db.Model, UserMixin):
    __tablename__ = 'User'
    __bind_key__ = 'security_bind'

    name = Column(String(128))
    notes = Column(Text)
    client_id = Column(Integer)
    id = Column(String(64), primary_key=True, unique=True)
    username = Column(String(128))
    email = Column(String(128))
    password_hash = Column(String(200))
    allow_client_generated_ids = True

    ApiList = relationship('Api', cascade_backrefs=True, backref='owner')
    UserRoleList = relationship('UserRole', cascade_backrefs=True, backref='user')


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Api(SAFRSBase, BaseSecurity, db.Model, UserMixin):
    __tablename__ = 'Apis'
    __bind_key__ = 'security_bind'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    connection_string = Column(String(64))
    owner_id = Column(ForeignKey('User.id'))

    # see backref on parent: owner = relationship('User', cascade_backrefs=True, backref='ApiList')


class UserRole(SAFRSBase, BaseSecurity, db.Model, UserMixin):
    __tablename__ = 'UserRole'
    __bind_key__ = 'security_bind'

    user_id = Column(ForeignKey('User.id'), primary_key=True)
    notes = Column(Text)
    role_name = Column(ForeignKey('Role.name'), primary_key=True)
    allow_client_generated_ids = True

    # see backref on parent: Role = relationship('Role', cascade_backrefs=True, backref='UserRoleList')
    # see backref on parent: user = relationship('User', cascade_backrefs=True, backref='UserRoleList')
