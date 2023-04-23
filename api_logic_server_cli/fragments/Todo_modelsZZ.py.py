# coding: utf-8
from sqlalchemy import Column, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding

from safrs import SAFRSBase
from flask_login import UserMixin
import safrs
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
BaseTodo = declarative_base()
metadata = BaseTodo.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *
########################################################################################################################



t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Todo(SAFRSBase, BaseTodo, db.Model, UserMixin):
    __tablename__ = 'todos'
    _s_collection_name = 'Todo-Todo'
    __bind_key__ = 'Todo'

    task = Column(Text)
    category = Column(Text)
    date_added = Column(Text)
    date_completed = Column(Text)
    status = Column(Integer)
    position = Column(Integer)
    id = Column(Integer, primary_key=True)
