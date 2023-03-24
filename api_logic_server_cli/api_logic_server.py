# -*- coding: utf-8 -*-

'''
ApiLogicServer CLI: given a database url, create [and run] customizable ApiLogicProject.
    * Basically clones prototype project, and creates:
        * database/models.py for SQLAlchemy, using modified sqlacodegen & safrs metadata
        * ui/admin/admin.yaml for the Admin App     - using introspected models.py
        * api/expose_api_models.py for a safrs api  - using introspected models.py
    * Special provisions for NW Sample, to show customizations.
    * See end for key module map quick links...

Called from api_logic_server_cli.py, by instantiating the ProjectRun object.
'''

__version__ = "08.01.15"
recent_changes = \
    f'\n\nRecent Changes:\n' +\
    "\t03/23/2023 - 08.01.15: cloud debug additions, issue 59, 62-4, table filters \n"\
    "\t03/05/2023 - 08.01.04: python 3.11.2, Werkzeug==2.2.3, mypy initial, logicbank 1.8.3 \n"\
    "\t02/15/2023 - 08.00.01: Declarative Authorization and Authentication, Werkzeug==2.2.3 \n"\
    "\t01/10/2023 - 07.00.04: Portable projects, server_proxy  \n"\
    "\t01/06/2023 - 07.00.00: Multi-db, sqlite test dbs, tests run, security prototype, env config  \n"\
    "\t12/21/2022 - 06.05.00: Devops, env db uri, api endpoint names, git-push-new-project  \n"\
    "\t12/08/2022 - 06.04.05: Clarify creating docker repo, IP info, logic comments, nested result example \n"\
    "\t11/22/2022 - 06.03.06: Image, Chkbox, Dialects, run.sh, SQL/Server url change, stop endpoint, Chinook Sqlite \n"\
    "\t10/02/2022 - 06.02.00: Option infer_primary_key, Oct1 SRA (issue 49), cleanup db/api setup, += postgres dvr \n"\
    "\t09/15/2022 - 06.01.00: Multi-app Projects \n"\
    "\t08/28/2022 - 06.00.01: Admin App show_when & cascade add. Simplify Codespaces swagger url & use default config \n"\
    "\t06/12/2022 - 05.02.22: No pyodbc by default, model customizations simplified, better logging \n"\
    "\t05/04/2022 - 05.02.03: alembic for database migrations, admin-merge.yaml \n"\
    "\t04/27/2022 - 05.01.02: copy_children, with support for nesting (children and grandchildren, etc.) \n"\
    "\t03/27/2022 - 05.00.06: Introducing Behave test framework, LogicBank bugfix \n"\
    "\t12/26/2021 - 04.00.05: Introducing the admin app, with Readme Tutorial \n"\
    "\t11/13/2021 - 03.50.01: rebuild-from-database/model, improved relationship support, port conflict msg \n"\
    "\t09/15/2021 - 03.00.09: auto-create .devcontainer for vscode, configure network, python & debug \n"\

from contextlib import closing

import yaml

temp_created_project = "temp_created_project"   # see copy_if_mounted

import socket
import subprocess
from os.path import abspath
from os.path import realpath
from pathlib import Path
from shutil import copyfile
import shutil
import importlib.util
from flask import Flask
import logging, logging.config
import datetime
from typing import NewType
import sys
import os
import importlib


def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    assert path_result == env_result
    return path_result


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    return str(python_path)

current_path = os.path.abspath(os.path.dirname(__file__))
with open(f'{get_api_logic_server_dir()}/logging.yml','rt') as f:
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)
log=logging.getLogger(__name__)
debug_value = os.getenv('APILOGICSERVER_DEBUG')
if debug_value is not None:
    debug_value = debug_value.upper()
    if debug_value.startswith("F") or debug_value.startswith("N"):
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.DEBUG)

# log.debug("sys.path.append(get_api_logic_server_dir())\n",get_api_logic_server_dir())
sys.path.append(get_api_logic_server_dir())  # e.g, on Docker: export PATH="/home/api_logic_server/api_logic_server_cli"
api_logic_server_path = os.path.dirname(get_api_logic_server_dir())  # e.g: export PATH="/home/api_logic_server"
sys.path.append(api_logic_server_path)
from create_from_model.model_creation_services import ModelCreationServices

import sqlacodegen_wrapper.sqlacodegen_wrapper as expose_existing_callable
import create_from_model.api_logic_server_utils as create_utils
import api_logic_server_cli.create_from_model.uri_info as uri_info
from api_logic_server_cli.cli_args_project import Project

api_logic_server_info_file_name = get_api_logic_server_dir() + "/api_logic_server_info.yaml"

api_logic_server_info_file_dict = {}  # last-run (debug, etc) info
""" contains last-run info, debug switches to show args, etc """

if Path(api_logic_server_info_file_name).is_file():
    api_logic_server_info_file = open(api_logic_server_info_file_name)
    api_logic_server_info_file_dict = yaml.load(api_logic_server_info_file, Loader=yaml.FullLoader)
    api_logic_server_info_file.close()


last_created_project_name = api_logic_server_info_file_dict.get("last_created_project_name","")
default_db = "default = nw.sqlite, ? for help"
default_project_name = "ApiLogicProject"
os_cwd = os.getcwd()
default_bind_key_url_separator = "-"  # admin app fails with "/" or ":" (json issues?)

if is_docker():
    default_project_name = "/localhost/ApiLogicProject"

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)

