# -*- coding: utf-8 -*-
"""Generates FAB views.py file from db model.

For Dev: Install, Run, Deploy Instructions to test Command Line

    https://github.com/valhuber/fab-quick-start/wiki/Explore-fab-quick-start
    cd nw-app
    python ../fab_quick_start_util/fab_quick_start.py
    python ../fab_quick_start_util/fab_quick_start.py run

    cd banking/basic_web_app/
    python ../../fab_quick_start_util/fab_quick_start.py run

    cd nw-app
    virtualenv venv
    pip install ../../fab-quick-start

For Users: Usage
    FAB Quick Start Guide: https://github.com/valhuber/fab-quick-start/wiki
    FAB Quick Start Utility: https://github.com/valhuber/fab-quick-start

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
# import fab_quick_start_util.__init__  TODO
# __version__ = __init__.__version__
# fails 'method-wrapper' object has no attribute '__version__'.. work-around:
__version__ = "1.0.0"

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)


class FabQuickStart(object):
    """
    Iterate over all tables, create view statements for each
    """

    _result = ""

    _favorite_names_list = []  #: ["name", "description"]
    """
        array of substrings used to find favorite column name

        command line option to override per language, db conventions

        eg,
            name in English
            nom in French
    """
    favorite_names = "name description"  #: e.g. "nom, description"

    _non_favorite_names_list = []
    non_favorite_names = "id"

    _indent = "   "
    _tables_generated = set()  # to address "generate children first"
    num_pages_generated = 0
    num_related = 0

    def run(self) -> str:
        """
            Returns a string of views.py content

            This is the main entry.  Typical calling sequence:\r
                qs = FabQuickStart()\r
                qs.favorite_names = "nom description"\r
                qs.non_favorite_names = "id"\r
                qs.run()\r

            Parameters:
        """
        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

        cwd = os.getcwd()
        self._result += '"""'
        self._result += ("\nFab QuickStart " + __version__ + "\n\n"
                         + "Current Working Directory: " + cwd + "\n\n"
                         + "From: " + sys.argv[0] + "\n\n"
                         + "Using Python: " + sys.version + "\n\n"
                         + "Favorites: "
                         + str(self._favorite_names_list) + "\n\n"
                         + "Non Favorites: "
                         + str(self._non_favorite_names_list) + "\n\n"
                         + "At: " + str(datetime.datetime.now()) + "\n\n")
        sys.path.append(cwd)  # for banking Command Line test
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
                self._result += "Debug Mode fix for cwd: " + cwd + "\n\n"
            else:
                cwd = cwd.replace("fab-quick-start",
                                  "fab-quick-start/banking/basic_web_app", 1)
                cwd = cwd.replace("/fab_quick_start_util","")
                python_path = os.getcwd()
                python_path = python_path.replace('fab-quick-start',
                                                  'banking', 1)
                python_path = python_path.replace("/fab_quick_start_util","")
                sys.path.append(python_path)
                self._result += "Python Path includes: " + python_path + "\n\n"
            self._result += "Debug cmd override: " + cwd + "\n\n"
            #  print ("\n\n** debug path issues 2: \n\n" + self._result)
        #  print ("\n\n** debug path issues 1: \n\n" + self._result)
        self._result += '"""\n\n'  # look into fstring - nicer to read TODO
        metadata = self.find_meta_data(cwd)
        meta_tables = metadata.tables
        self._result += self.generate_module_imports()
        for each_table in meta_tables.items():
            each_result = self.process_each_table(each_table[1])
            self._result += each_result
        self._result += self.process_module_end(meta_tables)
        return self._result

    def find_meta_data(self, a_cwd: str) -> MetaData:
        """     Find Metadata from model, or (failing that), db

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

        if (do_dynamic_load):
            """
                a_cwd -- not-this-project-dir (e.g., nw-app)
                --app
                --|--__init__.py
                --|--models.py
                --config.py

                credit: https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
            """
            sys_path = str(sys.path)
            model_loaded = False
            try:
                # models =
                importlib.import_module('models')
                model_loaded = True
            except:
                pass  # one more try...
            if not model_loaded:
                sys.path.insert(0, a_cwd + '/app')
                #  e.g., adds /Users/val/python/vscode/fab-quickstart/nw-app/app
                #  print("DEBUG find_meta sys.path: " + str(sys.path))
                try:
                    # models =
                    importlib.import_module('models')
                except:
                    print("\n\nERROR - current result:\n" + self._result)
                    raise Exception("Unable to open models from:\n" +
                                    a_cwd + ", or\n" +
                                    a_cwd + '/app')

            sys.path.insert(0, a_cwd)
            config = importlib.import_module('config')
            conn_string = config.SQLALCHEMY_DATABASE_URI
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
        result += "from .models import *\n"
        result += "\n"
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
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            return "# skip admin table: " + table_name + "\n"
        elif table_name in self._tables_generated:
            log.debug("table already generated per recursion: " + table_name)
            return "# table already generated per recursion: " + table_name
        else:
            self._tables_generated.add(table_name)
            child_list = self.find_child_list(a_table_def)
            for each_child in child_list:  # recurse to ensure children first
                log.debug(".. but children first: " + each_child.name)
                result += self.process_each_table(each_child)
                self._tables_generated.add(each_child.name)
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

        Creates instant web app - generates fab views contents.

\b
        fab is Flask Application Builder\r
            Docs:        https://flask-appbuilder.readthedocs.io/en/latest/\r
            Quick Start: https://github.com/valhuber/fab-quick-start/wiki

\b
        fab-quick-start\r
            Docs:       https://github.com/valhuber/fab-quick-start

\b
        Usage\r
        =====\r
            1. Generate a fab project\r
            2. Complete your models file (consider sqlacodegen)\r
                https://pypi.org/project/sqlacodegen/\r
                NB: Be sure to use the --noviews option\r
                NB: Add relationships missing in db to get related_views\r
            3. cd to directory containing your config.py file:\r
                cd <my_project> \r
                --app\r
                --|--__init__.py\r
                --|--models.py\r
                __|--views.py\r
                --config.py\r
            4. fab_quickstart run\r
            5. copy output over app/views.py
            6. cd my_project; flask run
    """


@main.command("run")
@click.option('--favorites',
              default="name description",
              prompt="Favorite Column Names",
              help="Word(s) identifying 'favorite name' (displayed first)")
@click.option('--non_favorites',
              default="id",
              prompt="Non Favorite Column Names",
              help="Word(s) used to identify last-shown fields")
@click.pass_context
def run(ctx, favorites: str, non_favorites: str):

    """
        Create views.py file from db, models.py
    """
    fab_quick_start = FabQuickStart()
    fab_quick_start.favorite_names = favorites
    fab_quick_start.non_favorite_names = non_favorites
    fab_quick_start.run()

    print("\n" + fab_quick_start._result)


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
    sys.stderr.write("\n\nfab-quick-start " + __version__ + " here\n\n")
    main(obj={})  # TODO - main(a,b) fails to work for --help


if __name__ == '__main__':
    commands = (
        'run',
        '--favorites=name description',
        '--non_favorites=id',
    )
    main(commands)
    # start()
