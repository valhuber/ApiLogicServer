# -*- coding: utf-8 -*-
"""
Given a database url,
create ApiLogicServer project by cloning ApiLogicServerProto,
in particular create the ui/basic_web_app/app/views.py
and api/expose_api_models.

CAREFUL!!
    This is copy / alteration of fab-quick-start, but the comments etc are all out of date.
    Don't believe anything you read (pretend it's the Internet).

For Dev: Install, Run, Deploy Instructions to test Command Line

    python ../fab_quick_start_util/create_server.py
    python ../fab_quick_start_util/create_server.py run

    cd nw-app
    virtualenv venv
    pip install ../../ApiLogicServer

For Users: Usage
    FAB Quick Start Guide: https://github.com/valhuber/ApiLogicServer
    FAB Quick Start Guide: https://github.com/valhuber/ApiLogicServerProto

Urgent
    None

New Quick Start Features:
    * Some minor relationships may be missing in models.py
    * Recognize other views, such as Maps
    * Suppress Master on Child (no Order# on each Order Detail)
        ** Big deal, since can't re-use child on multiple different parents.
        ** Ugh

New FAB Feature Suggestions:
    * Lookups (find/choose Product for Order Detail)
    * Better col/field captions
    * Updatable list (=> multi-row save)
    * Hide/show field (& caption)
    * Page (instruction) notes
"""
import builtins
import subprocess
from os.path import abspath
from os.path import realpath
from pathlib import Path

import logic_bank_utils.util as logic_bank_utils
from flask import Flask