def create_app(config_filename=None, host="localhost"):
    import safrs

    app = Flask("API Logic Server")
    import api_logic_server_cli.config as app_logic_server_config
    app.config.from_object(app_logic_server_config.Config)
    db = safrs.DB
    db.init_app(app)
    return app


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
        if msg != "":
            log.debug(f'{msg} Delete dir: {dir_path}')
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
                    log.debug("Error: %s : %s" % (dir_path, e.strerror))
    else:
        # https://stackoverflow.com/questions/22948189/how-to-solve-the-directory-is-not-empty-error-when-running-rmdir-command-in-a
        try:
            remove_project = create_utils.run_command(f'del /f /s /q {dir_path} 1>nul')
        except:
            pass
        try:
            remove_project = create_utils.run_command(f'rmdir /s /q {dir_path}')  # no prompt, no complaints if non-exists
        except:
            pass


def recursive_overwrite(src, dest, ignore=None):
    """
    copyTree, with overwrite
    thanks: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
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
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)


def create_nw_tutorial(project_name, api_logic_server_dir_str):
    """ copy tutorial from docs, and link to it from readme.md 
    
    alert 2 copies
    * /Users/val/dev/Org-ApiLogicServer/Docs/docs/Tutorial.md
    * /Users/val/dev/ApiLogicServer/Docs/api_logic_server_cli/docs/Tutorial.md <=
    """


    tutorial_file_proj = open(project_name + '/Tutorial.md', 'w')
    tutorial_file_docs_path = Path(api_logic_server_dir_str).\
        joinpath('docs/Tutorial.md')
    tutorial_file_docs = open(tutorial_file_docs_path)
    tutorial_readme = tutorial_file_docs.read()
    tutorial_file_proj.write(tutorial_readme)
    tutorial_file_proj.close()

    project_readme_file_path = project_name + '/readme.md'  # brief 'go read tutorial' - add std readme
    standard_readme_file_path = str(Path(api_logic_server_dir_str).\
        joinpath('project_prototype').joinpath("readme.md"))
    with open(project_readme_file_path, 'a') as project_readme_file:
        with open(standard_readme_file_path) as standard_readme_file:
            project_readme_file.write(standard_readme_file.read())


def create_project_with_nw_samples(project, msg: str) -> str:
    """
    clone prototype to  project directory, copy sqlite db, and remove git folder

    update config.py - SQLALCHEMY_DATABASE_URI

    if nw/nw+, inject sample logic/declare_logic and api/customize_api.

    :param project a ProjectRun
    :param msg log.debuged, such as Create Project:
    :return: return_abs_db_url (e.g., reflects sqlite copy to project/database dir)
    """

    import tempfile
    cloned_from = project.from_git
    tmpdirname = ""
    with tempfile.TemporaryDirectory() as tmpdirname:

        if project.merge_into_prototype:
            pass
        else:
            remove_project_debug = True
            if remove_project_debug and project.project_name != ".":
                delete_dir(realpath(project.project_directory), "1.")

        from_dir = project.from_git
        api_logic_server_dir_str = str(get_api_logic_server_dir())  # fixme not req'd
        if project.from_git.startswith("https://"):
            cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project.project_directory
            cmd = f'git clone --quiet {project.from_gitfrom_git} {project.project_directory}'
            result = create_utils.run_command(cmd, msg=msg)  # "2. Create Project")
            delete_dir(f'{project.project_directory}/.git', "3.")
        else:
            if from_dir == "":
                from_dir = (Path(api_logic_server_dir_str)).\
                    joinpath('project_prototype')  # /Users/val/dev/ApiLogicServer/project_prototype
            log.debug(f'{msg} {os.path.realpath(project.project_directory)}')
            log.debug(f'.. ..Clone from {from_dir} ')
            cloned_from = from_dir
            try:
                if project.merge_into_prototype:  # create project over current (e.g., docker, learning center)
                    # tmpdirname = tempfile.TemporaryDirectory() # preserve files like Tech_Bits.md
                    recursive_overwrite(project.project_directory, str(tmpdirname))  # save, restore @ end
                    delete_dir(str(Path(str(tmpdirname)) / ".devcontainer"), "")     # except, do NOT restore these
                    delete_dir(str(Path(str(tmpdirname)) / "api"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "database"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "logic"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "security"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "test"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "ui"), "")
                    if os.path.exists(str(Path(str(tmpdirname))  / "api_logic_server_run.py" )):
                        os.remove(str(Path(str(tmpdirname)) / "api_logic_server_run.py"))
                    delete_dir(realpath(project.project_directory), "")
                    recursive_overwrite(from_dir, project.project_directory)  # ApiLogic Proto -> current (new) project
                else:
                    shutil.copytree(from_dir, project.project_directory)  # normal path (fails if project_directory not empty)
            except OSError as e:
                raise Exception(f'\n==>Error - unable to copy to {project.project_directory} -- see log below'
                    f'\n\n{str(e)}\n\n'
                    f'Suggestions:\n'
                    f'.. Verify the --project_name argument\n'
                    f'.. If you are using Docker, verify the -v argument\n\n')
        if project.nw_db_status in ["nw", "nw+"]:
            log.debug(".. ..Copy in nw customizations: logic, custom api, readme, tests, admin app")
            nw_dir = (Path(api_logic_server_dir_str)).\
                joinpath('project_prototype_nw')  # /Users/val/dev/ApiLogicServer/api_logic_server_cli/project_prototype
            recursive_overwrite(nw_dir, project.project_directory)

            create_nw_tutorial(project.project_directory, api_logic_server_dir_str)

        if project.nw_db_status in ["nw-"]:
            log.debug(".. ..Copy in nw- customizations: readme, perform_customizations")
            nw_dir = (Path(api_logic_server_dir_str)).\
                joinpath('project_prototype_nw_no_cust')  # /Users/val/dev/ApiLogicServer/project_prototype_nw_no_cust
            recursive_overwrite(nw_dir, project.project_directory)

        create_utils.replace_string_in_file(search_for="creation-date",
                            replace_with=str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                            in_file=f'{project.project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_version",
                            replace_with=__version__,
                            in_file=f'{project.project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_template",
                            replace_with=f'{from_dir}',
                            in_file=f'{project.project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_project_directory",
                            replace_with=f'{project.project_directory}',
                            in_file=f'{project.project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_api_name",
                            replace_with=f'{project.api_name}',
                            in_file=f'{project.project_directory}/readme.md')

        do_fix_docker_for_vscode_dockerfile = True
        """
        if do_fix_docker_for_vscode_dockerfile:
            if arch.get_platform():
                create_utils.replace_string_in_file(search_for="apilogicserver/api_logic_server",
                                    replace_with=f'apilogicserver/arm-slim',
                                    in_file=f'{project_directory}/For_VSCode.dockerfile')
        """

        return_abs_db_url = project.abs_db_url
        copy_sqlite = True
        if copy_sqlite == False or "sqlite" not in project.abs_db_url:
            db_uri = get_windows_path_with_slashes(project.abs_db_url)
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=db_uri,
                                in_file=f'{project.project_directory}/config.py')
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=db_uri,
                                in_file=f'{project.project_directory}/database/alembic.ini')
        else:
            """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
            """
            # strip sqlite://// from sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/database/nw-gold.sqlite
            db_loc = project.abs_db_url.replace("sqlite:///", "")
            target_db_loc_actual = str(project.project_directory_path.joinpath('database/db.sqlite'))
            copyfile(db_loc, target_db_loc_actual)
            config_url = str(project.api_logic_server_dir_path)
            # build this:  SQLALCHEMY_DATABASE_URI = sqlite:///{str(project_abs_dir.joinpath('database/db.sqlite'))}
            # into  this:  SQLALCHEMY_DATABASE_URI = f"replace_db_url"
            replace_db_url_value = "sqlite:///{str(project_abs_dir.joinpath('database/db.sqlite'))}"

            if os.name == "nt":  # windows
                target_db_loc_actual = get_windows_path_with_slashes(target_db_loc_actual)
            # set this in config.py: SQLALCHEMY_DATABASE_URI = "replace_db_url"
            return_abs_db_url = f'sqlite:///{target_db_loc_actual}'
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=replace_db_url_value,
                                in_file=f'{project.project_directory}/config.py')
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=return_abs_db_url,
                                in_file=f'{project.project_directory}/database/alembic.ini')

            log.debug(f'.. ..Sqlite database setup {target_db_loc_actual}...')
            log.debug(f'.. .. ..From {db_loc}')
            log.debug(f'.. .. ..db_uri set to: {return_abs_db_url} in <project>/config.py')
        if project.merge_into_prototype:
            recursive_overwrite(str(tmpdirname), project.project_directory)
            # delete_dir(realpath(Path(str(tmpdirname))), "")
            # os.removedirs(Path(str(tmpdirname)))
            # tmpdirname.cleanup()
    return return_abs_db_url


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


def fix_database_models(project_directory: str, db_types: str, nw_db_status: str):
    """ injecting <db_types file> into database/models.py, fix nw cascade delete """
    models_file_name = f'{project_directory}/database/models.py'
    if db_types is not None and db_types != "":
        log.debug(f'.. .. ..Injecting file {db_types} into database/models.py')
        with open(db_types, 'r') as file:
            db_types_data = file.read()
        create_utils.insert_lines_at(lines=db_types_data,
                                    at="(typically via --db_types)",
                                    file_name=models_file_name)
    if nw_db_status in ["nw", "nw+", "nw-"]:
        log.debug(f'.. .. ..Setting cascade delete for sample database database/models.py')
        create_utils.replace_string_in_file(in_file=models_file_name,
            search_for="OrderDetailList = relationship('OrderDetail', cascade_backrefs=True, backref='Order')",
            replace_with="OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=True, backref='Order')  # manual fix")


def final_project_fixup(msg, project) -> str:
    """ fix ports/hosts, inject project names/dates, update info file """
    log.debug(msg)  # "7. Final project fixup"

    if False and project.use_model == "" and project.command != "rebuild-from-model":  # TODO remove dead code
        msg = f' a.   Appending "from database import customize_models" to database/models.py'
        fix_database_models__import_customize_models(project_directory, msg)

    copy_project_result = ""
    if project.command.startswith("rebuild"):
        pass
    else:
        log.debug(f' b.   Update api_logic_server_run.py with '
              f'project_name={project.project_name} and api_name, host, port')
        update_api_logic_server_run(project)

        fix_host_and_ports(" c.   Fixing api/expose_services - port, host", project)

        copy_project_result = ""

        api_logic_server_info_file_dict["last_created_project_name"] = project.project_directory  # project_name - twiddle
        api_logic_server_info_file_dict["last_created_date"] = str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
        api_logic_server_info_file_dict["last_created_version"] = __version__
        with open(api_logic_server_info_file_name, 'w') as api_logic_server_info_file_file:
            yaml.dump(api_logic_server_info_file_dict, api_logic_server_info_file_file, default_flow_style=False)
    return copy_project_result


def fix_database_models__import_customize_models(project_directory: str, msg: str):
    """ Append "from database import customize_models" to database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    log.debug(msg)
    models_file = open(models_file_name, 'a')
    models_file.write("\n\nfrom database import customize_models\n")
    models_file.close()


