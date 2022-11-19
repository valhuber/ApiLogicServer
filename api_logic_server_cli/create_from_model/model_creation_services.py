import ast
import io
import logging
import shutil
import traceback
from os.path import abspath
import importlib.util
import sys
import os
from typing import NewType, Type
import sqlalchemy
import sqlalchemy.ext
from sqlalchemy import MetaData
import inspect
import importlib
from flask import Flask
from typing import List, Dict
from pathlib import Path
from shutil import copyfile
from sqlalchemy.orm.interfaces import ONETOMANY, MANYTOONE, MANYTOMANY
from api_logic_server_cli.sqlacodegen_wrapper import sqlacodegen_wrapper

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(name)s: %(message)s')     # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = True

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


class ResourceAttribute():
    def __init__(self, each_attribute: object, resource: Type['Resource']):
        self.name = str(each_attribute.name)
        if self.name == "Ready":
            debug_str = "Nice breakpoint"
        # self.nullable = each_attribute.nullable
        type = str(each_attribute.type)
        self.type = None  # none means not interesting, default display to simple text
        if type == "DECIMAL":
            self.type = "DECIMAL"
        elif type == "DATE":
            self.type = "DATE"
#        elif type == "DATETIME":  safrs-admin date-picker fails with bad datetime format
#            self.type = "DATE"
        elif type == "IMAGE":
            self.type = "IMAGE"
        elif type.startswith("NTEXT") == "NTEXT":
            self.type = "NTEXT"
        self.non_favorite = False
        self.is_required = not each_attribute.nullable
        if self.is_required and each_attribute.primary_key:
            if type in ["Integer", "INTEGER", "MEDIUMINT", "SMALLINT", "TINYINT"]:
                self.is_required = False  # this is autonum... so not required (affects admin.yaml - required)
            else:
                debug_str = "Alpha Pkey"  # nothing to do, this for debug verification
        lower_name = self.name.lower()
        non_favs = resource.create_from_model._non_favorite_names_list
        for each_non_fav in non_favs:
            if lower_name.endswith(each_non_fav):
                self.non_favorite = True
                break
        resource.attributes.append(self)

    def __str__(self):
        result = self.name
        if self.type is not None:
            result += " - " + self.type
        return result


class ResourceRelationship():
    def __init__(self, parent_role_name: str, child_role_name: str):
        self.parent_role_name = parent_role_name
        self.child_role_name = child_role_name
        self.parent_resource = None
        self.child_resource = None
        self.parent_child_key_pairs = list()

    def __str__(self):
        return f'ResourceRelationship: ' \
               f'parent_role_name: {self.parent_role_name} | ' \
               f'child_role_name: {self.child_role_name} | ' \
               f'parent: {self.parent_resource} | ' \
               f'child: {self.child_resource} | '


class Resource():
    def __init__(self, name: str, create_from_model):
        self.name = name        # class name (which != safrs resource name)
        self.table_name = name  # safrs resource name; this is just default, overridden in create_model
        self.type = name        # just default, overridden in create_model
        self.children: List[ResourceRelationship] = list()
        self.parents: List[ResourceRelationship] = list()
        self.attributes: List[ResourceAttribute] = list()
        self.create_from_model = create_from_model  # to find favorite names etc.

    def __str__(self):
        return f'Resource: {self.name}, table_name: {self.table_name}, type: {self.type}'

    def get_favorite_attribute(self) -> ResourceAttribute:
        """
             returns ResourceAttribute of first attribute that is...
                 named <favorite_name> (default to "name"), else
                 containing <favorite_name>, else
                 (or first column)

             Parameters
                 argument1 a_table_name - str

             Returns
                 string of column name that is favorite (e.g., first in list)
         """
        favorite_names = self.create_from_model._favorite_names_list
        for each_favorite_name in favorite_names:
            for each_attribute in self.attributes:
                attribute_name = each_attribute.name.lower()
                if attribute_name == each_favorite_name:
                    return each_attribute
            for each_attribute in self.attributes:
                attribute_name = each_attribute.name.lower()
                if each_favorite_name in attribute_name:
                    return each_attribute
        for each_attribute in self.attributes:  # no favorites, just return 1st
            return each_attribute