import logging
import datetime
from typing import NewType
import sys
from sys import platform
import os
import sqlalchemy
import sqlalchemy.ext
from sqlalchemy import MetaData
import inspect
import importlib
import click
# import fab_quick_start_util.__init__  TODO
# __version__ = __init__.__version__
# fails 'method-wrapper' object has no attribute '__version__'.. work-around:
__version__ = "1.0.6"

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


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
    _tables_generated = set()  # to address "generate children first"
    num_pages_generated = 0
    num_related = 0

    def __init__(self,
                 project_name: str ="~/Desktop/my_project",
                 db_url: str = "sqlite:///nw.sqlite",
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id"):
        self.project_name = project_name
        self.db_url = db_url
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_name = non_favorite_names

    def generate(self):
        """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

        cwd = os.getcwd()
        self.result_views += '"""'
        self.result_apis += '"""'
        self.result_views += ("\nApiLogicServer Generate From Model " + __version__ + "\n\n"
                              + "From: " + sys.argv[0] + "\n\n"
                              + "Using Python: " + sys.version + "\n\n"
                              + "Favorites: "
                              + str(self._favorite_names_list) + "\n\n"
                              + "Non Favorites: "
                              + str(self._non_favorite_names_list) + "\n\n"
                              + "At: " + str(datetime.datetime.now()) + "\n\n")
        self.result_apis += ("\nApiLogicServer Generate From Model " + __version__ + "\n\n"
                             + "From: " + sys.argv[0] + "\n\n"
                             + "Using Python: " + sys.version + "\n\n"
                             + "At: " + str(datetime.datetime.now()) + "\n\n"
                             + '"""\n\n')
        sys.path.append(cwd)  # for banking Command Line test

        enable_cli_hack = False  # awful stuff, want to remove, keep for now...
        if enable_cli_hack:
            if ("fab-quick-start" in cwd and "nw" not in cwd and
                    "banking" not in cwd):
                # sorry, this is just to enable run cli/base, *or" by python cli.py
                # need to wind up at .... /nw-app, or /banking/db
                # AND have that in sys.path
                use_nw = True
                if use_nw:
                    cwd = cwd.replace("fab-quick-start",
                                      "fab-quick-start/nw-app", 1)
                    cwd = cwd.replace("/fab_quick_start_util","")
                    self.result_views += "Debug Mode fix for cwd: " + cwd + "\n\n"
                else:
                    cwd = cwd.replace("fab-quick-start",
                                      "fab-quick-start/banking/basic_web_app", 1)
                    cwd = cwd.replace("/fab_quick_start_util","")
                    python_path = os.getcwd()
                    python_path = python_path.replace('fab-quick-start',
                                                      'banking', 1)
                    python_path = python_path.replace("/fab_quick_start_util","")
                    sys.path.append(python_path)
                    self.result_views += "Python Path includes: " + python_path + "\n\n"
                self.result_views += "Debug cmd override: " + cwd + "\n\n"
                #  print ("\n\n** debug path issues 2: \n\n" + self._result)
            #  print ("\n\n** debug path issues 1: \n\n" + self._result)

        self.result_views += '"""\n\n'  # look into fstring - nicer to read TODO
        metadata = self.find_meta_data(cwd, self.project_name, self.db_url)
        meta_tables = metadata.tables
        self.result_views += self.generate_module_imports()
        for each_table in meta_tables.items():
            each_result = self.process_each_table(each_table[1])
            self.result_views += each_result
        self.result_views += self.process_module_end(meta_tables)
        return

    def find_meta_data(self, a_cwd: str, a_project_name: str, a_db_url) -> MetaData:
        """     Find Metadata by importing model, or (failing that), db

        a_cmd should be

            Metadata contains definition of tables, cols & fKeys (show_related)
            It can be obtained from db, *or* models.py; important because...
                Many DBs don't define FKs into the db (e.g. nw.db)
                Instead, they define "Virtual Keys" in their model files
                To find these, we need to get Metadata from models, not db
            So, we need to
                1. Import the models, via a location-relative dynamic import
                2. Find the Metadata from the imported models:
                    a. Find cls_members in models module
                    b. Locate first user model, use its metadata property
            #  view_metadata = models.Order().metadata  # class var, non ab_

            All this is doing is:
                    from <cwd>/app import models(.py) as models

        """

        conn_string = None
        do_dynamic_load = True
        project_abs_path = abspath(a_project_name)

        if (do_dynamic_load):
            """
                a_cwd -- see ApiLogicServerProto for structure

                credit: https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
            """
            sys_path = str(sys.path)
            # db = SQLAlchemy()
            # db = builtins.db = SQLAlchemy(app)  # set db as a global variable to be used models

            # from app_logic_server.my_project.app import create_app  # FIXME no way this can work
            def create_app(config_filename=None, host="localhost"):
                from flask_sqlalchemy import SQLAlchemy
                from sqlalchemy.orm import Session
                from sqlalchemy.ext.declarative import declarative_base
                import safrs

                app = Flask("API Logic Server")
                import app_logic_server.config as app_logic_server_config
                app.config.from_object(app_logic_server_config.Config)
                db = safrs.DB
                db.init_app(app)
                return app

            app = create_app()
            app.config.SQLALCHEMY_DATABASE_URI = a_db_url
            app.app_context().push()  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
            model_imported = False
            try:
                # models =
                importlib.import_module('database/models')
                model_imported = True
            except:
                pass  # keep looking...
            if not model_imported:
                sys.path.insert(0, project_abs_path + "/database")
                #  e.g., adds /Users/val/Desktop/my_project/database
                print(f'..Dynamic model import using sys.path: {project_abs_path + "/database"}')  # str(sys.path))
                try:
                    # models =
                    importlib.import_module('models')
                except:
                    pass  # once more...
                    print("\n\nERROR - current result:\n" + self.result_views)
                    # The sqlalchemy extension was not registered to the current application.  Please make sure to call init_app() first.
                    raise Exception("Unable to import models from:\n" +
                                    project_abs_path + "/database, or" +
                                    a_cwd + ", or\n" +
                                    a_cwd + '/app')

            # sys.path.insert(0, a_cwd)  # success - models open
            # config = importlib.import_module('config')
            conn_string = app.config.SQLALCHEMY_DATABASE_URI
        else:  # TODO - use dynamic loading (above), remove this when stable
            import models
            conn_string = "sqlite:///nw/nw.db"

        orm_class = None
        metadata = None
        cls_members = inspect.getmembers(sys.modules["models"],
                                         inspect.isclass)
        for each_cls_member in cls_members:
            each_class_def_str = str(each_cls_member)
            #  such as ('Category', <class 'models.Category'>)
            if ("'models." in str(each_class_def_str) and
                    "Ab" not in str(each_class_def_str)):
                orm_class = each_cls_member
                break
        if (orm_class is not None):
            log.debug("using sql for meta, from model: " + str(orm_class))
            metadata = orm_class[1].metadata
        # metadata = None  # enable to explore db with no fKeys

        engine = sqlalchemy.create_engine(conn_string)

        # connection =
        engine.connect()
        if (metadata is None):
            log.debug("using db for meta (models not found")
            metadata = MetaData()
        metadata.reflect(bind=engine, resolve_fks=True)
        return metadata

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
        if "TRANSFERFUND" in table_name:
            log.debug("special table")  # debug stop here
        if (table_name + " " in self.not_exposed):
            return "# not_exposed: api.expose_object(models.{table_name})"
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            return "# skip admin table: " + table_name + "\n"
        elif table_name in self._tables_generated:
            log.debug("table already generated per recursion: " + table_name)
            return "# table already generated per recursion: " + table_name
        elif 'sqlite_sequence' in table_name:
            return "# skip sqlite_sequence table: " + table_name + "\n"
        else:
            self._tables_generated.add(table_name)
            child_list = self.find_child_list(a_table_def)
            for each_child in child_list:  # recurse to ensure children first
                log.debug(".. but children first: " + each_child.name)
                result += self.process_each_table(each_child)
                self._tables_generated.add(each_child.name)

            if self.num_pages_generated == 0:
                self.result_apis += \
                    'def expose_models(app, HOST="localhost", PORT=5000, API_PREFIX="/api"):\n'
                self.result_apis += '    """this is called by api / __init__.py"""\n\n'
                self.result_apis += \
                    '    api = SAFRSAPI(app, host=HOST, port=PORT)\n'
            self.result_apis += f'    api.expose_object(models.{table_name})\n'

            self.num_pages_generated += 1

            model_name = self.model_name(table_name)
            class_name = a_table_def.name + model_name
            result += "\n\n\nclass " + class_name + "(" + model_name + "):\n"
            result += (
                self._indent + "datamodel = SQLAInterface(" +
                a_table_def.name + ")\n"
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
                + class_name
                + ", "
                + '"'
                + table_name
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
        if (a_table_def.name == "OrderDetail"):
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
            if (self.is_non_favorite_name(each_column.name.lower())):
                id_column_names.add(each_column.name)
                continue  # ids are boring - do at end
            column_count += 1
            if column_count > a_max_columns:  # - Todo - maybe cmd arg?
                break
            if column_count > 1:
                result += ", "
            result += '"' + each_column.name + '"'
        for each_id_column_name in id_column_names:
            column_count += 1
            if (column_count > a_max_id_columns):
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
        if a_table_def.name == "OrderDetail":  # for debug
            log.debug("predictive_joins for: " + a_table_def.name)
        for each_foreign_key in foreign_keys:
            each_parent_name = each_foreign_key.target_fullname
            loc_dot = each_parent_name.index(".")
            each_parent_name = each_parent_name[0:loc_dot]
            each_parent = a_table_def.metadata.tables[each_parent_name]
            favorite_column_name = self.favorite_column_name(each_parent)
            result.add(each_parent_name + "." + favorite_column_name)
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
            if (each_non_favorite_name in a_name):
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
        for each_child in child_list:
            related_count += 1
            if related_count > 1:
                result += ", "
            else:
                self.num_related += 1
            result += each_child.fullname + self.model_name(each_child)
        result += "]\n"
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

    def model_name(self, a_table_name: str):  # override as req'd
        """
            returns view model_name for a_table_name, defaulted to "ModelView"

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
        if (self.num_related == 0):
            result += "#  Warning - no related_views,"
            result += " since foreign keys missing\n"
            result += "#  .. add them to your models.py (see nw example)\n"
            result += "#  .. or better, add them to your database"
        return result


def delete_dir(dir_path):
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

        print(f'Delete dir: {dir_path}')
        import shutil
        use_callback = False
        if use_callback:
            shutil.rmtree(dir_path, ignore_errors=False, onerror=handleRemoveReadonly)
        else:
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                pass
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
    :param msg: optional message
    :return:
    """
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    print(f'{log_msg} {cmd}')

    use_env = env
    if env is None:
        project_dir = get_project_dir()
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
        result_b = subprocess.check_output(cmd, shell=True)
    result = str(result_b)  # b'pyenv 1.2.21\n'
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    if result != "" and result != "Downloaded the skeleton app, good coding!":
        print(f'{log_msg} {cmd} result: {spaces}{result}')


def clone_prototype_project(project_name: str):
    """
    clone prototype to create and remove git folder

    :param project_name: name of project created
    :return: result of cmd
    """
    remove_project_debug = True
    if remove_project_debug:
        delete_dir(realpath(project_name))
    cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project_name
    result = run_command(cmd, msg="Create Project")
    delete_dir(f'{project_name}/.git')

    replace_string_in_file(search_for="creation-date",
                           replace_with=str(datetime.datetime.now()),
                           in_file=f'{project_name}/readme.md')
    replace_string_in_file(search_for="cloned-from",
                           replace_with="https://github.com/valhuber/ApiLogicServerProto.git",
                           in_file=f'{project_name}/readme.md')

    pass


def create_basic_web_app(db_url, project_name):
    project_abs_path = abspath(project_name)
    fab_project = project_abs_path + "/ui/basic_web_app"
    cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
    result = run_command(cmd, msg="Create ui/basic_web_app")
    pass


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def create_models(db_url: str, project: str) -> str:

    class DotDict(dict):
        """dot.notation access to dictionary attributes"""
        # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    def get_codegen_args():
        codegen_args = DotDict({})
        codegen_args.url = db_url
        # codegen_args.outfile = models_file
        codegen_args.outfile = project + '/database/models.py'
        codegen_args.version = False
        return codegen_args

    use_approach = "expose_existing"
    if use_approach == "sqlacodeGen_main":
        import expose_existing.sqlacodegen.sqlacodegen.main as gen_models
        print(f'Create {project + "/database/models.py"} via sqlacodegen: {db_url}')
        code_gen_args = get_codegen_args()
        gen_models.main(code_gen_args)
    elif use_approach == "expose_existing":  # preferred version - Thomas' model fixup (etc)
        import expose_existing.expose_existing_callable as expose_existing
        print(f'Create {project + "/database/models.py"} via expose_existing / sqlacodegen: {db_url}')
        code_gen_args = get_codegen_args()
        expose_existing.codegen(code_gen_args)
        pass
    else:
        # PYTHONPATH=sqlacodegen/ python3 sqlacodegen/sqlacodegen/main.py mysql+pymysql://root:password@localhost/mysql > examples/models.py
        cmd_debug = f'python ../expose_existing/sqlacodegen/sqlacodegen/main.py '
        abs_cmd_debug = abspath(cmd_debug)
        project_dir = get_project_dir()
        python_path = str(project_dir) + "/venv/lib/python3.9/site_packages"
        env_list = os.environ.copy()
        # env_list["PATH"] = "/usr/sbin:/sbin:" + env_list["PATH"]
        """
        env_list["PYTHONPATH"] = python_path + ":" + env_list["PYTHONPATH"]  # python_path  # e.g., /Users/val/dev/ApiLogicServer/venv/lib/python3.9
        """
        cmd = f'python {project_dir}/expose_existing/sqlacodegen/sqlacodegen/main.py '
        cmd += db_url
        cmd += '  > ' + project + '/database/models.py'
        # env_list = {}
        # 'python ../expose_existing/sqlacodegen/sqlacodegen/main.py sqlite:///db.sqlite  > my_project/database/models.py'
        result = run_command(cmd, msg="Create database/models.py")  # might fail per venv, looking for inflect
        pass


def write_expose_api_models(project_name, apis):
    text_file = open(project_name + '/api/expose_api_models.py', 'a')
    text_file.write(apis)
    text_file.close()


def replace_string_in_file(search_for: str, replace_with: str, in_file: str):
    with open(in_file, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace(search_for, replace_with)
    with open(in_file, 'w') as file:
        file.write(file_data)


def get_os_url(url: str) -> str:
    """ idiotic fix for windows (\ --> \\\\)

    https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file"""
    return url.replace('\\', '\\\\')


def fix_basic_web_app_python_path(abs_project_name):
    """ prepend logic_bank_utils call to fixup python path """
    file_name = f'{abs_project_name}/ui/basic_web_app/run.py'
    proj = os.path.basename(abs_project_name)
    insert_text = ("\nimport logic_bank_utils.util as logic_bank_utils\n"
                   + f'logic_bank_utils.add_python_path(project_dir="{proj}", my_file=__file__)\n\n')
    with open(file_name, 'r+') as fp:
        lines = fp.readlines()  # lines is list of line, each element '...\n'
        lines.insert(0, insert_text)  # you can use any index if you know the line index
        fp.seek(0)  # file pointer locates at the beginning to write the whole file again
        fp.writelines(lines)  # write whole lists again to the same file


def inject_logic(abs_project_name):
    """ insert call LogicBank.activate """
    file_name = f'{abs_project_name}/ui/basic_web_app/app/__init__.py'
    insert_text = ("\nimport database.models as models\n"
                   + "from logic import declare_logic\n"
                   + "from logic_bank.logic_bank import LogicBank\n"
                   + "LogicBank.activate(session=db.session, activator=declare_logic)\n\n"
                   )
    with open(file_name, 'r+') as fp:
        lines = fp.readlines()  # lines is list of line, each element '...\n'
        found = False
        insert_line = 0
        for each_line in lines:
            if "appbuilder = AppBuilder(app, db.session)" in each_line:
                found = True
                break
            insert_line += 1
        if not found:
            raise Exception("Internal error - unable to find logic insert point")
        lines.insert(insert_line, insert_text)  # you can use any index if you know the line index
        fp.seek(0)  # file pointer locates at the beginning to write the whole file again
        fp.writelines(lines)  # write whole lists again to the same file


'''
            CLI

            fab-quick-start --help
            fab-quick-start version
            fab-quick-start run [--favorites=string] [--non_favorites=string]
'''


@click.group()
@click.pass_context
def main(ctx):
    """
    Creates ApiLogicServer project:\r
    """


@main.command("create")
@click.option('--project_name',
              default="new_api_logic_server",
              prompt="Name of Project to be created",
              help="Will be new directory at current location")
@click.option('--db_url',
              default=f'sqlite:///{abspath(get_project_dir())}/app_logic_server/nw.sqlite',
              prompt="Database URL",
              help="SQLAlchemy Database URL")
@click.option('--not_exposed',
              default="ProductDetails_V",
              prompt="Tables Not Exposed",
              help="These tables are not written to api/expose_api_models.py")
@click.option('--flask_appbuilder/--no-flask_appbuilder',
              default=True,
              prompt="Generate Flask AppBuilder",
              help="Creates <project_name>/ui/basic_web_app")
@click.option('--favorites',
              default="name description",
              prompt="Favorite Column Names",
              help="Word(s) identifying 'favorite name' (displayed first)")
@click.option('--non_favorites',
              default="id",
              prompt="Non Favorite Column Names",
              help="Word(s) used to identify last-shown fields")
@click.pass_context
def create(ctx, project_name: str, db_url: str, not_exposed: str,
        flask_appbuilder: bool, favorites: str, non_favorites: str):
    """
    Creates a Python Project from an existing database:

        * JSON:API, via SAFRS

        * basic_web_app, via Flask AppBuilder and fab-quick-start

        * add spreadsheet like rules for derivations and constraints, via LogicBank

    """
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
    abs_db_url = db_url
    if db_url.startswith('sqlite:///'):
        url = db_url[10: len(db_url)]
        abs_db_url = abspath(url)
        abs_db_url = 'sqlite:///' + abs_db_url
        pass

    abs_project_name = project_name
    if abs_project_name.startswith("~"):
        abs_project_name = str(Path.home()) + project_name[1:]

    create_project_debug = True
    if create_project_debug:
        clone_prototype_project(abs_project_name)
        create_models(abs_db_url, abs_project_name)  # exec's sqlacodegen

    if flask_appbuilder:
        create_basic_web_app(abs_db_url, abs_project_name)

    """
        Create views.py file from db, models.py
    """
    generate_from_model = GenerateFromModel(
        project_name=abs_project_name,
        db_url=abs_db_url,
        not_exposed=not_exposed + " ",
        favorite_names=favorites,
        non_favorite_names=non_favorites
    )
    print("Create ui/basic_web_app/app/views.py and api/expose_api_models.py (import / iterate models)")
    generate_from_model.generate()  # sets generate_from_model.result_apis & result_views

    print("Writing: /api/expose_api_models.py")
    write_expose_api_models(abs_project_name, generate_from_model.result_apis)

    print("Update api_logic_server_run.py, config.py and ui/basic_web_app/config.py with project_name and db_url")
    replace_string_in_file(search_for="replace_project_name",
                           replace_with=os.path.basename(project_name),
                           in_file=f'{abs_project_name}/api_logic_server_run.py')
    replace_string_in_file(search_for="replace_db_url",
                           replace_with=get_os_url(abs_db_url),
                           in_file=f'{abs_project_name}/config.py')
    # ApiLogicServer hello "At: " + str(datetime.datetime.now())
    replace_string_in_file(search_for="ApiLogicServer hello",
                           replace_with="ApiLogicServer generated at:" + str(datetime.datetime.now()),
                           in_file=f'{abs_project_name}/api_logic_server_run.py')

    if flask_appbuilder:
        replace_string_in_file(search_for='"sqlite:///" + os.path.join(basedir, "app.db")',  # odd extra paren...
                               replace_with='"' + get_os_url(abs_db_url) + '"',
                               in_file=f'{abs_project_name}/ui/basic_web_app/config.py')
        print("Writing: /ui/basic_web_app/app/views.py")
        text_file = open(abs_project_name + '/ui/basic_web_app/app/views.py', 'w')
        text_file.write(generate_from_model.result_views)
        text_file.close()
        fix_basic_web_app_python_path(abs_project_name)
        inject_logic(abs_project_name)

    print("\nCreation complete.  Next steps:")
    print(f'..cd {project_name}')
    print(f'..virtualenv venv')
    print(f'..source venv/bin/activate  # windows: venv\Scripts\activate')
    print(f'..pip install -r requirements.txt')
    print(f'..python api_logic_server_run.py')
    print(f'..python ui/basic_web_app/run.py')


@main.command("version")
@click.pass_context
def version(ctx):
    """
        Recent Changes
    """
    click.echo(
        click.style(
            "\nInitial Version\n\n"
        )
    )


log = logging.getLogger(__name__)


def start():  # target of setup.py
    sys.stderr.write("\n\nAPI Logic Server Creation Utility " + __version__ + " here\n\n")
    main(obj={})  # TODO - main(a,b) fails to work for --help


if __name__ == '__main__':  # debugger & cmd-line start here

    (did_fix_path, sys_env_info) = \
        logic_bank_utils.add_python_path(project_dir="ApiLogicServer", my_file=__file__)

    print("\n\nAPI Logic Server Creation " + __version__ + " here\n")
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    if len(sys.argv) > 1:
        """ eg
        cd app_logic_server
        python create_server.py --project_name=~/Desktop/test_project
        """
        print("\nAPI Logic Server Creation " + __version__ + " here\n")
        commands = sys.argv
        commands[0] = "create"
    else:
        print("\nAPI Logic Server Creation " + __version__ + " (no args, using debug defaults)\n")
        db_url = "sqlite:///" + os.path.dirname(__file__) + "/nw.sqlite"

        commands = (
            'create',
            '--project_name=~/Desktop/my_project',
            '--not_exposed=ProductDetails_V',
            '--flask_appbuilder',
            f'--db_url={db_url}',  # FIXME verify
            '--favorites=name description',
            '--non_favorites=id',
        )
    main(commands)
    # start()
