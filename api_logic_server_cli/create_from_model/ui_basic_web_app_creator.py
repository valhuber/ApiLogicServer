import logging
import datetime
import sys, os
from os.path import abspath
from typing import NewType
from sqlalchemy import MetaData
from flask import Flask
import create_from_model.api_logic_server_utils as create_utils
from api_logic_server_cli.create_from_model.model_creation_services import ModelCreationServices

log = logging.getLogger(__file__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(f'%(name)s: %(message)s')     # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = True

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)

# have to monkey patch to work with WSL as workaround for https://bugs.python.org/issue38633
import errno, shutil
orig_copyxattr = shutil._copyxattr


def patched_copyxattr(src, dst, *, follow_symlinks=True):
    try:
        orig_copyxattr(src, dst, follow_symlinks=follow_symlinks)
    except OSError as ex:
        if ex.errno != errno.EACCES: raise


shutil._copyxattr = patched_copyxattr


class FabCreator(object):
    """
    Iterate over model

    Create ui/basic_web_app/views.py and api/expose_api_models.py
    """

    result_views = ""

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
                 mod_gen: ModelCreationServices,
                 host: str = "localhost",
                 port: str = "5656",
                 not_exposed: str = 'ProductDetails_V',
                 favorite_names: str = "name description",
                 non_favorite_names: str = "id"):
        self.mod_gen = mod_gen
        self.host = host
        self.port = port
        self.not_exposed = not_exposed
        self.favorite_names = favorite_names
        self.non_favorite_name = non_favorite_names

        # TODO REMOVE self.table_to_class_map = {}
        """ keys are table[.column], values are class / attribute """
        self.metadata = None
        self.engine = None
        self.session = None
        self.connection = None
        self.app = None

        self._non_favorite_names_list = self.non_favorite_names.split()
        self._favorite_names_list = self.favorite_names.split()

    def generate_ui_views(self, version="TBD"):
        """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

        cwd = os.getcwd()
        self.result_views += '"""'
        self.result_views += ("\nApiLogicServer Generate From Model " + version + "\n\n"
                              # + "From: " + sys.argv[0] + "\n\n"
                              + "Using Python: " + sys.version + "\n\n"
                              + "Favorites: "
                              + str(self._favorite_names_list) + "\n\n"
                              + "Non Favorites: "
                              + str(self._non_favorite_names_list) + "\n\n"
                              + "At: " + str(datetime.datetime.now()) + "\n\n")
        port_replace = self.port if self.port else "None"

        sys.path.append(cwd)  # for banking Command Line test

        self.result_views += '"""\n\n'
        self.mod_gen.find_meta_data(cwd)  # sets self.metadata
        meta_tables = self.mod_gen.metadata.tables
        self.result_views += self.generate_module_imports()
        for each_table in meta_tables.items():
            each_result = self.process_each_table(each_table[1])
            self.result_views += each_result
        self.result_views += self.process_module_end(meta_tables)
        return

    def zz_add_table_to_class_map(self, orm_class):
        """ given class, find table (hide your eyes), add table/class to table_to_class_map """
        orm_class_info = orm_class[1]
        query = str(orm_class_info.query)[7:]
        table_name = query.split('.')[0]
        table_name = table_name.strip('\"')
        self.mod_gen.table_to_class_map.update({table_name: orm_class[0]})
        pass  # for debug

    def zz_get_class_for_table(self, table_name) -> str:
        """ given table_name, return its class_name from table_to_class_map """
        if table_name in self.mod_gen.table_to_class_map:
            return self.mod_gen.table_to_class_map[table_name]
        else:
            log.debug("skipping view: " + table_name)
            return None

    @staticmethod
    def generate_module_imports() -> str:
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

    def related_views(self, a_table_def: MetaDataTable) -> str:
        """
            Generates statements like
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
        child_list = self.mod_gen.find_child_list(a_table_def)
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
                class_name = self.mod_gen.get_class_for_table(each_child.fullname)  # todo why using class name?
                if class_name is None:
                    print(f'.. .. .. Warning - Skipping {self.mod_gen.model_name(each_child)}->'
                          f'{each_child.fullname} - no database/models.py class')
                    related_count -= 1
                else:
                    each_entry = class_name + self.mod_gen.model_name(each_child)
                    result += each_entry
        omitted = "  # omitted mutually referring relationships: " + self_relns if self_relns != "" else ""
        result += "]" + omitted + "\n"
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
            class_name = self.mod_gen.get_class_for_table(table_name)
            if class_name is None:
                return "# skip view: " + table_name
            self.tables_visited.add(table_name)
            child_list = self.mod_gen.find_child_list(a_table_def)
            for each_child in child_list:  # recurse to ensure children first
                log.debug(".. but children first: " + each_child.name)
                result += self.process_each_table(each_child)
                self.tables_visited.add(each_child.name)

            self.tables_generated.add(a_table_def.fullname)

            self.num_pages_generated += 1

            model_name = self.mod_gen.model_name(class_name)
            view_class_name = class_name + model_name
            result += "\n\n\nclass " + view_class_name + "(" + model_name + "):\n"
            result += (
                self._indent + "datamodel = SQLAInterface(" +
                class_name + ")\n"
            )
            result += self._indent + self.mod_gen.list_columns(a_table_def)
            result += self._indent + self.mod_gen.show_columns(a_table_def)
            result += self._indent + self.mod_gen.edit_columns(a_table_def)
            result += self._indent + self.mod_gen.add_columns(a_table_def)
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
            print(".. .. ..WARNING - no relationships detected - add them to your database or model")
            print(".. .. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design")
        return result

    def create_basic_web_app_directory(self, msg):
        project_abs_path = abspath(self.mod_gen.project_directory)
        fab_project = project_abs_path + "/ui/basic_web_app"
        use_fab_based_creation = False
        if use_fab_based_creation:
            cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
            result = create_utils.run_command(cmd, msg=msg)
        else:  # use local copy
            code_loc = self.mod_gen.api_logic_server_dir
            if "\\" in code_loc:
                from_dir = code_loc + "\\create_from_model\\templates\\basic_web_app"
            else:
                from_dir = code_loc + "/create_from_model/templates/basic_web_app"
            print(f'{msg} - copy {from_dir} -> {fab_project}')
            shutil.copytree(from_dir, fab_project)
            # self.mod_gen.recursive_overwrite(from_dir, fab_project)

        pass

    def fix_basic_web_app_run__python_path(self):
        """ overwrite ui/basic_web_app/run.py (enables run.py) with logic_bank_utils call to fixup python path """
        project_ui_basic_web_app_run_file = open(self.mod_gen.project_directory + '/ui/basic_web_app/run.py', 'w')
        ui_basic_web_app_run_file = open(os.path.dirname(os.path.realpath(__file__)) + "/ui_basic_web_app_run.py")
        ui_basic_web_app_run = ui_basic_web_app_run_file.read()  # standard content
        project_ui_basic_web_app_run_file.write(ui_basic_web_app_run)
        project_ui_basic_web_app_run_file.close()

        proj = os.path.basename(self.mod_gen.project_directory)
        create_utils.replace_string_in_file(search_for="api_logic_server_project_directory",
                                   replace_with=proj,
                                   in_file=f'{self.mod_gen.project_directory}/ui/basic_web_app/run.py')
        default_host = "localhost"  # docker uses 0.0.0.0, local install uses localhost
        if os.path.exists('/home/api_logic_server'):  # docker?
            default_host = "0.0.0.0"
        create_utils.replace_string_in_file(search_for="api_logic_server_default_host",
                                   replace_with=default_host,
                                   in_file=f'{self.mod_gen.project_directory}/ui/basic_web_app/run.py')

    def fix_basic_web_app_run__create_admin(self):
        """ update create_admin.sh with project_directory """

        unix_project_name = self.mod_gen.project_directory.replace('\\', "/")  # file to update
        copy_to_unix_project_name = unix_project_name
        if self.mod_gen.copy_to_project_directory != "":
            copy_to_unix_project_name = self.mod_gen.copy_to_project_directory.replace('\\', "/")
        if self.mod_gen.command == "create-ui" or self.mod_gen.command.startswith("rebuild"):
            pass
        else:
            target_create_admin_sh_file = open(f'{unix_project_name}/ui/basic_web_app/create_admin.sh', 'x')
            source_create_admin_sh_file = open(os.path.dirname(os.path.realpath(__file__)) + "/templates/create_admin.sh")
            create_admin_commands = source_create_admin_sh_file.read()
            target_create_admin_sh_file.write(create_admin_commands)
            target_create_admin_sh_file.close()

        create_utils.replace_string_in_file(search_for="/Users/val/dev/servers/classicmodels/",
                                   replace_with=copy_to_unix_project_name,
                                   in_file=f'{unix_project_name}/ui/basic_web_app/create_admin.sh')

    def fix_basic_web_app_app_init__inject_logic(self):
        """ insert call LogicBank.activate into ui/basic_web_app/app/__init__.py """
        file_name = f'{self.mod_gen.project_directory}/ui/basic_web_app/app/__init__.py'
        proj = os.path.basename(self.mod_gen.project_directory)  # enable flask run

        insert_text = ("\n# ApiLogicServer - enable flask fab create-admin\n"
                       "\nimport database.models as models\n"
                       + "from logic import declare_logic\n"
                       + "from logic_bank.logic_bank import LogicBank\n"
                       )
        if self.mod_gen.nw_db_status.startswith("nw"):  # admin pre-installed for nw, no need to disable logic
            insert_text += "LogicBank.activate(session=db.session, activator=declare_logic)\n\n"
        else:  # logic interferes with create-admin - disable it
            insert_text += "# *** Enable the following after creating Flask AppBuilder Admin ***\n"
            insert_text += "# LogicBank.activate(session=db.session, activator=declare_logic)\n\n"
        create_utils.insert_lines_at(lines=insert_text,
                                     at="appbuilder = AppBuilder(app, db.session)",
                                     file_name=file_name)

    def fix_config(self):
        """ add abs_db_url to config

        constant for sqlite, per copy db to <project>/database
        """

        config_file_name = f'{self.mod_gen.project_directory}/ui/basic_web_app/config.py'
        create_utils.replace_string_in_file(search_for='"sqlite:///" + os.path.join(basedir, "app.db")',
                                            replace_with='"' + self.mod_gen.abs_db_url + '"',
                                            in_file=config_file_name)
        if "sqlite" in self.mod_gen.abs_db_url:
            fab_config_file_name = os.path.dirname(os.path.realpath(__file__)) + "/templates/fab_config.py"
            with open(fab_config_file_name, 'r') as file:
                fab_config = file.read()
            create_utils.insert_lines_at(lines=fab_config,
                                          at="postgresql://root:password@localhost/myapp",
                                          file_name=config_file_name)
        pass


    def prepare_flask_app_builder(self, msg: str):
        """ 8. Writing: /ui/basic_web_app/app/views.py """
        # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/val/dev/servers/api_logic_server/database/db.sqlite"
        print(msg)  # 8. Writing: /ui/basic_web_app/app/views.py
        text_file = open(self.mod_gen.project_directory + '/ui/basic_web_app/app/views.py', 'w')
        text_file.write(self.result_views)
        text_file.close()
        if self.mod_gen.command.startswith("rebuild"):
            print(".. .. ..Use existing run.py and app/init for Python path, logic")
        else:
            print(".. .. ..Fixing run.py and app/init for Python path, logic")
        if not self.mod_gen.db_url.endswith("nw.sqlite"):
            print(".. .. ..Important: you will need to run flask fab create-admin")
        self.fix_basic_web_app_run__python_path()
        self.fix_basic_web_app_run__create_admin()
        self.fix_basic_web_app_app_init__inject_logic()
        self.fix_config()

    def create_basic_web_app(self):
        if self.mod_gen.command == "create-ui" or self.mod_gen.command.startswith("rebuild"):
            print(".. .. ..Use existing ui/basic_web_app")
        else:
            self.create_basic_web_app_directory(".. .. ..Create ui/basic_web_app")
        self.generate_ui_views()
        self.prepare_flask_app_builder(msg=".. .. ..Writing: /ui/basic_web_app/app/views.py")
        log.debug(f'create_from_model.fab_creator("{self.mod_gen.db_url}", "{self.mod_gen.project_directory}" Completed')


def create(model_creation_services: ModelCreationServices):
    """ called by ApiLogicServer CLI -- creates basic web app (Flask AppBuilder)
    """
    # create_basic_web_app(db_url, project_directory, ".. ..Create ui/basic_web_app")
    fab_creator = FabCreator(model_creation_services,
                             host=model_creation_services.host, port=model_creation_services.port,
                             not_exposed=model_creation_services.not_exposed + " ",
                             favorite_names=model_creation_services.favorite_names,
                             non_favorite_names=model_creation_services.non_favorite_names)
    fab_creator.create_basic_web_app()
