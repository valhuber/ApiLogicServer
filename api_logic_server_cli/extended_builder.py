import os

from sqlalchemy.sql import text
from typing import List
import sqlalchemy

print("Extended builder")


class DotDict(dict):
    """ dot.notation access to dictionary attributes """
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TvfBuilder(object):

    def __init__(self, db_url, project_directory):

        self.db_url = db_url
        self.project_directory = project_directory

        self.number_of_services = 0

        self.tvf_contents = """# coding: utf-8
from sqlalchemy import Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI, jsonapi_rpc
from safrs import JABase, DB

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

"""

    def build_tvf_class(self, cols: List[DotDict]):
        self.tvf_contents += f't_{cols[0].Function} = Table(  # define result for {cols[0].Function}\n'
        self.tvf_contents += f'\t"{cols[0].Function}", metadata,\n'
        col_count = 0
        for each_col in cols:
            self.tvf_contents += f'\tColumn("{each_col.Column}", '
            if each_col.Data_Type == "int":
                self.tvf_contents += f'Integer)'
            elif each_col.Data_Type == "nvarchar":
                self.tvf_contents += f'String({each_col.Char_Max_Length}))'
            else:  # TODO - support additional data types
                self.tvf_contents += f'String(8000))'
            col_count += 1
            if col_count < len(cols):
                self.tvf_contents += ",\n"
            else:
                self.tvf_contents += ")\n"
        self.tvf_contents += f'\n\n'

    def build_tvf_service(self, args: List[DotDict]):
        self.tvf_contents += f'class {args[0].ObjectName}(JABase):\n'
        self.tvf_contents += f"\t''' define service for {args[0].ObjectName} '''\n"
        self.tvf_contents += f"\t@staticmethod\n"
        self.tvf_contents += f"\t@jsonapi_rpc(http_methods=['POST'], valid_jsonapi=False)\n"

        # def udfEmployeeInLocationWithName(location, Name):
        self.tvf_contents += f"\tdef {args[0].ObjectName}("
        arg_number = 0
        for each_arg in args:
            self.tvf_contents += each_arg.ParameterName[1:]
            arg_number += 1
            if arg_number < len(args):
                self.tvf_contents += ", "
        self.tvf_contents += "):\n"
        self.tvf_contents += f'\t\t"""\n'
        self.tvf_contents += f"\t\tdescription: expose TVF - {args[0].ObjectName}\n"
        self.tvf_contents += f"\t\targs:\n"
        for each_arg in args:
            self.tvf_contents += f'\t\t\t{each_arg.ParameterName[1:]}\n'
        self.tvf_contents += f'\t\t"""\n'

        # sql_query = db.text("SELECT * FROM udfEmployeeInLocationWithName(:location, :Name)")
        self.tvf_contents += f'\t\tsql_query = db.text("SELECT * FROM {args[0].ObjectName}('
        arg_number = 0
        for each_arg in args:
            self.tvf_contents += ":" + each_arg.ParameterName[1:]
            arg_number += 1
            if arg_number < len(args):
                self.tvf_contents += ", "
        self.tvf_contents += ')")\n'

        # query_result = db.engine.execute(sql_query, location=location, Name=Name)
        self.tvf_contents += f'\t\tquery_result = db.engine.execute(sql_query, '  # arg=arg)\n'
        arg_number = 0
        for each_arg in args:
            self.tvf_contents += each_arg.ParameterName[1:] + "=" + each_arg.ParameterName[1:]
            arg_number += 1
            if arg_number < len(args):
                self.tvf_contents += ", "
        self.tvf_contents += ")\n"
        self.tvf_contents += f'\t\tresult = query_result.fetchall()\n'
        self.tvf_contents += '\t\treturn {"result" : list(result[0])}\n'
        self.tvf_contents += f'\n\n'

    def write_tvf_file(self):
        """ write tvf_contents -> api/tvf.py """
        tvf_file = open(self.project_directory + '/api/tvf.py', 'w')
        tvf_file.write(self.tvf_contents)
        tvf_file.close()

    def run(self):
        """ call by ApiLogicServer CLI -- scan db_url schema for TVFs, create api/tvf.py
                for each TVF:
                    class t_<TVF_Name> -- the model
                    class <TVF_Name>   -- the service

        """
        print(f'extended_builder.extended_builder("{self.db_url}", "{self.project_directory}"')

        cols_sql = "" \
                   "SELECT TABLE_CATALOG AS [Database], TABLE_SCHEMA AS [Schema], TABLE_NAME AS [Function], " \
                    "COLUMN_NAME AS [Column], DATA_TYPE AS [Data_Type], CHARACTER_MAXIMUM_LENGTH AS [Char_Max_Length] " \
                    "FROM INFORMATION_SCHEMA.ROUTINE_COLUMNS " \
                    "WHERE TABLE_NAME IN " \
                        "(SELECT ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'FUNCTION' AND DATA_TYPE = 'TABLE') " \
                   "ORDER BY TABLE_NAME, COLUMN_NAME;"
        engine = sqlalchemy.create_engine(self.db_url, echo=False)  # sqlalchemy sqls...
        cols = []
        current_table_name = ""
        with engine.connect() as connection:
            result = connection.execute(text(cols_sql))
            for row_dict in result:
                row = DotDict(row_dict)
                print(f'col row: {row}, database: {row.Database}')
                function_name = row.Function
                if function_name != current_table_name:
                    if len(cols) > 0:
                        self.number_of_services += 1
                        self.build_tvf_class(cols)
                    current_table_name = function_name
                    cols = []
                cols.append(row)

        # connection.close()
        engine.dispose()  # TODO not sure what this is, but fixed some no-result errors

        if len(cols) > 0:
            self.number_of_services += 1
            self.build_tvf_class(cols)

        args_sql = "SELECT " \
                   "SCHEMA_NAME(SCHEMA_ID) AS [Schema]" \
                   ",SO.name AS [ObjectName]" \
                   ",SO.Type_Desc AS [ObjectType (UDF/SP)]" \
                   ",P.parameter_id AS [ParameterID]" \
                   ",P.name AS [ParameterName]" \
                   ",TYPE_NAME(P.user_type_id) AS [ParameterDataType]" \
                   ",P.max_length AS [ParameterMaxBytes]" \
                   ",P.is_output AS [IsOutPutParameter]" \
                   " FROM sys.objects AS SO" \
                   " INNER JOIN sys.parameters AS P ON SO.OBJECT_ID = P.OBJECT_ID" \
                   " ORDER BY [Schema], SO.name, P.parameter_id"
        args = []
        current_object_name = ""

        with engine.connect() as connection:
            result = connection.execute(text(args_sql))
            for row_dict in result:
                row = DotDict(row_dict)
                print(f'arg row: {row}, database: {row.Database}')
                object_name = row.ObjectName
                if object_name != current_object_name:
                    if len(args) > 0:
                        self.build_tvf_service(args)
                    current_object_name = object_name
                    args = []
                args.append(row)
        # connection.close()
        if len(args) > 0:
            self.build_tvf_service(args)

        self.tvf_contents += f'#  {self.number_of_services} services created.\n'

        self.write_tvf_file()


def extended_builder(db_url, project_directory):
    """ called by ApiLogicServer CLI -- scan db_url schema for TVFs, create api/tvf.py
            for each TVF:
                class t_<TVF_Name> -- the model
                class <TVF_Name>   -- the service
        args
            db_url - use this to open the target database, e.g. for meta data
            project_directory - the created project... create / alter files here
    """
    print(f'extended_builder.extended_builder("{db_url}", "{project_directory}"')
    tvf_builder = TvfBuilder(db_url, project_directory)
    tvf_builder.run()
