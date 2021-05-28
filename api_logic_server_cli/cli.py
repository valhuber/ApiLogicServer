# -*- coding: utf-8 -*-
"""
Given a database url,
create ApiLogicServer project by cloning prototype,
in particular create the ui/basic_web_app/app/views.py
and api/expose_api_models.

See: main driver

"""

import pathlib
import subprocess
import traceback
from os.path import abspath
from os.path import realpath
from pathlib import Path
from shutil import copyfile
import shutil
import importlib.util

import logic_bank_utils.util as logic_bank_utils
from flask import Flask

import logging
import datetime
from typing import NewType
import sys
import os
import sqlalchemy
import sqlalchemy.ext
from sqlalchemy import MetaData
import inspect
import importlib
import click

__version__ = "02.02.28"
default_db = "<default -- nw.sqlite>"

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


def create_app(config_filename=None, host="localhost"):
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base
    import safrs

    app = Flask("API Logic Server")
    import api_logic_server_cli.config as app_logic_server_config
    app.config.from_object(app_logic_server_config.Config)
    db = safrs.DB
    db.init_app(app)
    return app


class GenerateFromModel(object):
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
    tables_visited = set()  # to address "generate children first"
    """ table names of all visited views """
    tables_generated = set()  # to address "generate children first"
    """ table names of all fully generated views """

    num_pages_generated = 0
    num_related = 0

    def __init__(self,
                 project_name: str ="~/Desktop/my_project",
                 db_url: str = "sqlite:///nw.sqlite",
                 host: str = "localhost",
                 port: str = "5000",
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id"):
        self.project_name = project_name
        self.db_url = db_url
        self.host = host
        self.port = port
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_name = non_favorite_names

        self.table_to_class_map = {}
        """ keys are table[.column], values are class / attribute """
        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None

    def generate_api_expose_and_ui_views(self):
        """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

        cwd = os.getcwd()
        self.result_views += '"""'
        self.result_apis += '"""'
        self.result_views += ("\nApiLogicServer Generate From Model " + __version__ + "\n\n"
                              # + "From: " + sys.argv[0] + "\n\n"
                              + "Using Python: " + sys.version + "\n\n"
                              + "Favorites: "
                              + str(self._favorite_names_list) + "\n\n"
                              + "Non Favorites: "
                              + str(self._non_favorite_names_list) + "\n\n"
                              + "At: " + str(datetime.datetime.now()) + "\n\n")
        self.result_apis += ("\nApiLogicServer Generate From Model " + __version__ + "\n\n"
                             # + "From: " + sys.argv[0] + "\n\n"
                             + "Using Python: " + sys.version + "\n\n"
                             + "At: " + str(datetime.datetime.now()) + "\n\n"
                             + '"""\n\n')
        port_replace = self.port if self.port else "None"
        self.result_apis += \
            f'def expose_models(app, HOST="{self.host}", PORT={port_replace}, API_PREFIX="/api"):\n'
        self.result_apis += '    """ called by api_logic_server_run.py """\n\n'
        self.result_apis += \
            '    api = SAFRSAPI(app, host=HOST, port=PORT)\n'

        sys.path.append(cwd)  # for banking Command Line test

        self.result_views += '"""\n\n'
        self.find_meta_data(cwd, self.project_name, self.db_url)  # sets self.metadata
        meta_tables = self.metadata.tables
        self.result_views += self.generate_module_imports()
        for each_table in meta_tables.items():
            each_result = self.process_each_table(each_table[1])
            self.result_views += each_result
        self.result_views += self.process_module_end(meta_tables)
        self.result_apis += f'    return api\n'
        # self.session.close()
        self.app.teardown_appcontext(None)
        if self.engine:
            self.engine.dispose()
        return

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

    def find_meta_data(self, a_cwd: str, a_project_name: str, a_db_url) -> MetaData:
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
        project_abs_path = abspath(a_project_name)

        if do_dynamic_load:
            """
                a_cwd -- see ApiLogicServer/prototype for structure

                credit: https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
            """
            sys_path = str(sys.path)

            self.app = create_app(host=self.host)
            self.app.config.SQLALCHEMY_DATABASE_URI = a_db_url
            self.app.app_context().push()  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

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

    def generate_module_imports(self) -> str:
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

    def process_each_table(self, a_table_def: MetaDataTable) -> str:
        """
            Generate class and add_view for given table.

            These must be ordered children first,
            so view.py compiles properly
            ("related_views" would otherwise fail to compile).

            We therefore recurse for children first.

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                string class and add_view for given table.
        """
        result = ""
        table_name = a_table_def.name
        log.debug("process_each_table: " + table_name)
        if "TRANSFERFUNDx" in table_name:
            log.debug("special table")  # debug stop here
        if table_name + " " in self.not_exposed:
            return "# not_exposed: api.expose_object(models.{table_name})"
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            return "# skip admin table: " + table_name + "\n"
        elif table_name in self.tables_visited:
            log.debug("table already generated per recursion: " + table_name)
            return "# table already generated per recursion: " + table_name + "\n"
        elif 'sqlite_sequence' in table_name:
            return "# skip sqlite_sequence table: " + table_name + "\n"
        else:
            class_name = self.get_class_for_table(table_name)
            if class_name is None:
                return "# skip view: " + table_name
            self.tables_visited.add(table_name)
            child_list = self.find_child_list(a_table_def)
            for each_child in child_list:  # recurse to ensure children first
                log.debug(".. but children first: " + each_child.name)
                result += self.process_each_table(each_child)
                self.tables_visited.add(each_child.name)

            self.tables_generated.add(a_table_def.fullname)
            self.result_apis += f'    api.expose_object(models.{class_name})\n'

            self.num_pages_generated += 1

            model_name = self.model_name(class_name)
            view_class_name = class_name + model_name
            result += "\n\n\nclass " + view_class_name + "(" + model_name + "):\n"
            result += (
                self._indent + "datamodel = SQLAInterface(" +
                class_name + ")\n"
            )
            result += self._indent + self.list_columns(a_table_def)
            result += self._indent + self.show_columns(a_table_def)
            result += self._indent + self.edit_columns(a_table_def)
            result += self._indent + self.add_columns(a_table_def)
            result += self._indent + self.related_views(a_table_def)
            result += (
                "\nappbuilder.add_view(\n"
                + self._indent
                + self._indent
                + view_class_name
                + ", "
                + '"'
                + class_name
                + ' List", '
                + 'icon="fa-folder-open-o", category="Menu")\n'
            )
            return result + "\n\n"

    def list_columns(self, a_table_def: MetaDataTable) -> str:
        """
            Generate list_columns = [...]

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                list_columns = [...] - favorites / joins first, not too many
        """
        return self.gen_columns(a_table_def, "list_columns = [", 2, 5, 0)

    def show_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "show_columns = [", 99, 999, 999)

    def edit_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "edit_columns = [", 99, 999, 999)

    def add_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "add_columns = [", 99, 999, 999)

    def query_columns(self, a_table_def: MetaDataTable):
        return self.gen_columns(a_table_def, "query_columns = [", 99, 999, 999)

    def gen_columns(self,
                    a_table_def: MetaDataTable,
                    a_view_type: int,
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

    def related_views(self, a_table_def: MetaDataTable) -> str:
        """
            Generates statments like
                related_views = ["Child1", "Child2"]

            Todo
                * are child roles required?
                    ** e.g., children = relationship("Child"
                * are multiple relationsips supported?
                    ** e.g., dept has worksFor / OnLoan Emps
                * are circular relationships supported?
                    ** e.g., dept has emps, emp has mgr

            Parameters
                argument1 a_table_def - TableModelInstance

            Returns
                str like related_views = ["Child1", "Child2"]
        """
        result = "related_views = ["
        related_count = 0
        child_list = self.find_child_list(a_table_def)
        self_relns = ""
        if a_table_def.fullname == "store":
            log.debug(f'related_views for {a_table_def.fullname}')
        for each_child in child_list:
            if a_table_def.fullname not in self.tables_generated:
                log.debug(f'must omit: {a_table_def.fullname}')
            if a_table_def.fullname == each_child.fullname or \
                    each_child.fullname not in self.tables_generated:
                self_relns += a_table_def.fullname + " "
            else:
                related_count += 1
                if related_count > 1:
                    result += ", "
                else:
                    self.num_related += 1
                class_name = self.get_class_for_table(each_child.fullname)
                if class_name is None:
                    print(f'.. .. .. Warning - Skipping {self.model_name(each_child)}->'
                          f'{each_child.fullname} - no database/models.py class')
                    related_count -= 1
                else:
                    each_entry = class_name + self.model_name(each_child)
                    result += each_entry
        omitted = "  # omitted mutually referring relationships: " + self_relns if self_relns != "" else ""
        result += "]" + omitted + "\n"
        return result

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

    def process_module_end(self, a_metadata_tables: MetaData) -> str:
        """
            returns the last few lines

            comments - # tables etc
        """
        result = (
            "#  "
            + str(len(a_metadata_tables))
            + " table(s) in model; generated "
            + str(self.num_pages_generated)
            + " page(s), including "
            + str(self.num_related)
            + " related_view(s).\n\n"
        )
        if self.num_related == 0:
            result += "#  Warning - no related_views,"
            result += " since foreign keys missing\n"
            result += "#  .. add them to your models.py (see nw example)\n"
            result += "#  .. or better, add them to your database"
            print(".. ..WARNING - no relationships detected - add them to your database or model")
            print(".. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design")
        return result


def delete_dir(dir_path, msg):
    """
    :param dir_path: delete this folder
    :return:
    """
    use_shutil_debug = True
    if use_shutil_debug:
        # credit: https://linuxize.com/post/python-delete-files-and-directories/
        # and https://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
        import errno, os, stat, shutil

        def handleRemoveReadonly(func, path, exc):
            excvalue = exc[1]
            if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
                os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                func(path)
            else:
                raise
        print(f'{msg} Delete dir: {dir_path}')
        use_callback = False
        if use_callback:
            shutil.rmtree(dir_path, ignore_errors=False, onerror=handleRemoveReadonly)
        else:
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                if "No such file" in e.strerror:
                    pass
                else:
                    print("Error: %s : %s" % (dir_path, e.strerror))
    else:
        # https://stackoverflow.com/questions/22948189/how-to-solve-the-directory-is-not-empty-error-when-running-rmdir-command-in-a
        try:
            remove_project = run_command(f'del /f /s /q {dir_path} 1>nul')
        except:
            pass
        try:
            remove_project = run_command(f'rmdir /s /q {dir_path}')  # no prompt, no complaints if non-exists
        except:
            pass


def run_command(cmd: str, env=None, msg: str = "") -> str:
    """ run shell command

    :param cmd: string of command to execute
    :param env:
    :param msg: optional message (no-msg to suppress)
    :return:
    """
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    if msg != "no-msg":
        print(f'{log_msg} {cmd}')

    use_env = env
    if env is None:
        project_dir = get_api_logic_server_dir()
        python_path = str(project_dir) + "/venv/lib/python3.9/site_packages"
        use_env = os.environ.copy()
        # print("\n\nFixing env for cmd: " + cmd)
        if hasattr(use_env, "PYTHONPATH"):
            use_env["PYTHONPATH"] = python_path + ":" + use_env["PYTHONPATH"]  # eg, /Users/val/dev/ApiLogicServer/venv/lib/python3.9
            # print("added PYTHONPATH: " + str(use_env["PYTHONPATH"]))
        else:
            use_env["PYTHONPATH"] = python_path
            # print("created PYTHONPATH: " + str(use_env["PYTHONPATH"]))
    use_env_debug = False  # not able to get this working
    if use_env_debug:
        result_b = subprocess.check_output(cmd, shell=True, env=use_env)
    else:
        result_b = subprocess.check_output(cmd, shell=True)  # , stderr=subprocess.STDOUT)  loses all logging
    result = str(result_b)  # b'pyenv 1.2.21\n'
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    if result != "" and result != "Downloaded the skeleton app, good coding!":
        print(f'{log_msg} {cmd} result: {spaces}{result}')


def run_command_nowait(cmd: str, env=None, msg: str = "") -> str:
    """ run shell command

    :param cmd: string of command to execute
    :param env:
    :param msg: optional message (no-msg to suppress)
    :return:
    """
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    if msg != "no-msg":
        print(f'{log_msg} {cmd}')

    use_env = env
    if env is None:
        project_dir = get_api_logic_server_dir()
        python_path = str(project_dir) + "/venv/lib/python3.9/site_packages"
        use_env = os.environ.copy()
        # print("\n\nFixing env for cmd: " + cmd)
        if hasattr(use_env, "PYTHONPATH"):
            use_env["PYTHONPATH"] = python_path + ":" + use_env["PYTHONPATH"]  # eg, /Users/val/dev/ApiLogicServer/venv/lib/python3.9
            # print("added PYTHONPATH: " + str(use_env["PYTHONPATH"]))
        else:
            use_env["PYTHONPATH"] = python_path
            # print("created PYTHONPATH: " + str(use_env["PYTHONPATH"]))
    use_env_debug = False  # not able to get this working
    if use_env_debug:
        result_b = subprocess.check_output(cmd, shell=True, env=use_env)
    else:
        result_b = subprocess.Popen(cmd, shell=True)
    result = str(result_b)  # b'pyenv 1.2.21\n'
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    if result != "" and result != "Downloaded the skeleton app, good coding!":
        print(f'{log_msg} {cmd} result: {spaces}{result}')


def clone_prototype_project_with_nw_samples(project_directory: str, from_git: str, msg: str, db_url: str):
    """
    clone prototype to create and remove git folder

    if nw, Append logic/logic_bank.py with pre-defined...

    :param project_directory: name of project created
    :param from_git: name of git project to clone (blank for default)
    :return: result of cmd
    """
    cloned_from = from_git
    remove_project_debug = True
    if remove_project_debug:
        delete_dir(realpath(project_directory), "1.")

    if from_git.startswith("https://"):
        cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project_directory
        cmd = f'git clone --quiet {from_git} {project_directory}'
        result = run_command(cmd, msg=msg)  # "2. Create Project")
        delete_dir(f'{project_directory}/.git', "3.")
    else:
        from_dir = from_git
        if from_dir == "":
            code_loc = str(get_api_logic_server_dir())
            if "\\" in code_loc:
                from_dir = code_loc + "\\prototype"
            else:
                from_dir = code_loc + "/prototype"
        print(f'{msg} copy {from_dir} -> {project_directory}')
        cloned_from = from_dir
        shutil.copytree(from_dir, project_directory)

    replace_string_in_file(search_for="creation-date",
                           replace_with=str(datetime.datetime.now()),
                           in_file=f'{project_directory}/readme.md')
    replace_string_in_file(search_for="cloned-from",
                           replace_with=cloned_from,
                           in_file=f'{project_directory}/readme.md')

    if db_url.endswith("nw.sqlite"):
        print(".. ..Append logic/logic_bank.py with pre-defined nw_logic, rpcs")
        replace_logic_with_nw_logic(project_directory)
        replace_models_ext_with_nw_models_ext(project_directory)
        replace_expose_rpcs_with_nw_expose_rpcs(project_directory)
        replace_server_startup_test_with_nw_server_startup_test(project_directory)


def create_basic_web_app(db_url, project_name, msg):
    project_abs_path = abspath(project_name)
    fab_project = project_abs_path + "/ui/basic_web_app"
    cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
    result = run_command(cmd, msg=msg)
    pass


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def create_models(db_url: str, project: str, use_model: str) -> str:
    """
    create model.py, normally via expose_existing.expose_existing_callable

    or, use_model -- then just copy
    """

    class DotDict(dict):
        """dot.notation access to dictionary attributes"""
        # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    def get_codegen_args():
        """ DotDict of url, outfile, version """
        codegen_args = DotDict({})
        codegen_args.url = db_url
        # codegen_args.outfile = models_file
        codegen_args.outfile = project + '/database/models.py'
        codegen_args.version = False
        return codegen_args

    if use_model != "":  # use this hand-edited model (e.g., added relns)
        model_file = resolve_home(use_model)
        print(f'.. ..Copy {model_file} to {project + "/database/models.py"}')
        copyfile(model_file, project + '/database/models.py')
    else:
        import expose_existing.expose_existing_callable as expose_existing_callable
        code_gen_args = get_codegen_args()
        expose_existing_callable.codegen(code_gen_args)
        pass


def write_expose_api_models(project_name, apis):
    text_file = open(project_name + '/api/expose_api_models.py', 'a')
    text_file.write(apis)
    text_file.close()


def update_api_logic_server_run__and__config(project_name, project_directory, abs_db_url, host, port) -> str:
    """
    Updates project_name, ApiLogicServer hello, project_dir in api_logic_server_run_py

    Note project_directory is from user, and may be relative (and same as project_name)
    """
    project_directory_actual = os.path.abspath(project_directory)  # make path absolute, not relative (no /../)
    api_logic_server_run_py = f'{project_directory}/api_logic_server_run.py'
    replace_string_in_file(search_for="\"api_logic_server_project_name\"",  # fix logic_bank_utils.add_python_path
                           replace_with='"' + os.path.basename(project_name) + '"',
                           in_file=api_logic_server_run_py)
    replace_string_in_file(search_for="ApiLogicServer hello",
                           replace_with="ApiLogicServer generated at:" + str(datetime.datetime.now()),
                           in_file=api_logic_server_run_py)
    project_directory_fix = project_directory_actual
    if os.name == "nt":  # windows
        project_directory_fix = get_windows_path_with_slashes(str(project_directory_actual))
    replace_string_in_file(search_for="\"api_logic_server_project_dir\"",  # for logging project location
                           replace_with='"' + project_directory_fix + '"',
                           in_file=api_logic_server_run_py)
    replace_string_in_file(search_for="api_logic_server_host",  # server host
                           replace_with=host,
                           in_file=api_logic_server_run_py)
    replace_port = f', port="{port}"' if port else ""  # TODO: consider reverse proxy

    replace_string_in_file(search_for="api_logic_server_version",
                           replace_with=__version__,
                           in_file=api_logic_server_run_py)

    replace_string_in_file(search_for="api_logic_server_port",   # server port
                           replace_with=port,
                           in_file=api_logic_server_run_py)
    copy_sqlite = True
    if copy_sqlite == False or "sqlite" not in abs_db_url:
        db_uri = get_windows_path_with_slashes(abs_db_url)
        replace_string_in_file(search_for="replace_db_url",
                               replace_with=db_uri,
                               in_file=f'{project_directory}/config.py')
    else:
        """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
        """
        # strip sqlite://// from sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/nw.sqlite
        db_loc = abs_db_url.replace("sqlite:///", "")
        target_db_loc_actual = project_directory_actual + '/database/db.sqlite'
        copyfile(db_loc, target_db_loc_actual)

        if os.name == "nt":  # windows
            # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
            target_db_loc_actual = get_windows_path_with_slashes(project_directory_actual + '\database\db.sqlite')
        db_uri = f'sqlite:///{target_db_loc_actual}'
        replace_string_in_file(search_for="replace_db_url",
                               replace_with=db_uri,
                               in_file=f'{project_directory}/config.py')
    return db_uri


def replace_logic_with_nw_logic(project_name):
    """ Replace logic/logic_bank.py with pre-defined nw_logic """
    logic_file = open(project_name + '/logic/logic_bank.py', 'w')
    nw_logic_file = open(os.path.dirname(os.path.realpath(__file__)) + "/nw_logic.py")
    nw_logic = nw_logic_file.read()
    logic_file.write(nw_logic)
    logic_file.close()


def replace_models_ext_with_nw_models_ext(project_name):
    """ Replace models/models_ext.py with pre-defined nw_models_ext """
    models_ext_file = open(project_name + '/database/models_ext.py', 'w')
    nw_models_ext_file = open(os.path.dirname(os.path.realpath(__file__)) + "/nw_models_ext.py")
    nw_models_ext = nw_models_ext_file.read()
    models_ext_file.write(nw_models_ext)
    models_ext_file.close()


def replace_expose_rpcs_with_nw_expose_rpcs(project_name):
    """ replace api/expose_rpcs with nw version """
    rpcs_file = open(project_name + '/api/expose_services.py', 'w')
    nw_expose_rpcs_file = open(os.path.dirname(os.path.realpath(__file__)) + "/nw_expose_services.py")
    nw_expose_rpcs = nw_expose_rpcs_file.read()
    rpcs_file.write(nw_expose_rpcs)
    rpcs_file.close()


def replace_server_startup_test_with_nw_server_startup_test(project_name):
    """ replace api/expose_rpcs with nw version """
    tests_file = open(project_name + '/test/server_startup_test.py', 'w')
    nw_tests_file = open(os.path.dirname(os.path.realpath(__file__)) + "/nw_server_startup_test.py")
    nw_tests_file_data = nw_tests_file.read()
    tests_file.write(nw_tests_file_data)
    tests_file.close()


def replace_string_in_file(search_for: str, replace_with: str, in_file: str):
    with open(in_file, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace(search_for, replace_with)
    with open(in_file, 'w') as file:
        file.write(file_data)


def get_windows_path_with_slashes(url: str) -> str:
    """ idiotic fix for windows (\ --> \\\\)

    https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file"""
    return url.replace('\\', '\\\\')


def resolve_home(name: str) -> str:
    """
    :param name: a file name, eg, ~/Desktop/a.b
    :return: /users/you/Desktop/a.b

    This just removes the ~, the path may still be relative to run location
    """
    result = name
    if result.startswith("~"):
        result = str(Path.home()) + result[1:]
    return result


def fix_basic_web_app_run__python_path(project_directory):
    """ prepend logic_bank_utils call to fixup python path in ui/basic_web_app/run.py (enables run.py) """
    old_way = False
    if old_way:
        file_name = f'{project_directory}/ui/basic_web_app/run.py'
        proj = os.path.basename(project_directory)
        insert_text = ("\n# ApiLogicServer - enable flask run\n"
                       "import logic_bank_utils.util as logic_bank_utils\n"
                       + f'logic_bank_utils.add_python_path(project_dir="{proj}", my_file=__file__)\n\n')
        with open(file_name, 'r+') as fp:
            lines = fp.readlines()  # lines is list of line, each element '...\n'
            lines.insert(0, insert_text)  # you can use any index if you know the line index
            fp.seek(0)  # file pointer locates at the beginning to write the whole file again
            fp.writelines(lines)  # write whole lists again to the same file
    else:
        models_ext_file = open(project_directory + '/ui/basic_web_app/run.py', 'w')
        nw_models_ext_file = open(os.path.dirname(os.path.realpath(__file__)) + "/ui_basic_web_app_run.py")
        nw_models_ext = nw_models_ext_file.read()
        models_ext_file.write(nw_models_ext)
        models_ext_file.close()

        proj = os.path.basename(project_directory)
        replace_string_in_file(search_for="api_logic_server_project_directory",
                               replace_with=proj,
                               in_file=f'{project_directory}/ui/basic_web_app/run.py')


def fix_basic_web_app_run__create_admin(project_directory):
    """ update create_admin.sh with project_directory """

    unix_project_name = project_directory.replace('\\', "/")
    target_create_admin_sh_file = open(f'{unix_project_name}/ui/basic_web_app/create_admin.sh', 'x')
    source_create_admin_sh_file = open(os.path.dirname(os.path.realpath(__file__)) + "/create_admin.sh")
    create_admin_commands = source_create_admin_sh_file.read()
    target_create_admin_sh_file.write(create_admin_commands)
    target_create_admin_sh_file.close()

    replace_string_in_file(search_for="/Users/val/dev/servers/classicmodels/",
                           replace_with=unix_project_name,
                           in_file=f'{unix_project_name}/ui/basic_web_app/create_admin.sh')


def insert_lines_at(lines: str, at: str, file_name: str):
    """ insert <lines> into file_name after line with <str> """
    with open(file_name, 'r+') as fp:
        file_lines = fp.readlines()  # lines is list of lines, each element '...\n'
        found = False
        insert_line = 0
        for each_line in file_lines:
            if at in each_line:
                found = True
                break
            insert_line += 1
        if not found:
            raise Exception(f'Internal error - unable to find insert: {at}')
        file_lines.insert(insert_line, lines)  # you can use any index if you know the line index
        fp.seek(0)  # file pointer locates at the beginning to write the whole file again
        fp.writelines(file_lines)  # write whole list again to the same file


def fix_host_and_ports(msg, project_name, host, port):
    """ 9. Fixing port / host -- update server, port in /api/expose_services.py """
    print(msg)  # 9. Fixing port / host
    replace_port = f':{port}' if port else ""
    replace_with = host + replace_port
    in_file = f'{project_name}/api/expose_services.py'
    replace_string_in_file(search_for="localhost:5000",
                           replace_with=replace_with,
                           in_file=in_file)
    print(f'.. ..Updated expose_services_py with port={port} and host={host}')
    full_path = os.path.abspath(project_name)
    replace_string_in_file(search_for="python_anywhere_path",
                           replace_with=full_path,
                           in_file=f'{project_name}/python_anywhere_wsgi.py')
    print(f'.. ..Updated python_anywhere_wsgi.py with {full_path}')


def fix_basic_web_app_app_init__inject_logic(project_directory, db_url):
    """ insert call LogicBank.activate into ui/basic_web_app/app/__init__.py """
    file_name = f'{project_directory}/ui/basic_web_app/app/__init__.py'
    proj = os.path.basename(project_directory)  # enable flask run
    import_fix = f'logic_bank_utils.add_python_path(project_dir="{proj}", my_file=__file__)\n'

    insert_text = ("\n# ApiLogicServer - enable flask fab create-admin\n"
                   "import logic_bank_utils.util as logic_bank_utils\n"
                   + import_fix +
                   "\nimport database.models as models\n"
                   + "from logic import declare_logic\n"
                   + "from logic_bank.logic_bank import LogicBank\n"
                   )
    if db_url.endswith("nw.sqlite"):    # admin pre-installed for nw, no need to disable logic
        insert_text += "LogicBank.activate(session=db.session, activator=declare_logic)\n\n"
    else:                               # logic interferes with create-admin - disable it
        insert_text += "# *** Enable the following after creating Flask AppBuilder Admin ***\n"
        insert_text += "# LogicBank.activate(session=db.session, activator=declare_logic)\n\n"
    insert_lines_at(lines=insert_text, at="appbuilder = AppBuilder(app, db.session)", file_name=file_name)


def fix_database_models__inject_db_types(project_directory: str, db_types: str):
    """ insert <db_types file> into database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    if db_types != "":
        print(f'.. ..Injecting file {db_types} into database/models.py')
        with open(db_types, 'r') as file:
            db_types_data = file.read()
        insert_lines_at(lines=db_types_data, at="(typically via --db_types)", file_name=models_file_name)


def fix_database_models__import_models_ext(project_directory: str):
    """ Append "from database import models_ext" to database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    print(f'.. ..Appending "from database import models_ext" to database/models.py')
    models_file = open(models_file_name, 'a')
    models_file.write("\n\nfrom database import models_ext\n")
    models_file.close()


def start_open_with(open_with: str, project_name: str):
    """ Creation complete.  Opening {open_with} at {project_name} """
    print(f'\nCreation complete - Opening {open_with} at {project_name}')
    print(".. See the readme for install / run instructions")
    run_command(f'{open_with} {project_name}', None, "no-msg")


def prepare_flask_appbuilder(msg: str,
                             project_directory: str, db_uri: str, db_url: str,
                             generate_from_model: GenerateFromModel):
    """ 8. Writing: /ui/basic_web_app/app/views.py """
    replace_string_in_file(search_for='"sqlite:///" + os.path.join(basedir, "app.db")',
                           replace_with='"' + db_uri + '"',
                           in_file=f'{project_directory}/ui/basic_web_app/config.py')
    print(msg)  # 8. Writing: /ui/basic_web_app/app/views.py
    text_file = open(project_directory + '/ui/basic_web_app/app/views.py', 'w')
    text_file.write(generate_from_model.result_views)
    text_file.close()
    print(".. ..Fixing run.py and app/init for Python path, logic")
    if not db_url.endswith("nw.sqlite"):
        print(".. ..Important: you will need to run flask fab create-admin")
    fix_basic_web_app_run__python_path(project_directory)
    fix_basic_web_app_run__create_admin(project_directory)
    fix_basic_web_app_app_init__inject_logic(project_directory, db_url)


def print_options(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, extended_builder: str):
    """ Creating ApiLogicServer with options:"""
    print_options = True
    if print_options:
        print(f'\n\nCreating ApiLogicServer with options:')
        print(f'  --db_url={db_url}')
        print(f'  --project_name={project_name}')
        print(f'  --flask_appbuilder={flask_appbuilder}')
        print(f'  --from_git={from_git}')
        #        print(f'  --db_types={db_types}')
        print(f'  --run={run}')
        print(f'  --host={host}')
        print(f'  --port={port}')
        print(f'  --not_exposed={not_exposed}')
        print(f'  --open_with={open_with}')
        print(f'  --use_model={use_model}')
        print(f'  --favorites={favorites}')
        print(f'  --non_favorites={non_favorites}')
        print(f'  --extended_builder={extended_builder}')


def invoke_extended_builder(builder_path, db_url, project_directory):
    # spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
    spec = importlib.util.spec_from_file_location("module.name", builder_path)
    extended_builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extended_builder)  # runs "bare" module code (e.g., initialization)
    extended_builder.extended_builder(db_url, project_directory)  # extended_builder.MyClass()


def invoke_nw_tests(builder_path, db_url, project_directory):
    # spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
    nw_tests_path = abspath(f'{abspath(get_api_logic_server_dir())}/api_logic_server_cli/nw_tests.py')
    spec = importlib.util.spec_from_file_location("module.name", nw_tests_path)
    nw_tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nw_tests)  # runs "bare" module code (e.g., initialization)
    nw_tests.nw_tests(db_url, project_directory)  # extended_builder.MyClass()