def update_api_logic_server_run(project):
    """
    Updates project_name, ApiLogicServer hello, project_dir in api_logic_server_run_py

    Note project_directory is from user, and may be relative (and same as project_name)
    """
    api_logic_server_run_py = f'{project.project_directory}/api_logic_server_run.py'
    create_utils.replace_string_in_file(search_for="\"api_logic_server_project_name\"",  # fix logic_bank_utils.add_python_path
                           replace_with='"' + os.path.basename(project.project_name) + '"',
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="ApiLogicServer hello",
                           replace_with="ApiLogicServer generated at:" +
                                        str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                           in_file=api_logic_server_run_py)
    project_directory_fix = project.project_directory_actual
    if os.name == "nt":  # windows
        project_directory_fix = get_windows_path_with_slashes(str(project.project_directory_actual))
    create_utils.replace_string_in_file(search_for="\"api_logic_server_project_dir\"",  # for logging project location
                           replace_with='"' + project_directory_fix + '"',
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_api_name",  # last node of server url
                           replace_with=project.api_name,
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_host",
                           replace_with=project.host,
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_swagger_host",
                           replace_with=project.swagger_host,
                           in_file=api_logic_server_run_py)
    replace_port = f', port="{project.port}"' if project.port else ""  # TODO: consider reverse proxy

    create_utils.replace_string_in_file(search_for="api_logic_server_version",
                           replace_with=__version__,
                           in_file=api_logic_server_run_py)

    create_utils.replace_string_in_file(search_for="api_logic_server_created_on",
                           replace_with=str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                           in_file=api_logic_server_run_py)

    create_utils.replace_string_in_file(search_for="api_logic_server_port",   # server port
                           replace_with=project.port,
                           in_file=api_logic_server_run_py)
    pass


