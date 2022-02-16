# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import CHAR, Column, Computed, Integer, SmallInteger, String, Unicode, text
from sqlalchemy.dialects.mssql import MONEY
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
from safrs import SAFRSBase

import safrs

Base = declarative_base()
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

# from sqlalchemy.dialects.mysql import *
########################################################################################################################

# use_model test, these models from ApiLogicServer/tests/use-model.py

class DataType(SAFRSBase, Base):
    __tablename__ = 'DataTypes'

    Key = Column(Unicode(10), primary_key=True)
    char_type = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    varchar_type = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    allow_client_generated_ids = True


class Employee(SAFRSBase, Base):
    __tablename__ = 'Employees'

    Id = Column(Integer, primary_key=True, server_default=text("0"))
    Name = Column(Unicode(50))
    Location = Column(Unicode(50))


class PlusTable(SAFRSBase, Base):
    __tablename__ = 'Plus+Table'

    Id = Column(Integer, primary_key=True, server_default=text("0"))
    Name = Column(Unicode(50))
    Location = Column(Unicode(50))
    QtyAvailable = Column(SmallInteger)
    UnitPrice = Column(MONEY)
    InventoryValue = Column(MONEY, Computed('([QtyAvailable]*[UnitPrice])', persisted=False))


# from database import customize_models