def api_logic_server(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, extended_builder: str):

    """ Creates logic-enabled Python JSON_API project, options for FAB and execution - main driver """

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
    print_options(project_name = project_name, db_url=db_url, host=host, port=port, not_exposed=not_exposed,
                  from_git=from_git, db_types=db_types, open_with=open_with, run=run, use_model=use_model,
                  flask_appbuilder=flask_appbuilder, favorites=favorites, non_favorites=non_favorites,
                  extended_builder=extended_builder)
    print(f"\nApiLogicServer {__version__} Creation Log:")

    abs_db_url = db_url
    if abs_db_url == "":
        print(f'0. Using demo default db_url: sqlite:///{abspath(get_api_logic_server_dir())}/api_logic_server_cli/nw.sqlite')
        abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/api_logic_server_cli/nw.sqlite'
    if extended_builder == "*":
        extended_builder = abspath(f'{abspath(get_api_logic_server_dir())}/api_logic_server_cli/extended_builder.py')
        print(f'0. Using default extended_builder: {extended_builder}')
    if db_url.startswith('sqlite:///'):
        url = db_url[10: len(db_url)]
        abs_db_url = abspath(url)
        abs_db_url = 'sqlite:///' + abs_db_url
        pass

    project_directory = resolve_home(project_name)
    """user-supplied project_name, less the twiddle. Typically relative to cwd. """

    clone_prototype_project_with_nw_samples(project_directory, from_git, "2. Create Project", db_url)

    print(f'3. Create {project_directory + "/database/models.py"} via expose_existing_callable / sqlacodegen: {db_url}')
    create_models(abs_db_url, project_directory, use_model)  # exec's sqlacodegen
    fix_database_models__inject_db_types(project_directory, db_types)

    if flask_appbuilder:
        create_basic_web_app(abs_db_url, project_directory, "4. Create ui/basic_web_app")
    else:
        print("4. ui/basic/web_app creation declined")

    print("5. Create api/expose_api_models.py and ui/basic_web_app/app/views.py (import / iterate models)")
    generate_from_model = GenerateFromModel(  # Create views.py file from db, models.py
        project_name=project_directory, db_url=abs_db_url, host=host, port=port,
        not_exposed=not_exposed + " ", favorite_names=favorites, non_favorite_names=non_favorites)
    generate_from_model.generate_api_expose_and_ui_views()  # sets generate_from_model.result_apis & result_views

    print("6. Writing: /api/expose_api_models.py")
    write_expose_api_models(project_directory, generate_from_model.result_apis)
    if use_model == "":
        fix_database_models__import_models_ext(project_directory)

    print("7. Update api_logic_server_run.py and config.py with project_name and db_url")
    db_uri = update_api_logic_server_run__and__config(project_name, project_directory, abs_db_url, host, port)

    if flask_appbuilder:
        prepare_flask_appbuilder(msg="8. Writing: /ui/basic_web_app/app/views.py",
                                 project_directory=project_directory,
                                 db_uri=db_uri, db_url=db_url, generate_from_model=generate_from_model)

    fix_host_and_ports("9. Fixing port / host", project_directory, host, port)

    if extended_builder is not None and extended_builder !="":
        print(f'10. Invoke extended_builder: {extended_builder}({db_url}, {project_directory})')
        invoke_extended_builder(extended_builder, db_url, project_directory)

    if open_with != "":
        start_open_with(open_with=open_with, project_name=project_name)

    if run:
        run_file = os.path.abspath(f'{project_directory}/api_logic_server_run.py')
        run_command(f'python {run_file} {host}',
                    msg="\nRun created ApiLogicServer project")  # sync run of server - does not return

        if db_url.endswith("nw.sqlite"):
            invoke_nw_tests(builder_path=extended_builder, db_url=db_url, project_directory=project_directory)

    else:
        print("\nApiLogicServer customizable project created.  Next steps:")
        print(f'..cd {project_name}')
        print(f'..python api_logic_server_run.py')
        print(f'..python ui/basic_web_app/run.py')