def fix_host_and_ports(msg, project):
    """ c.   Fixing api/expose_services - port, host """
    log.debug(msg)  # c.   Fixing api/expose_services - port, host
    replace_port = f':{project.port}' if project.port else ""
    # replace_with = host + replace_port
    in_file = f'{project.project_directory}/api/customize_api.py'
    create_utils.replace_string_in_file(search_for="api_logic_server_host",
                           replace_with=project.host,
                           in_file=in_file)
    create_utils.replace_string_in_file(search_for="api_logic_server_port",
                           replace_with=replace_port,
                           in_file=in_file)
    log.debug(f' d.   Updated customize_api_py with port={project.port} and host={project.host}')
    full_path = project.project_directory_actual
    create_utils.replace_string_in_file(search_for="python_anywhere_path",
                           replace_with=full_path,
                           in_file=f'{project.project_directory}/python_anywhere_wsgi.py')
    log.debug(f' e.   Updated python_anywhere_wsgi.py with {full_path}')


def start_open_with(open_with: str, project_name: str):
    """ Creation complete.  Opening {open_with} at {project_name} """
    log.debug(f'\nCreation complete - Opening {open_with} at {project_name}')
    log.debug(".. See the readme for install / run instructions")
    create_utils.run_command(f'{open_with} {project_name}', None, "no-msg")


def invoke_extended_builder(builder_path, db_url, project_directory):
    # spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
    spec = importlib.util.spec_from_file_location("module.name", builder_path)
    extended_builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extended_builder)  # runs "bare" module code (e.g., initialization)
    extended_builder.extended_builder(db_url, project_directory)  # extended_builder.MyClass()


def invoke_creators(model_creation_services: ModelCreationServices):
    """ MAJOR: uses model_creation_services (resource_list, model iterator functions) to create api, apps
    """

    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')

    log.debug(" b.  Create api/expose_api_models.py from models")
    # log.debug(f'---> cwd: {model_creation_services.os_cwd}')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/api_expose_api_models_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)  # runs "bare" module code (e.g., initialization)
    creator.create(model_creation_services)  # invoke create function

    if model_creation_services.project.admin_app:
        log.debug(" c.  Create ui/admin/admin.yaml from models")
        spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/ui_admin_creator.py')
        creator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(creator)
        creator.create(model_creation_services)
    else:
        pass
        # log.debug(".. .. ..ui/admin_app creation declined")

    # model_creation_services.close_app()  # this may no longer be required


