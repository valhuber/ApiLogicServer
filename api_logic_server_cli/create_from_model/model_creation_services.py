import ast
import logging
import traceback
from os.path import abspath
import importlib.util
import sys
import os
from typing import NewType
import sqlalchemy
import sqlalchemy.ext
from sqlalchemy import MetaData
import inspect
import importlib
from flask import Flask

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


class CreateFromModel(object):
    """
    Iterate over model

    Create ui/basic_web_app/views.py and api/expose_api_models.py
    """

    result_views = ""
    result_apis = ""

    _favorite_names_list = []  #: ["name", "description"]
    """
        array of substrings used to find favorite column name

        command line option to override per language, db conventions

        eg,
            name in English
            nom in French
    """
    _non_favorite_names_list = []
    non_favorite_names = "id"

    _indent = "   "

    num_pages_generated = 0
    num_related = 0

    def __init__(self,
                 project_directory: str ="~/Desktop/my_project",
                 abs_db_url: str = "sqlite:///nw.sqlite",
                 db_url: str="sqlite:///nw.sqlite",
                 host: str = "localhost",
                 port: str = "5000",
                 flask_appbuilder: bool=True,
                 react_admin: bool=True,
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id",
                 version: str = "0.0.0"):
        self.project_directory = self.get_windows_path_with_slashes(project_directory)
        self.abs_db_url = abs_db_url  # actual (not relative, reflects nw copy, etc)
        self.db_url = db_url  # the original cli parameter
        self.host = host
        self.port = port
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_names = non_favorite_names
        self.flask_appbuilder = flask_appbuilder
        self.react_admin = react_admin
        self.version = version

        self.table_to_class_map = {}
        """ keys are table[.column], values are class / attribute """
        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

    @staticmethod
    def get_windows_path_with_slashes(url: str) -> str:
        """ idiotic fix for windows (\ --> \\\\)
        https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file"""
        full_path = os.path.abspath(url)
        result = full_path.replace('\\', '\\\\')
        if os.name == "nt":  # windows
            result = full_path.replace('/', '\\')
        return result

    @staticmethod
    def create_app(config_filename=None, host="localhost"):
        import safrs

        app = Flask("API Logic Server")
        import api_logic_server_cli.config as app_logic_server_config
        app.config.from_object(app_logic_server_config.Config)
        db = safrs.DB
        db.init_app(app)
        return app

    def add_table_to_class_map(self, orm_class):
        """ given class, find table (hide your eyes), add table/class to table_to_class_map """
        orm_class_info = orm_class[1]
        query = str(orm_class_info.query)[7:]
        table_name = query.split('.')[0]
        table_name = table_name.strip('\"')
        self.table_to_class_map.update({table_name: orm_class[0]})
        pass  # for debug

    def get_class_for_table(self, table_name) -> str:
        """ given table_name, return its class_name from table_to_class_map """
        if table_name in self.table_to_class_map:
            return self.table_to_class_map[table_name]
        else:
            log.debug("skipping view: " + table_name)
            return None

    def find_meta_data(self, cwd: str, log_info: bool=False) -> MetaData:
        """     Find Metadata by importing model, or (failing that), db

        a_cmd should be cli folder, e.g. '/Users/val/dev/ApiLogicServer/api_logic_server_cli'

            Metadata contains definition of tables, cols & fKeys (show_related)
            It can be obtained from db, *or* models.py; important because...
                Many DBs don't define FKs into the db (e.g. nw.db)
                Instead, they define "Virtual Keys" in their model files
                To find these, we need to get Metadata from models, not db
            So, we need to
                1. Import the models, via a location-relative dynamic import (warning - not trivial)
                2. Find the Metadata from the imported models:
                    a. Find cls_members in models module
                    b. Locate first user model, use its metadata property
            #  view_metadata = models.Order().metadata  # class var, non ab_

            All this is doing is:
                    from <cwd>/database import models(.py) as models

        """

        conn_string = None
        do_dynamic_load = True
        project_abs_path = abspath(self.project_directory)

        if do_dynamic_load:
            """
                a_cwd -- see ApiLogicServer/prototype for structure

                credit: https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
            """
            sys_path = str(sys.path)

            self.app = self.create_app(host=self.host)
            self.app.config.SQLALCHEMY_DATABASE_URI = self.abs_db_url
            self.app.app_context().push()  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
            if log_info:
                print(f'.. ..Dynamic model import using sys.path: {project_abs_path + "/database"}')  # str(sys.path))
            model_imported = False
            sys.path.insert(0, project_abs_path + "/database")  #  e.g., adds /Users/val/Desktop/my_project/database
            try:
                # models =
                importlib.import_module('models')
                model_imported = True
            except:
                print("\n===> ERROR - Dynamic model import failed - project run will fail")
                traceback.print_exc()
                pass  # try to continue to enable manual fixup

            # sys.path.insert(0, a_cwd)  # success - models open
            # config = importlib.import_module('config')
            conn_string = self.app.config.SQLALCHEMY_DATABASE_URI
        else:  # using dynamic loading (above), remove this when stable (TODO)
            import models
            conn_string = "sqlite:///nw/nw.db"

        orm_class = None
        metadata = None
        if not model_imported:
            print('.. ..Creation proceeding to enable manual database/models.py fixup')
            print('.. .. See https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#manual-model-repair')
        else:
            try:
                cls_members = inspect.getmembers(sys.modules["models"], inspect.isclass)
                for each_cls_member in cls_members:
                    each_class_def_str = str(each_cls_member)
                    #  such as ('Category', <class 'models.Category'>)
                    if ("'models." in str(each_class_def_str) and
                            "Ab" not in str(each_class_def_str)):
                        orm_class = each_cls_member
                        self.add_table_to_class_map(orm_class)
                if (orm_class is not None):
                    if log_info:
                        print(f'.. ..Dynamic model import successful '
                              f'({len(self.table_to_class_map)} classes'
                              f') -'
                              f' getting metadata from {str(orm_class)}')
                    metadata = orm_class[1].metadata

                self.engine = sqlalchemy.create_engine(conn_string)
                self.connection = self.engine.connect()
            except:
                print("\n===> ERROR - Unable to introspect model classes")
                traceback.print_exc()
                pass

        if metadata is None:  # this recovery fails to find meta, but should continue to enable model repair
            # print('.. Using db for meta (models not found)')
            # print('.. See https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#manual-model-repair')
            metadata = MetaData()
        else:
            metadata.reflect(bind=self.engine, resolve_fks=True)
        self.metadata = metadata

    def zz_generate_module_imports(self) -> str:  # TODO drop
        """
            Returns a string of views.py imports

            (first portion of `views.py` file)
        """
        result = "from flask_appbuilder import ModelView\n"
        result += "from flask_appbuilder.models.sqla.interface "\
            "import SQLAInterface\n"
        result += "from . import appbuilder, db\n"
        result += "from database.models import *\n"
        return result

    def list_columns(self, a_table_def: MetaDataTable) -> str:
        """
            Example: list_columns = ["InvoiceLineId", "Track.Name", "Invoice.InvoiceId", "UnitPrice", "Quantity"]

            Parameters
                a_table_def TableModelInstance

            Returns
                list_columns = [...] - favorites / joins first, not too many
        """
        return self.gen_columns(a_table_def, "list_columns = [", 2, 5, 0)

    def get_list_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.list_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def show_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "show_columns = [", 99, 999, 999)

    def get_show_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.show_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def edit_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "edit_columns = [", 99, 999, 999)

    def get_edit_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.edit_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def add_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "add_columns = [", 99, 999, 999)

    def get_add_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.add_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def query_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "query_columns = [", 99, 999, 999)

    def get_query_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.query_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def gen_columns(self,
                    a_table_def: MetaDataTable,
                    a_view_type: str,
                    a_max_joins: int,
                    a_max_columns: int,
                    a_max_id_columns: int):
        """
        Generates statements like:

            list_columns =["Id", "Product.ProductName", ... "Id"]

            This is *not* simply a list of columms:
                1. favorite column first,
                2. then join (parent) columns, with predictive joins
                3. and id fields at the end.

            Parameters
                argument1 a_table_def - TableModelInstance
                argument2 a_view_type - str like "list_columns = ["
                argument3 a_max_joins - int max joins (list is smaller)
                argument4 a_max_columns - int how many columns (")
                argument5 a_id_columns - int how many "id" columns (")

            Returns
                string like list_columns =["Name", "Parent.Name", ... "Id"]
        """
        result = a_view_type
        columns = a_table_def.columns
        id_column_names = set()
        processed_column_names = set()
        result += ""
        if a_table_def.name == "OrderDetail":
            result += "\n"  # just for debug stop

        favorite_column_name = self.favorite_column_name(a_table_def)
        column_count = 1
        result += '"' + favorite_column_name + '"'  # todo hmm: emp territory
        processed_column_names.add(favorite_column_name)

        predictive_joins = self.predictive_join_columns(a_table_def)
        if "list" in a_view_type or "show" in a_view_type:
            # alert - prevent fab key errors!
            for each_join_column in predictive_joins:
                column_count += 1
                if column_count > 1:
                    result += ", "
                result += '"' + each_join_column + '"'
                if column_count > a_max_joins:
                    break
        for each_column in columns:
            if each_column.name in processed_column_names:
                continue
            if self.is_non_favorite_name(each_column.name.lower()):
                id_column_names.add(each_column.name)
                continue  # ids are boring - do at end
            column_count += 1
            if column_count > a_max_columns:
                break
            if column_count > 1:
                result += ", "
            result += '"' + each_column.name + '"'
        for each_id_column_name in id_column_names:
            column_count += 1
            if column_count > a_max_id_columns:
                break
            if column_count > 1:
                result += ", "
            result += '"' + each_id_column_name + '"'
        result += "]\n"
        return result

    def predictive_join_columns(self, a_table_def: MetaDataTable) -> set:
        """
        Generates set of predictive join column name:

            (Parent1.FavoriteColumn, Parent2.FavoriteColumn, ...)

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                set of col names (such Product.ProductName for OrderDetail)
        """
        result = set()
        foreign_keys = a_table_def.foreign_keys
        if a_table_def.name == "orderdetails":  # for debug
            log.debug("predictive_joins for: " + a_table_def.name)
        for each_foreign_key in foreign_keys:
            each_parent_name = each_foreign_key.target_fullname
            loc_dot = each_parent_name.index(".")
            each_parent_name = each_parent_name[0:loc_dot]
            parent_getter = each_parent_name
            if parent_getter[-1] == "s":  # plural parent table names have singular lower case accessors
                class_name = self.get_class_for_table(each_parent_name)  # eg, Product
                parent_getter = class_name[0].lower() + class_name[1:]
            each_parent = a_table_def.metadata.tables[each_parent_name]
            favorite_column_name = self.favorite_column_name(each_parent)
            result.add(parent_getter + "." + favorite_column_name)
        return result

    def is_non_favorite_name(self, a_name: str) -> bool:
        """
        Whether a_name is non-favorite (==> display at end, e.g., 'Id')

            Parameters
                argument1 a_name - str  (lower case expected)

            Returns
                bool
        """
        for each_non_favorite_name in self._non_favorite_names_list:
            if each_non_favorite_name in a_name:
                return True
        return False

    def find_child_list(self, a_table_def: MetaDataTable) -> list:
        """
            Returns list of models w/ fKey to a_table_def

            Not super efficient
                pass entire table list for each table
                ok until very large schemas

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                list of models w/ fKey to each_table
        """
        child_list = []
        all_tables = a_table_def.metadata.tables
        for each_possible_child_tuple in all_tables.items():
            each_possible_child = each_possible_child_tuple[1]
            parents = each_possible_child.foreign_keys
            if (a_table_def.name == "Customer" and
                    each_possible_child.name == "Order"):
                log.debug(a_table_def)
            for each_parent in parents:
                each_parent_name = each_parent.target_fullname
                loc_dot = each_parent_name.index(".")
                each_parent_name = each_parent_name[0:loc_dot]
                if each_parent_name == a_table_def.name:
                    child_list.append(each_possible_child)
        return child_list

    def model_name(self, a_class_name: str):  # override as req'd
        """
            returns "ModelView"

            default suffix for view corresponding to model

            intended for subclass override, for custom views

            Parameters
                argument1 a_table_name - str

            Returns
                view model_name for a_table_name, defaulted to "ModelView"
        """
        return "ModelView"

    def favorite_column_name(self, a_table_def: MetaDataTable) -> str:
        """
            returns string of first column that is...
                named <favorite_name> (default to "name"), else
                containing <favorite_name>, else
                (or first column)

            Parameters
                argument1 a_table_name - str

            Returns
                string of column name that is favorite (e.g., first in list)
        """
        favorite_names = self._favorite_names_list
        for each_favorite_name in favorite_names:
            columns = a_table_def.columns
            for each_column in columns:
                col_name = each_column.name.lower()
                if col_name == each_favorite_name:
                    return each_column.name
            for each_column in columns:
                col_name = each_column.name.lower()
                if each_favorite_name in col_name:
                    return each_column.name
        for each_column in columns:  # no favorites, just return 1st
            return each_column.name