@click.group()
@click.pass_context
def main(ctx):
    """
    Creates and runs logic-enabled Python project.

        Examples:

            ApiLogicServer run  # use defaults (verify install)

            ApiLogicServer run --db_url=sqlite:///nw.sqlite

        Doc:

            ApiLogicServer: https://github.com/valhuber/ApiLogicServer#readme

            Logic Bank: https://github.com/valhuber/logicbank#readme

            SQLAlchemy: https://docs.sqlalchemy.org/en/14/core/engines.html

            SAFRS: https://github.com/thomaxxl/safrs/wiki

            FAB: https://flask-appbuilder.readthedocs.io/en/latest/

    https://github.com/valhuber/ApiLogicServer/wiki/Tutorial
    """


@main.command("version")
@click.pass_context
def version(ctx):
    """
        Recent Changes.
    """
    print(f'\tInstalled at {abspath(__file__)}\n')
    print(f'\thttps://github.com/valhuber/ApiLogicServer/wiki/Tutorial\n')
    click.echo(
        click.style(
            f'Recent Changes:\n'
            "\t05/27/2021 - 02.02.28: Flask AppBuilder 3.3.0\n"
            "\t05/26/2021 - 02.02.27: Clearer logicbank multi-table chain log - show attribute names\n"
            "\t05/23/2021 - 02.02.19: TVF multi-row fix; ApiLogicServer Summary - Console Startup Banner\n"
            "\t05/21/2021 - 02.02.17: SAFRS Patch Error Fix, model gen for Posting w/o autoIncr, Startup Tests\n"
            "\t05/10/2021 - 02.02.09: Extended Builder fix - no-arg TVFs\n"
            "\t05/08/2021 - 02.02.08: Server Startup Option\n"
            "\t05/03/2021 - 02.01.05: --extended_builder - bypass Scalar Value Functions\n"
            "\t04/30/2021 - 02.01.04: --extended_builder - multiple Table Value Functions example running\n"
            "\t04/27/2021 - 02.01.01: Improved Svcs, option --extended_builder (e.g., restify Table Value Functions)\n"
            "\t04/23/2021 - 02.00.15: Bug fix - SQLAlchemy version, server port\n"
            "\t04/21/2021 - 02.00.14: pythonanywhere - port option, wsgi creation\n"
            "\t04/13/2021 - 02.00.10: Improved model error recovery; fix sql/server char type (issues # 13)\n"
            "\t04/11/2021 - 02.00.06: Minor - additional CLI info\n"
            "\t04/09/2021 - 02.00.05: Bug Fix - View names with spaces\n"
            "\t03/23/2021 - 02.00.01: Minor doc changes, CLI argument simplification for default db_url\n"
            "\t03/17/2021 - 02.00.00: Create create_admin.sh, copy sqlite3 DBs locally, model_ext\n"
            "\t03/10/2021 - 01.04.10: Fix issues in creating Basic Web App\n"
            "\t03/03/2021 - 01.04.09: Services, cleanup main api_run\n"
        )
    )