class ProjectRun(Project):
    """ Main Class - instantiate / create_project to run CLI functions """
    def __init__(self, command: str, project_name: str, 
                     db_url: str,
                     api_name: str="api",
                     host: str='localhost', 
                     port: str='5656', 
                     swagger_host: str="localhost", 
                     not_exposed: str="ProductDetails_V",
                     from_git: str="", 
                     db_types: str=None, 
                     open_with: str="", 
                     run: bool=False, 
                     use_model: str="", 
                     admin_app: bool=True,
                     flask_appbuilder: bool=False, 
                     favorites: str="name description", 
                     non_favorites: str="id", 
                     react_admin: bool=True,
                     extended_builder: str="", 
                     include_tables: str="",
                     multi_api: bool=False, 
                     infer_primary_key: bool=False, 
                     bind_key_url_separator: str=default_bind_key_url_separator,
                     bind_key: str="",
                     execute: bool=True):
        super(ProjectRun, self).__init__()
        self.project_name = project_name
        self.db_url = db_url
        self.bind_key = bind_key
        self.api_name = api_name
        self.host = host
        self.port = port
        self.swagger_host = swagger_host
        self.not_exposed = not_exposed
        self.from_git = from_git
        self.db_types = db_types
        self.open_with = open_with
        self.run = run
        self.use_model = use_model
        self.admin_app = admin_app
        self.flask_appbuilder = flask_appbuilder
        self.favorites = favorites
        self.non_favorites = non_favorites
        self.react_admin = react_admin
        self.extended_builder = extended_builder
        self.include_tables = include_tables
        self.multi_api = multi_api
        self.infer_primary_key = infer_primary_key
        self.bind_key_url_separator = bind_key_url_separator
        self.command = command

        if execute:
            self.create_project()


    def print_options(self):
        """ Creating ApiLogicProject with options: (or uri helo) """
        if self.db_url == "?":
            uri_info.print_uri_info()
            exit(0)

        print_options = True
        if print_options:
            creating_or_updating = "Creating"
            if self.command.startswith("add_"):
                creating_or_updating = "Updating"
            log.debug(f'\n\n{creating_or_updating} ApiLogicProject with options:')
            log.debug(f'  --db_url={self.db_url}')
            log.debug(f'  --bind_key={self.bind_key}')
            log.debug(f'  --project_name={self.project_name}   (pwd: {self.os_cwd})')
            log.debug(f'  --api_name={self.api_name}')
            log.debug(f'  --admin_app={self.admin_app}')
            log.debug(f'  --react_admin={self.react_admin}')
            log.debug(f'  --flask_appbuilder={self.flask_appbuilder}')
            log.debug(f'  --from_git={self.from_git}')
            #        log.debug(f'  --db_types={self.db_types}')
            log.debug(f'  --run={self.run}')
            log.debug(f'  --host={self.host}')
            log.debug(f'  --port={self.port}')
            log.debug(f'  --swagger_host={self.swagger_host}')
            log.debug(f'  --not_exposed={self.not_exposed}')
            log.debug(f'  --open_with={self.open_with}')
            log.debug(f'  --use_model={self.use_model}')
            log.debug(f'  --favorites={self.favorites}')
            log.debug(f'  --non_favorites={self.non_favorites}')
            log.debug(f'  --extended_builder={self.extended_builder}')
            log.debug(f'  --include_tables={self.include_tables}')
            log.debug(f'  --multi_api={self.multi_api}')
            log.debug(f'  --infer_primary_key={self.infer_primary_key}')

    def update_config_and_copy_sqlite_db(self, msg: str) -> str:
        """

        1. If sqlite, copy db to database folder

        2. Add project.db_url to config 

        3. Update database/bind_databases.py

        Parameters:

        :arg: msg log.debug this, e.g., ".. ..Adding Database [{self.bind_key}] to existing project"
        :arg: project project setting object
        """
        log.debug(msg)
        bind_key_upper = self.bind_key.upper()  # configs insist on all caps
        return_abs_db_url = self.abs_db_url
        config_uri_value = "'" + return_abs_db_url + "'"


        """ **********************
        sqlite? copy to database/
        **************************  """
        if "sqlite" in self.abs_db_url:
            """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
            """
            log.debug(f'.. .. ..Copying sqlite database to: database/{self.bind_key}_db.sqlite')
            db_loc = self.abs_db_url.replace("sqlite:///", "")
            target_db_loc_actual = str(self.project_directory_path.joinpath(f'database/{self.bind_key}_db.sqlite'))
            copyfile(db_loc, target_db_loc_actual)

            if os.name == "nt":  # windows
                # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
                target_db_loc_actual = get_windows_path_with_slashes(target_db_loc_actual)
            return_abs_db_url = f'sqlite:///{target_db_loc_actual}'
            # build this:  SQLALCHEMY_DATABASE_URI_AUTHENTICATION = f'sqlite:///{str(project_abs_dir.joinpath("database/authentication_db.sqlite"))}'
            # into  this:  {CONFIG_URI} = '{config_uri_value}'
            file_name = f'"database/{self.bind_key}_db.sqlite"'
            config_uri_value = "f'sqlite:///{str(project_abs_dir.joinpath(" + file_name + "))}'"
            log.debug(f'.. .. ..From {db_loc}')


        """ **********************
        add url to config
        **************************  """
        # db_uri = config_uri  # return_abs_db_url
        if os.name == "nt":  # windows
            # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
            target_db_loc_actual = get_windows_path_with_slashes(target_db_loc_actual)
        CONFIG_URI = f'SQLALCHEMY_DATABASE_URI_{bind_key_upper}'

        config_insert = f"""
    {CONFIG_URI} = {config_uri_value}
    app_logger.info(f'config.py - {CONFIG_URI}: <CONFIG_URI_VALUE>\\n')

    # as desired, use env variable: export SQLALCHEMY_DATABASE_URI='sqlite:////Users/val/dev/servers/docker_api_logic_project/database/db.sqliteXX'
    if os.getenv('{CONFIG_URI}'):
        {CONFIG_URI} = os.getenv('{CONFIG_URI}')  # type: ignore # type: str
        app_logger.debug(f'.. overridden from env variable: {CONFIG_URI}')

    """
        config_insert = config_insert.replace("<CONFIG_URI_VALUE>", "{" + f'{CONFIG_URI}' + "}")
        config_file = f'{self.project_directory}/config.py'
        config_built = create_utils.does_file_contain(search_for=CONFIG_URI, in_file=config_file)
        if not config_built:
            create_utils.insert_lines_at(lines=config_insert,
                                        at="# End Multi-Database URLs (from ApiLogicServer add-db...)",
                                        file_name=f'{self.project_directory}/config.py')
            log.debug(f'.. ..Updating config.py file with {CONFIG_URI}...')
        else:
            log.debug(f'.. ..Not updating config.py file with {CONFIG_URI}... (already present)')


        """ **********************
        update bind_databases.py
        **************************  """
        # NB: must do all binds in 1 call (not 1 call / db): https://www.youtube.com/watch?v=SB5BfYYpXjE

        bind_insert_urls = """
    from api import <project.bind_key>_expose_api_models
    from database import <project.bind_key>_models

    # flask_app.config.update(SQLALCHEMY_BINDS = \\
    #     {'<project.bind_key>': flask_app.config['SQLALCHEMY_DATABASE_URI_<bind_key_upper>']})
    
    app_logger.debug(f"\\n<project.bind_key> Config complete - database/<project.bind_key>_models.py"
        + f'\\n -- with bind: <project.bind_key>'
        + f'\\n -- len(database.<project.bind_key>_models.<project.bind_key>.metadata.tables) tables loaded')
    
    <project.bind_key>_expose_api_models.expose_models(safrs_api, method_decorators= method_decorators)

    """ # not f-string since it contains {}

        flask_app_config__update = \
            f"\t\t'{self.bind_key}': flask_app.config['SQLALCHEMY_DATABASE_URI_{bind_key_upper}']\n"

        bind_insert_urls = bind_insert_urls.replace('<project.bind_key>', f'{self.bind_key}')
        bind_insert_urls = bind_insert_urls.replace('<bind_key_upper>', f'{bind_key_upper}')
        binds_databases_file = f'{self.project_directory}/database/bind_databases.py'
        binds_built = create_utils.does_file_contain( \
            search_for=bind_key_upper, in_file=binds_databases_file)
        some_configs_built = create_utils.does_file_contain( \
            search_for='flask_app.config[', in_file=binds_databases_file)
        if some_configs_built:
            flask_app_config__update = ', ' + flask_app_config__update
        if not binds_built:
            create_utils.insert_lines_at(lines=bind_insert_urls,
                                        at="# End Bind URLs",
                                        file_name=binds_databases_file)
            # 'Todo': flask_app.config['SQLALCHEMY_DATABASE_URI_TODO'],
            create_utils.insert_lines_at(lines=flask_app_config__update,
                                        at="# make multiple databases available",
                                        file_name=binds_databases_file)
            log.debug(f'.. ..Updating database/bind_databases.py with {CONFIG_URI}...')
        else:
            log.debug(f'.. ..Not updating database/bind_databases.py with {CONFIG_URI} (already present)')

        return return_abs_db_url


    def add_sqlite_security(self, msg: str, is_nw: bool = False):
        """_summary_

        1. add-db --db_url=auth

        2. add user.login endpoint

        3. Set SECURITY_ENABLED in config.py

        4. Adding Sample authorization to security/declare_security.py, or user TODO

        Args:
            msg (str): eg: ApiLogicProject customizable project created.  Adding Security:")
            is_nw (bool): is northwind, which means we add the nw security logic
        """

        log.debug("\n\n==================================================================")
        if msg != "":
            log.info(msg)
            log.info("  1. ApiLogicServer add-db --db_url=auth --bind_key=authentication")
        log.debug("==================================================================5\n")
        save_run = self.run
        save_command = self.command
        save_db_url = self.db_url
        self.command = "add_db"
        self.bind_key = "authentication"
        self.db_url = "auth"  # shorthand for api_logic_server_cli/database/auth...
        self.run = False
        self.create_project()  # not creating project, but using model creation svcs
        self.run = save_run
        self.command = save_command
        self.db_url = save_db_url
        
        log.debug("\n==================================================================")
        if msg != "":
            log.info("  2. Add User.Login endpoint")
        log.debug("==================================================================\n")
        login_endpoint_filename = f'{self.api_logic_server_dir_path.joinpath("templates/login_endpoint.txt")}'
        auth_models_file_name = f'{self.project_directory_path.joinpath("database/authentication_models.py")}'
        with open(login_endpoint_filename, 'r') as file:
            login_endpoint_data = file.read()
        create_utils.insert_lines_at(lines=login_endpoint_data, 
                    at="backref='user'", after=True,
                    file_name=auth_models_file_name)
        login_endpoint_filename = f'{self.api_logic_server_dir_path.joinpath("templates/login_endpoint_imports.txt")}'
        auth_models_file_name = f'{self.project_directory_path.joinpath("database/authentication_models.py")}'
        with open(login_endpoint_filename, 'r') as file:
            login_endpoint_data = file.read()
        create_utils.insert_lines_at(lines=login_endpoint_data, 
                    at="import declarative_base", after=True,
                    file_name=auth_models_file_name)

        log.debug("\n==================================================================")
        if msg != "":
            log.info("  3. Set SECURITY_ENABLED in config.py")
        log.debug("==================================================================\n")
        create_utils.replace_string_in_file(search_for="SECURITY_ENABLED = False  #",
                            replace_with='SECURITY_ENABLED = True  #',
                            in_file=f'{self.project_directory}/config.py')
        if is_nw:
            log.debug("\n==================================================================")
        if msg != "":
            if msg != "":
                log.info("  4. Adding Sample authorization to security/declare_security.py")
            log.debug("==================================================================\n\n")
            nw_declare_security_py_path = self.api_logic_server_dir_path.\
                joinpath('project_prototype_nw/security/declare_security.py')
            declare_security_py_path = self.project_directory_path.joinpath('security/declare_security.py')
            shutil.copyfile(nw_declare_security_py_path, declare_security_py_path)
        else:
            log.debug("\n==================================================================")
            if msg != "":
                log.info("  4. TODO: Declare authorization in security/declare_security.py")
            log.debug("==================================================================\n\n")


    def add_nw_customizations(self, do_show_messages: bool = True):
        """_summary_

        1. add-sqlite-security

        2. deep copy project_prototype_nw

        Args:
        """
        log.debug("\n\n==================================================================")
        nw_messages = ""
        if do_show_messages:
            nw_messages = "Add northwind customizations - enabling security"
        self.add_sqlite_security(is_nw=True, msg=nw_messages)

        nw_path = (self.api_logic_server_dir_path).\
            joinpath('project_prototype_nw')  # /Users/val/dev/ApiLogicServer/api_logic_server_cli/project_prototype
        recursive_overwrite(nw_path, self.project_directory)

        create_nw_tutorial(self.project_directory, str(self.api_logic_server_dir_path))

        if do_show_messages:
            log.info("\nExplore key customization files:")
            log.info(f'..api/customize_api.py')
            log.info(f'..database/customize_models.py')
            log.info(f'..logic/declare_logic.py')
            log.info(f'..security/declare_security.py\n')
            if self.is_tutorial == False:
                log.info(".. complete\n")


    def tutorial(self, msg: str="", create: str='tutorial'):
        """
        Creates (updates) Tutorial

        Contains 3 projects: basic_app, ApiLogicProject, ApiLogicProject_Logic
        
        example: 
\b    
        cd ApiLogicProject  # any empty folder, perhaps where ApiLogicServer is installed
\b
        ApiLogicServer tutorial

        - use existing for tutorial
        - if fiddle, delete top, read app_fiddle.md -> fiddle.extend(tutorial-top)

        :param create: 'fiddle' (for codespaces), or 'tutorial'
        """

        def create_readme():
            """
            Creates the readme file for either tutorial or fiddle:
            - use existing for tutorial
            - if fiddle, delete top, read app_fiddle.md -> fiddle.extend(tutorial-top)
            """

            read_me_target = target_project_path.joinpath(f'{create}/readme.md')
            if create == "app_fiddle":  # starting browser via port mappings
                fiddle_header_path = self.api_logic_server_dir_path.joinpath(f'templates/{create}.md')
                fiddle_header_file = open(fiddle_header_path, "r")
                fiddle_header_data = fiddle_header_file.read()
                fiddle_header_file.close()
                readme_file = open(read_me_target)
                readme_data = readme_file.read()
                end_of_tutorial_header = readme_data.find('<summary>1.')
                readme_fiddle_data = fiddle_header_data + readme_data[end_of_tutorial_header:]
                readme_file = open(read_me_target, "w")  # write the fiddle over the readme
                readme_file.write(readme_fiddle_data)
                readme_file.close()
                create_utils.replace_string_in_file(search_for="cd tutorial",
                        replace_with='cd /workspaces/app_fiddle',
                        in_file=read_me_target)
            else:
                create_utils.replace_string_in_file(search_for="2-apilogicproject.png",
                        replace_with='2-apilogicproject-tutorial.png',
                        in_file=read_me_target)
        

        log.info(f'\n{msg} {create}')
        target_project = self.project_name  # eg, ApiLogicServer (or, in dev, server)
        target_project_path = Path(target_project)
        self.project_directory_path = Path(self.project_name)
        self.project_directory_actual = self.project_directory_path
        # if not self.project_directory_path.exists():
        #    os.mkdir(self.project_directory_path, mode = 0o777)
        
        log.info(f"\nCreating Basic_app")
        shutil.copytree(dirs_exist_ok=True,
            src=self.api_logic_server_dir_path.joinpath('project_tutorial'),
            dst=target_project_path.joinpath(create))
        
        create_readme()

        self.command = "create"
        self.project_name = str(target_project_path.joinpath(f"{create}/2. ApiLogicProject"))
        self.db_url = "nw-"  # shorthand for sample db, no cust
        save_run = self.run
        self.run = False
        self.is_tutorial = True
        log.info(f"\nCreating ApiLogicProject")
        self.create_project()

        log.info(f"\nCreating ApiLogicProject_Logic\n")
        no_cust = self.project_name
        with_cust = str(target_project_path.joinpath(f"{create}/3. ApiLogicProject_Logic"))
        shutil.copytree(dirs_exist_ok=True,
            src=no_cust,
            dst=with_cust)
        
        self.project_name = with_cust
        self.command = "add-cust"
        self.add_nw_customizations(do_show_messages=False)
        self.run = save_run
        log.info(f"Tutorial project successfully created.  Next steps:\n")
        log.info(f'  Open the tutorial project in your VSCode\n')
        if is_docker() == False:
            log.info(f'  Establish your Python environment - see https://apilogicserver.github.io/Docs/Project-Env/')
            docker_info = """
        cd tutorial
        python3 -m venv venv       # may require python -m venv venv
        source venv/bin/activate   # windows venv\Scripts\\activate
        python3 -m pip install -r requirements.txt"""
            log.info(f'{docker_info}\n')


    def create_project(self):
        """
        Creates logic-enabled Python safrs api/admin project, options for execution

        main driver

        :returns: none
        """

        # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
        self.print_options()

        log.debug(f"\nApiLogicServer {__version__} Creation Log:")

        self.abs_db_url, self.nw_db_status, self.model_file_name = create_utils.get_abs_db_url("0. Using Sample DB", self)

        if self.extended_builder == "*":
            self.extended_builder = abspath(f'{self.api_logic_server_dir_path}/extended_builder.py')
            log.debug(f'0. Using default extended_builder: {self.extended_builder}')

        self.project_directory, self.api_name, self.merge_into_prototype = \
            create_utils.get_project_directory_and_api_name(self)
        self.project_directory_actual = os.path.abspath(self.project_directory)  # make path absolute, not relative (no /../)
        self.project_directory_path = Path(self.project_directory_actual)

        if self.command.startswith("rebuild") or self.command == "add_db":
            log.debug("1. Not Deleting Existing Project")
            log.debug("2. Using Existing Project")
            if self.command == "add_db":
                self.abs_db_url = self.update_config_and_copy_sqlite_db(
                    f".. ..Adding Database [{self.bind_key}] to existing project")
        else:                                                                            # normal path - clone, [overlay nw]
            self.abs_db_url = create_project_with_nw_samples(self, "2. Create Project:")

        log.debug(f'3. Create/verify database/{self.model_file_name}, then use that to create api/ and ui/ models')
        model_creation_services = ModelCreationServices(project = self,   # Create database/models.py from db
            project_directory=self.project_directory)
        fix_database_models(self.project_directory, self.db_types, self.nw_db_status)
        invoke_creators(model_creation_services)  # MAJOR! creates api/expose_api_models, ui/admin & basic_web_app
        if self.extended_builder is not None and self.extended_builder != "":
            log.debug(f'4. Invoke extended_builder: {self.extended_builder}, ({self.db_url}, {self.project_directory})')
            invoke_extended_builder(self.extended_builder, self.abs_db_url, self.project_directory)

        copy_project_result = final_project_fixup("4. Final project fixup", self)

        if self.open_with != "":  # open project with open_with (vscode, charm, atom) -- NOT for docker!!
            start_open_with(open_with=self.open_with, project_name=self.project_name)

        if self.nw_db_status in ["nw", "nw+"] and self.command != "add_db":
            self.add_sqlite_security("ApiLogicProject customizable project created.  Adding Security:")
            
        if self.command.startswith("add_"):
            pass  # keep silent for add-db, add-auth...
        elif self.is_tutorial:
            log.debug(f"\nTutorial created.  Next steps:\n")
            log.debug(f'  Establish your Python environment - see https://apilogicserver.github.io/Docs/IDE-Execute/#execute-prebuilt-launch-configurations\n')
        else:
            disp_url = self.db_url
            if disp_url == "":
                disp_url = "nw"
            log.info(f"\n\nCustomizable project {self.project_name} created from database {disp_url}.  Next steps:\n")
            if self.multi_api:
                log.debug(f'Server already running.  To Access: Configuration > Load > //localhost:5656/{self.api_name}')
            else:
                log.info("\nRun API Logic Server:")
                if os.getenv('CODESPACES'):
                    # log.debug(f'  Add port 5656, with Public visibility') - automated in .devcontainer.json
                    log.info(f'  Execute using Launch Configuration "ApiLogicServer"')
                else:
                    log.info(f'  cd {self.project_name};  python api_logic_server_run.py')
        if self.command.startswith("add_"):
            pass  # keep silent for add-db, add-auth...
        elif self.is_tutorial:
            log.debug(f"  Proceed as described in the readme\n")
        else:
            if (is_docker()):
                if os.getenv('CODESPACES'):
                    log.info(f'\nCustomize right here, in Browser/VSCode - just as you would locally')
                    log.info(f'Save customized project to GitHub')
                else:
                    log.info(f'\nCustomize Docker project using IDE on local machine:')
                    docker_project_name = self.project_name
                    if self.project_name.startswith('/localhost/'):
                        docker_project_name = self.project_name[11:]
                    else:
                        docker_project_name = f'<local machine directory for: {self.project_name}>'
                    log.info(f'  exit  # exit the Docker container ')
                    log.info(f'  code {docker_project_name}  # e.g., open VSCode on created project')
            else:
                log.info(f'\nCustomize using your IDE:')
                log.info(f'  code {self.project_name}  # e.g., open VSCode on created project')
                log.info(f'  Establish your Python environment - see https://apilogicserver.github.io/Docs/IDE-Execute/#execute-prebuilt-launch-configurations\n')

        if self.run:  # synchronous run of server - does not return
            run_file = os.path.abspath(f'{resolve_home(self.project_name)}/api_logic_server_run.py')
            run_file = '"' + run_file + '"'  # spaces in file names - with windows
            run_args = ""
            if self.command == "create-and-run":
                run_args = "--create_and_run=True"
            create_utils.run_command(f'python {run_file} {run_args}', msg="\nStarting created API Logic Project")


