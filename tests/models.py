# coding: utf-8
from sqlalchemy import CHAR, Column, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
from safrs import SAFRSBase

import safrs
db = safrs.DB

Base = db.Model
metadata = Base.metadata

NullType = db.String  # datatype fixup
TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mysql import *

########################################################################################################################



class DataType(SAFRSBase, Base):
    __tablename__ = 'DataTypes'

    Key = Column(Unicode(10), primary_key=True)
    char_type = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    varchar_type = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))


class Employee(SAFRSBase, Base):
    __tablename__ = 'Employees'

    Id = Column(Integer, primary_key=True)
    Name = Column(Unicode(50))
    Location = Column(Unicode(50))


# ALTERED -- exclude:
# from database import models_ext