class ModelCreationServices(object):
    """
    Model creation and shared services (favorite attributes, etc)

    Create models/expose_api_models.py, services for ui/basic_web_app/views.py and api/expose_api_models.py

    Key logic is initiated when a (single) object is created.  The `__init__` calls `create_models`.
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
                 project_directory: str = "~/Desktop/my_project",
                 api_name: str = "api",
                 copy_to_project_directory: str = "",
                 api_logic_server_dir: str = "",
                 os_cwd: str = "",
                 abs_db_url: str = "sqlite:///nw.sqlite",
                 db_url: str = "sqlite:///nw.sqlite",
                 nw_db_status: str = "",
                 my_children_list: dict = None,
                 my_parents_list: dict = None,
                 host: str = "localhost",
                 port: str = "5656",
                 use_model: str = "",
                 admin_app: bool = True,
                 flask_appbuilder: bool = True,
                 react_admin: bool = True,
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id",
                 command: str = "",
                 version: str = "0.0.0",
                 multi_api: bool = False,
                 infer_primary_key: bool = False):
        self.project_directory = None
        self.api_name = api_name
        if project_directory:
            self.project_directory = self.get_windows_path_with_slashes(project_directory)
        self.copy_to_project_directory = ""
        if copy_to_project_directory != "":
            self.copy_to_project_directory = self.get_windows_path_with_slashes(copy_to_project_directory)
        self.api_logic_server_dir = api_logic_server_dir
        self.abs_db_url = abs_db_url  # actual (not relative, reflects nw copy, etc)
        self.os_cwd = os_cwd
        self.db_url = db_url  # the original cli parameter
        self.nw_db_status = nw_db_status
        self.host = host
        self.port = port
        self.use_model = use_model
        self.command = command
        self.resource_list : Dict[str, Resource] = dict()
        self.resource_list_complete = False
        self.my_children_list = my_children_list
        """ key is table name, value is list of (parent-role-name, child-role-name, relationship) ApiLogicServer """
        self.my_parents_list = my_parents_list
        """ key is table name, value is list of (parent-role-name, child-role-name, relationship) ApiLogicServer """
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_names = non_favorite_names
        self.admin_app = admin_app
        self.flask_appbuilder = flask_appbuilder
        self.react_admin = react_admin
        self.version = version
        self.multi_api = multi_api
        self.infer_primary_key = infer_primary_key

        self.table_to_class_map = {}
        """ keys are table[.column], values are class / attribute """
        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()
        model_file_name, msg = sqlacodegen_wrapper.create_models_py(
            model_creation_services = self,
            abs_db_url= abs_db_url,
            project_directory = project_directory)
        self.create_resource_list(model_file_name, msg)  # whether created or used, build resource_list


    @staticmethod
    def get_windows_path_with_slashes(url: str) -> str:
        """ idiotic fix for windows (\ --> \\\\)
        https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file"""
        """ old code
        full_path = os.path.abspath(url)
        result = full_path.replace('\\', '\\\\')
        if os.name == "nt":  # windows
            result = full_path.replace('/', '\\')
        print(f'*** DEBUG - how about url_path={url_path}')
        """
        url_path = Path(url)
        result = str(url_path)
        return result

    def recursive_overwrite(self, src, dest, ignore=None):
        """ copyTree, with overwrite
        """
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    self.recursive_overwrite(os.path.join(src, f),
                                        os.path.join(dest, f),
                                        ignore)
        else:
            shutil.copyfile(src, dest)

    @staticmethod
    def fix_win_path(path: str) -> str:
        result = path
        if os.name == "nt":
            result = path.replace('/', '\\')
        return result

    @staticmethod
    def create_app_zzz(config_filename=None, host="localhost"):
        import safrs

        app = Flask("API Logic Server")
        import api_logic_server_cli.config as app_logic_server_config
        app.config.from_object(app_logic_server_config.Config)
        db = safrs.DB
        db.init_app(app)
        return app

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

    def show_attributes(self, resource: Resource):
        return self.gen_attributes(resource, "show_columns = [", 99, 999, 999)

    def get_show_columns(self, a_table_def: MetaDataTable) -> set:
        gen_string = self.show_columns(a_table_def)
        gen_string = gen_string[2 + gen_string.find("="):]
        columns = ast.literal_eval(gen_string)
        return columns

    def get_show_attributes(self, resource: Resource) -> set:
        gen_string = self.show_attributes(resource)
        gen_string = gen_string[2 + gen_string.find("="):]
        attributes = ast.literal_eval(gen_string)
        return attributes

    def get_attributes(self, resource: Resource) -> list:
        """ bypass all joins, ids at end - just the raw attributes """
        result_set = list()
        for each_attribute in resource.attributes:
            result_set.append(each_attribute.name)
        return result_set

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

    def gen_attributes(self,
                       a_resource: Resource,
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
        attributes = a_resource.attributes
        id_attribute_names = set()
        processed_attribute_names = set()
        result += ""
        if a_resource.name == "OrderDetail":
            result += "\n"  # just for debug stop

        favorite_attribute_name = self.favorite_attribute_name(a_resource)
        column_count = 1
        result += '"' + favorite_attribute_name + '"'  # todo hmm: emp territory
        processed_attribute_names.add(favorite_attribute_name)

        predictive_joins = self.predictive_join_attributes(a_resource)
        if "list" in a_view_type or "show" in a_view_type:
            # alert - prevent fab key errors!
            for each_parent_attribute in predictive_joins:
                column_count += 1
                if column_count > 1:
                    result += ", "
                result += '"' + each_parent_attribute + '"'
                if column_count > a_max_joins:
                    break
        for each_column in attributes:
            if each_column.name in processed_attribute_names:
                continue
            if self.is_non_favorite_name(each_column.name.lower()):
                id_attribute_names.add(each_column.name)
                continue  # ids are boring - do at end
            column_count += 1
            if column_count > a_max_columns:
                break
            if column_count > 1:
                result += ", "
            result += '"' + each_column.name + '"'
        for each_id_column_name in id_attribute_names:
            column_count += 1
            if column_count > a_max_id_columns:
                break
            if column_count > 1:
                result += ", "
            result += '"' + each_id_column_name + '"'
        result += "]\n"
        return result

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

    def predictive_join_attributes(self, a_resource: Resource) -> list:
        """
        Generates set of predictive join column name:

            (Parent1.FavoriteColumn, Parent2.FavoriteColumn, ...)

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                set of col names (such Product.ProductName for OrderDetail)
        """
        result = list()
        if a_resource.name == "Order":  # for debug
            debug_str = "predictive_joins for: " + a_resource.name
        for each_parent in a_resource.parents:
            each_parent_resource = self.resource_list[each_parent.parent_resource]
            favorite_attribute_name = self.favorite_attribute_name(each_parent_resource)
            parent_ref_attr_name = each_parent.parent_role_name + "." + favorite_attribute_name
            result.append(parent_ref_attr_name)
        return result

    def predictive_join_columns(self, a_table_def: MetaDataTable) -> list:
        """
        Generates set of predictive join column name:

            (Parent1.FavoriteColumn, Parent2.FavoriteColumn, ...)

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                set of col names (such Product.ProductName for OrderDetail)
        """
        result = list()
        foreign_keys = a_table_def.foreign_key_constraints
        if a_table_def.name == "Order":  # for debug
            debug_str = "predictive_joins for: " + a_table_def.name
        for each_foreign_key in foreign_keys:
            """ remove old code
            each_parent_name = each_foreign_key.referred_table.name + "." + each_foreign_key.column_keys[0]
            loc_dot = each_parent_name.index(".")
            each_parent_name = each_parent_name[0:loc_dot]
            """
            each_parent_name = each_foreign_key.referred_table.name  # todo: improve multi-field key support
            parent_getter = each_parent_name
            if parent_getter[-1] == "s":  # plural parent table names have singular lower case accessors
                class_name = self.get_class_for_table(each_parent_name)  # eg, Product
                parent_getter = class_name[0].lower() + class_name[1:]
            each_parent = a_table_def.metadata.tables[each_parent_name]
            favorite_column_name = self.favorite_column_name(each_parent)
            parent_ref_attr_name = parent_getter + "." + favorite_column_name
            if parent_ref_attr_name in result:
                parent_ref_attr_name = parent_getter + "1." + favorite_column_name
            result.append(parent_ref_attr_name)
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
                debug_str = a_table_def
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


    def favorite_attribute_name(self, resource: Resource) -> str:
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
            attributes = resource.attributes
            for each_attribute in attributes:
                attribute_name = each_attribute.name.lower()
                if attribute_name == each_favorite_name:
                    return each_attribute.name
            for each_attribute in attributes:
                attribute_name = each_attribute.name.lower()
                if each_favorite_name in attribute_name:
                    return each_attribute.name
        for each_attribute in resource.attributes:  # no favorites, just return 1st
            return each_attribute.name

    def add_table_to_class_map(self, orm_class) -> str:
        """ given class, find table (hide your eyes), add table/class to table_to_class_map """
        orm_class_info = orm_class[1]
        query = str(orm_class_info.query)[7:]
        table_name = query.split('.')[0]
        table_name = table_name.strip('\"')
        self.table_to_class_map_update(table_name=table_name, class_name=orm_class[0])
        return table_name

    def table_to_class_map_update(self, table_name: str, class_name: str):
        self.table_to_class_map.update({table_name: class_name})

    def get_class_for_table(self, table_name) -> str:
        """ given table_name, return its class_name from table_to_class_map """
        if table_name in self.table_to_class_map:
            return self.table_to_class_map[table_name]
        else:
            debug_str = "skipping view: " + table_name
            return None

    def find_meta_data(self, cwd: str, log_info: bool=False) -> MetaData:
        return self.metadata

    def resolve_home(self, name: str) -> str:
        """
        :param name: a file name, eg, ~/Desktop/a.b
        :return: /users/you/Desktop/a.b

        This just removes the ~, the path may still be relative to run location
        """
        result = name
        if result.startswith("~"):
            result = str(Path.home()) + result[1:]
        return result

    def close_app(self):
        """ may not be necessary - once had to open app to load class
        """
        if self.app:
            self.app.teardown_appcontext(None)
        if self.engine:
            self.engine.dispose()

    def create_resource_list(self, models_file, msg):
        """
        creates self.resource_list via dynamic import of models.py  (drives create_from_model modules)
        
        :param models_file name of file for output
        :param msg e.g. .. .. ..Create resource_list - dynamic import database/models.py, inspect
        """
        """ old code
        # project_abs_path = abspath(self.project_directory)
        # project_abs_path = str(Path(self.project_directory).absolute())
        """
        project_path = self.project_directory
        debug_dynamic_loader = False
        if debug_dynamic_loader:
            print(f'\n\n ### INSTALL cwd = {os.getcwd()}')
            print(f'\n*** DEBUG/import - self.project_directory={self.project_directory}')
            print(f'*** DEBUG/import - project_abs_path={project_path}')
        model_imported = False
        path_to_add = project_path if self.command == "create-ui" else \
            project_path + "/database"  # for Api Logic Server projects
        sys.path.insert(0, self.project_directory)    # e.g., /Users/val/dev/servers/install/ApiLogicServer
        sys.path.insert(0, path_to_add)    # e.g., /Users/val/dev/servers/install/ApiLogicServer/database
        print(msg + " in <project>/database")  #  + path_to_add)
        # sys.path.insert( 0, '/Users/val/dev/servers/install/ApiLogicServer/ApiLogicProject/database')
        # sys.path.insert( 0, '/Users/val/dev/servers/install/ApiLogicServer/ApiLogicProject')  # AH HA!!
        # sys.path.insert( 0, 'ApiLogicProject')  # or, AH HA!!
        # print(f'*** DEBUG - sys.path={sys.path}')
        try:
            # credit: https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
            importlib.import_module('models')
            model_imported = True
        except:
            print(f'\n===> ERROR - Dynamic model import failed in {path_to_add} - project run will fail')
            traceback.print_exc()
            pass  # try to continue to enable manual fixup

        orm_class = None
        if not model_imported:
            print('.. .. ..Creation proceeding to enable manual database/models.py fixup')
            print('.. .. .. See https://valhuber.github.io/ApiLogicServer/Troubleshooting/')
        else:
            try:
                resource_list: Dict[str, Resource] = dict()
                cls_members = inspect.getmembers(sys.modules["models"], inspect.isclass)
                for each_cls_member in cls_members:
                    each_class_def_str = str(each_cls_member)
                    #  such as ('Category', <class 'models.Category'>)
                    if ("'models." in str(each_class_def_str) and
                            "Ab" not in str(each_class_def_str)):
                        resource_name = each_cls_member[0]
                        resource_class = each_cls_member[1]
                        table_name = resource_class._s_collection_name
                        if table_name == "Department":
                            debug_str = "Excellent breakpoint"
                        resource = Resource(name=resource_name, create_from_model=self)
                        self.metadata = resource_class.metadata
                        self.table_to_class_map.update({table_name: resource_name})   # required for ui_basic_web_app
                        if resource_name not in resource_list:
                            resource_list[resource_name] = resource
                        resource = resource_list[resource_name]
                        resource.table_name = table_name
                        resource_data = {"type": resource_class._s_type}  # todo what's this?
                        resource_data = {"type": resource_name}
                        for each_attribute in resource_class._s_columns:
                            attr_type = str(each_attribute.type)
                            resource_attribute = ResourceAttribute(each_attribute=each_attribute,
                                                                   resource=resource)
                        for rel_name, rel in resource_class._s_relationships.items():
                            # relation = {}
                            # relation["direction"] = "toone" if rel.direction == MANYTOONE else "tomany"
                            if rel.direction == ONETOMANY:  # process only parents of this child
                                debug_str = "onetomany"
                            else:  # many to one (parent for this child) - version <= 3.50.43
                                debug_rel = False
                                if debug_rel:
                                    debug_rel_str = f'Debug resource_class._s_relationships {resource_name}: ' \
                                                    f'parent_role_name (aka rel_name): {rel_name},    ' \
                                                    f'child_role_name (aka rel.back_populates): {rel.back_populates}'
                                    print(debug_rel_str)

                                parent_role_name = rel_name
                                child_role_name = rel.back_populates
                                do_patch_self_reln = False  # roles backward for self-relns, but addressed in codegen
                                if do_patch_self_reln and resource_name == rel.mapper.class_._s_class_name:
                                    parent_role_name = rel.back_populates
                                    child_role_name = rel_name
                                relationship = ResourceRelationship(parent_role_name=parent_role_name,
                                                                    child_role_name=child_role_name)
                                for each_fkey in rel._calculated_foreign_keys:
                                    pair = ("?", each_fkey.description)
                                    relationship.parent_child_key_pairs.append(pair)
                                resource.parents.append(relationship)
                                relationship.child_resource = resource_name
                                parent_resource_name = str(rel.target.name)
                                parent_resource_name = rel.mapper.class_._s_class_name
                                relationship.parent_resource = parent_resource_name
                                if parent_resource_name not in resource_list:
                                    parent_resource = Resource(name=parent_resource_name, create_from_model=self)
                                    resource_list[parent_resource_name] = parent_resource
                                parent_resource = resource_list[parent_resource_name]
                                parent_resource.children.append(relationship)
                    pass
                pass
                debug_str = f'setting resource_list: {str(resource_list)}'
                self.resource_list = resource_list  # model loaded - excellent breakpoint location

                if orm_class is not None:
                    log.debug(f'.. .. ..Dynamic model import successful '
                             f'({len(self.table_to_class_map)} classes'
                             f') -'
                             f' getting metadata from {str(orm_class)}')
            except:
                print("\n===> ERROR - Unable to introspect model classes")
                traceback.print_exc()
                pass
    