def check_ports():
    try:
        rtn_hostname = socket.gethostname()
        rtn_local_ip = socket.gethostbyname(rtn_hostname)
    except:
        rtn_local_ip = f"cannot get local ip from {rtn_hostname}"
        log.debug(f"{rtn_local_ip}")
    port_check = False
    if port_check or is_docker():
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 5656  # Reserve a port for your service.
        port_is_available = True
        try:
            s.bind((host, port))  # Bind to the port
        except:
            port_is_available = False
        if not port_is_available:
            msg = "\nWarning - port 5656 does not appear to be available\n" \
                  "  Version 3.30 has changed port assignments to avoid port conflicts\n" \
                  "  For example, docker start:\n" \
                  "    docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server \n" \
                  "Ports are sometimes freed slowly, you may need to re-issue this command.\n\n"
            log.warning(msg)
            # sys.exit(msg)
        s.close()
    return rtn_hostname, rtn_local_ip


def key_module_map():
    """ not called - just index of key code - use this for hover, goto etc 
        ctl-l (^l) for last edit
    """
    import create_from_model.ui_admin_creator as ui_admin_creator
    import create_from_model.api_expose_api_models_creator as api_expose_api_models_creator
    import sqlacodegen_wrapper.sqlacodegen_wrapper as sqlacodegen_wrapper

    ProjectRun.create_project()                             # main driver, calls...
    create_project_with_nw_samples()                        # clone project, overlay nw
    model_creation_services = ModelCreationServices()       # creates resource_list (python db model); ctor calls...
    def and_the_ctor_calls():
        sqlacodegen_wrapper.create_models_py({})            # creates models.py via *sqlacodegen*
        sqlacodegen_wrapper.CodeGenerator.render_class()    # sqlacodegen - creates models_py as string
        model_creation_services.create_resource_list()      # creates resource_list via *dynamic import* of models.py
    invoke_creators(model_creation_services)                # creates api & ui, via create_from_model...
    api_expose_api_models_creator.create()                  # creates api/expose_api_models.py, key input to SAFRS        
    ui_admin_creator.create()                               # creates ui/admin/admin.yaml from resource_list
    create_utils.get_abs_db_url()                           # nw set here, dbname
    ProjectRun.update_config_and_copy_sqlite_db()           # adds db (model, binds, api, app) to curr project
    ProjectRun.add_sqlite_security()                        # add_db(auth), adds nw declare_security, upd config
    ProjectRun.tutorial()                                   # creates basic, nw, nw + cust