@main.command("create")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default="api_logic_server",
              help="Create new directory here")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=False,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--flask_appbuilder/--no-flask_appbuilder',
              default=True, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5000',
              help="Port (default 5000, or leave empty)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def create(ctx, project_name: str, db_url: str, not_exposed: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           flask_appbuilder: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           favorites: str, non_favorites: str,
           extended_builder: str):

    db_types = ""
    if db_url == default_db:
        db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/api_logic_server_cli/nw.sqlite'
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


@main.command("run")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default="api_logic_server",
              help="Create new directory here")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=True,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--flask_appbuilder/--no-flask_appbuilder',
              default=True, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5000',
              help="Port (default 5000, or leave empty)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def run(ctx, project_name: str, db_url: str, not_exposed: str,
        from_git: str,
        # db_types: str,
        open_with: str,
        run: click.BOOL,
        flask_appbuilder: click.BOOL,
        use_model: str,
        host: str,
        port: str,
        favorites: str, non_favorites: str,
        extended_builder: str):

    db_types = ""
    if db_url == default_db:
        db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/api_logic_server_cli/nw.sqlite'
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


log = logging.getLogger(__name__)


def print_info():
    """
    Creates and optionally runs a customizable ApiLogicServer project, Example

    URI examples, Docs URL
    """
    info = [
        '',
        'Creates and optionally runs a customizable ApiLogicServer project',
        '',
        'Examples:',
        '  ApiLogicServer run',
        '  ApiLogicServer run --db_url=sqlite:///nw.sqlite',
        '  ApiLogicServer run --db_url=mysql+pymysql://root:p@localhost/classicmodels',
        '  ApiLogicServer run --db_url=postgresql://postgres:p@10.0.0.234/postgres]',
        '  ApiLogicServer run --db_url=mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no',
        '  ApiLogicServer create --host=ApiLogicServer.pythonanywhere.com --port=',
        '',
        'Where --db_url defaults to supplied sample, or, specify URI for your own database:',
        '   SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html',
        '   Other URI examples:           https://github.com/valhuber/ApiLogicServer/wiki/Testing',
        ' ',
        'Docs: https://github.com/valhuber/ApiLogicServer#readme\n'
    ]
    for each_line in info:
        sys.stdout.write(each_line + '\n')
    sys.stdout.write('\n')


def print_args(args, msg):
    print(msg)
    for each_arg in args:
        print(f'  {each_arg}')
    print(" ")


def start():               # target of setup.py
    sys.stdout.write("\nWelcome to API Logic Server CLI, " + __version__ + "\n")
    print_info()
    # sys.stdout.write("    SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html\n")
    # sys.stdout.write("    Other examples are at:        https://github.com/valhuber/ApiLogicServer/wiki/Testing\n\n")
    main(obj={})


if __name__ == '__main__':  # debugger & python command line start here
    # eg: python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project
    # unix: python api_logic_server_cli/cli.py create --project_name=/home/api_logic_server
    (did_fix_path, sys_env_info) = \
        logic_bank_utils.add_python_path(project_dir="ApiLogicServer", my_file=__file__)

    print(f'\nWelcome to API Logic Server CLI Utility, {__version__}')
    print_info()
    commands = sys.argv
    if len(sys.argv) > 1 and sys.argv[1] != "version":
        print_args(commands, "Utility / Main - Command Line Arguments:")
    main()
