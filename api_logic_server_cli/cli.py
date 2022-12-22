# -*- coding: utf-8 -*-

'''
ApiLogicServer CLI: given a database url, create [and run] customizable ApiLogicProject.
    * Basically clones prototype project, and creates:
        * database/models.py for SQLAlchemy, using modified sqlacodegen & safrs metadata
        * ui/admin/admin.yaml for the Admin App     - using introspected models.py
        * api/expose_api_models.py for a safrs api  - using introspected models.py
    * Special provisions for NW Sample, to show customizations.
    * See end for key module map quick links...
'''

__version__ = "6.05.00"
recent_changes = \
    f'\n\nRecent Changes:\n' +\
    "\t12/21/2022 - 06.05.00: devops, env db uri, api endpoint names, git-push-new-project  \n"\
    "\t12/08/2022 - 06.04.05: Clarify creating docker repo, IP info, logic comments, nested result example \n"\
    "\t11/30/2022 - 06.04.00: Python 11 install fails (Issue 55), Remove confusing files (Issue 54) \n"\
    "\t11/22/2022 - 06.03.06: Image, Chkbox, Dialects, run.sh, SQL/Server url change, stop endpoint, Chinook Sqlite \n"\
    "\t10/02/2022 - 06.02.00: Option infer_primary_key, Oct1 SRA (issue 49), cleanup db/api setup, += postgres dvr \n"\
    "\t09/15/2022 - 06.01.00: Multi-app Projects \n"\
    "\t09/07/2022 - 06.00.09: show_when isInserting \n"\
    "\t09/03/2022 - 06.00.07: Codespaces - create to '.' or './', preserve readme, perform_customizations \n"\
    "\t08/29/2022 - 06.00.01: Admin App show_when & cascade add. Simplify Codespaces swagger url & use default config \n"\
    "\t08/15/2022 - 05.03.34: Remove Postgres driver from local install, Fix ApiLogicServer run fails (Issue 45) \n"\
    "\t07/24/2022 - 05.03.26: api_logic_server_run refactor, codespaces support \n"\
    "\t07/15/2022 - 05.03.17: Add swagger_host for create & run, Docker env \n"\
    "\t06/27/2022 - 05.03.06: nw-, with perform_customizations docker \n"\
    "\t06/22/2022 - 05.03.00: Docker support to load/run project (env or sh), create ApiLogicProject image \n"\
    "\t06/12/2022 - 05.02.22: No pyodbc by default, model customizations simplified, better logging \n"\
    "\t05/30/2022 - 05.02.16: Python 3.10, Dockerfile include, start info \n"\
    "\t05/04/2022 - 05.02.03: alembic for database migrations, admin-merge.yaml \n"\
    "\t04/27/2022 - 05.01.02: copy_children, with support for nesting (children and grandchildren, etc.) \n"\
    "\t04/02/2022 - 05.00.09: Windows Werkzeug version, run Configurations for PyCharm \n"\
    "\t03/27/2022 - 05.00.06: Introducing Behave test framework, LogicBank bugfix \n"\
    "\t02/07/2022 - 04.01.08: SQLAlchemy 1.4; cli param: api_name (. option), multi_api; db open failure info \n"\
    "\t12/26/2021 - 04.00.05: Introducing the admin app, with Readme Tutorial \n"\
    "\t11/13/2021 - 03.50.01: rebuild-from-database/model, improved relationship support, port conflict msg \n"\
    "\t11/04/2021 - 03.40.01: Per MacOS Monterey, default ports to 5001, 5002 \n"\
    "\t09/29/2021 - 03.01.15: run (now just runs without create), added create-and-run \n"\
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

import logging
import datetime
from typing import NewType
import sys
import os
import importlib
import click


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    return str(python_path)


# print("sys.path.append(get_api_logic_server_dir())\n",get_api_logic_server_dir())
sys.path.append(get_api_logic_server_dir())  # e.g, on Docker: export PATH="/home/api_logic_server/api_logic_server_cli"
api_logic_server_path = os.path.dirname(get_api_logic_server_dir())  # e.g: export PATH="/home/api_logic_server"
sys.path.append(api_logic_server_path)
from create_from_model.model_creation_services import ModelCreationServices

import sqlacodegen_wrapper.sqlacodegen_wrapper as expose_existing_callable
import create_from_model.api_logic_server_utils as create_utils


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
default_fab_host = "localhost"
os_cwd = os.getcwd()
if os.path.exists('/home/api_logic_server'):  # docker?
    default_project_name = "/localhost/ApiLogicProject"
    default_fab_host = "0.0.0.0"
nw_db_status = ""
""" '', nw, nw+, nw- """

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


def copy_project_to_local(project_directory, copy_to_project_directory, message) -> str:
    """
    fab cannot create-app on a mount, so we created temp_created_project, and then copy_to_local

    test with create, silent, copy (lock /Users/Shared/copy_test for negative test)
    """
    result = ""
    try:
        # print(f'10. Copy temp_created_project to {copy_to_project_directory} ')
        delete_dir(copy_to_project_directory, message)
        shutil.copytree(project_directory, copy_to_project_directory)
    except OSError as e:
        if "Delete or copy tree failed" in e.strerror:
            pass
        else:
            result = "Error: %s : %s" % (copy_to_project_directory, e.strerror)
            print(result)
            print(f'\n===> Copy failed (see above), but your project exists at {project_directory}')
            print(f'===> Resolve the issue, and use the cp command below...')
    return result


def copy_if_mounted(project_directory):
    """
    fab is unable to create-app in mounted path
    so, if mounted, create files in "created_project" and later copy to 
    
    this approach is superceded by not using fab.create-app, now just copy the fab skeleton project files

    :param project_directory: name of project created
    :return: project_directory: name of project created (or "created_project"), copy_to_project (target copy when mounted, else "")
    """
    global os_cwd
    return_project_directory = project_directory
    return_copy_to_directory = ""
    cwd = os_cwd
    if project_directory == ".":
        code_path = os.path.dirname(os.path.realpath(__file__))
        if cwd == code_path:  # '/Users/val/dev/ApiLogicServer/api_logic_server_cli':
            return_project_directory = "/Users/val/dev/servers/current"
        else:
            return_project_directory = cwd
    use_copy_strategy = False  # must be true for fab-based creation (see fab_creator - use_fab_based_creation)
    if use_copy_strategy and os.name == "posix":  # mac, docker...
        directory_is_mounted = project_directory.startswith("/local") or "copy_test" in project_directory
        if directory_is_mounted:  # TODO: https://www.baeldung.com/linux/bash-is-directory-mounted
            running_at =  Path(__file__)
            cli_path = running_at.parent.absolute()
            root_path = cli_path.parent.absolute()
            return_project_directory = str(root_path) + f'/{temp_created_project}'
            return_copy_to_directory = project_directory
    return return_project_directory, return_copy_to_directory


def create_nw_tutorial(project_name, api_logic_server_dir_str):
    """ copy tutorial from docs, and link to it from readme.md """

    tutorial_file_proj = open(project_name + '/Tutorial.md', 'w')
    tutorial_file_docs_path = Path(api_logic_server_dir_str).\
        joinpath('docs').joinpath("Tutorial.md")
    tutorial_file_docs = open(tutorial_file_docs_path)  # /Users/val/dev/ApiLogicServer/docs/Tutorial.md
    tutorial_readme = tutorial_file_docs.read()
    tutorial_file_proj.write(tutorial_readme)
    tutorial_file_proj.close()

    project_readme_file_path = project_name + '/readme.md'
    standard_readme_file_path = str(Path(api_logic_server_dir_str).\
        joinpath('project_prototype').joinpath("readme.md"))
    with open(project_readme_file_path, 'a') as project_readme_file:
        with open(standard_readme_file_path) as standard_readme_file:
            project_readme_file.write(standard_readme_file.read())


def get_project_directory_and_api_name(project_name: str, api_name: str, multi_api: bool):
    """
    user-supplied project_name, less the twiddle (which might be in project_name); typically relative to cwd.

    :param project_name: a file name, eg, ~/Desktop/a.b
    :param api_name: defaults to 'api'
    :param multi_api: cli arg - e.g., set by alsdock

    :return:
            rtn_project_directory -- /users/you/Desktop/a.b (removes the ~)

            rtn_api_name -- api_name, or last node of project_name if multi_api or api_name is "."

            rtn_merge_into_prototype -- preserve contents of current (".", "./") *prototype* project
    """

    global os_cwd
    rtn_project_directory = project_name    # eg, '../../servers/ApiLogicProject'
    rtn_api_name = api_name                 # typically api
    rtn_merge_into_prototype = False        
    if rtn_project_directory.startswith("~"):
        rtn_project_directory = str(Path.home()) + rtn_project_directory[1:]
    if rtn_project_directory == '.' or rtn_project_directory == './':
        rtn_project_directory = os_cwd
        rtn_merge_into_prototype = True
        msg = ''
        if rtn_project_directory == get_api_logic_server_dir():
            rtn_project_directory = str( Path(get_api_logic_server_dir()) / 'ApiLogicProject' )
            msg = ' <dev>'
        print(f'1. Merge into project prototype: {rtn_project_directory}{msg}')
    project_path = Path(rtn_project_directory)
    project_path_last_node = project_path.parts[-1]
    if multi_api or api_name == ".":
        rtn_api_name = project_path_last_node
    return rtn_project_directory, \
        rtn_api_name, \
        rtn_merge_into_prototype


def create_project_with_nw_samples(project_directory: str, project_name: str,
                                    merge_into_prototype: bool, api_name: str,
                                    from_git: str, msg: str,
                                    abs_db_url: str, nw_db_status: str) -> str:
    """
    clone prototype to  project directory, copy sqlite db, and remove git folder

    if nw/nw+, inject sample logic/declare_logic and api/customize_api.

    :param project_directory: name of project created
    :param project_name: actual user parameter (might have ~, .)
    :param merge_into_prototype: if True, merge creation into project_directory
    :param api_name: node in rest uri
    :param from_git: name of git project to clone (blank for default)
    :param msg printed, such as Create Project:
    :param abs_db_url: non-relative location of db
    :param nw_db_status one of ["", "nw", "nw+", "nw-"]
    :return: return_abs_db_url (e.g., reflects sqlite copy to project/database dir)
    """

    import tempfile
    cloned_from = from_git
    tmpdirname = ""
    with tempfile.TemporaryDirectory() as tmpdirname:

        if merge_into_prototype:
            pass
        else:
            remove_project_debug = True
            if remove_project_debug and project_name != ".":
                delete_dir(realpath(project_directory), "1.")

        from_dir = from_git
        api_logic_server_dir_str = str(get_api_logic_server_dir())  # fixme not req'd
        if from_git.startswith("https://"):
            cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project_directory
            cmd = f'git clone --quiet {from_git} {project_directory}'
            result = create_utils.run_command(cmd, msg=msg)  # "2. Create Project")
            delete_dir(f'{project_directory}/.git', "3.")
        else:
            if from_dir == "":
                from_dir = (Path(api_logic_server_dir_str)).\
                    joinpath('project_prototype')  # /Users/val/dev/ApiLogicServer/project_prototype
            print(f'{msg} {os.path.realpath(project_directory)}')
            print(f'.. ..Clone from {from_dir} ')
            cloned_from = from_dir
            try:
                if merge_into_prototype:
                    # tmpdirname = tempfile.TemporaryDirectory() 
                    recursive_overwrite(project_directory, str(tmpdirname))       # user proto -> temp
                    delete_dir(str(Path(str(tmpdirname)) / ".devcontainer"), "")  # clean it up
                    delete_dir(str(Path(str(tmpdirname)) / "api"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "database"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "logic"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "test"), "")
                    delete_dir(str(Path(str(tmpdirname)) / "ui"), "")
                    if os.path.exists(str(Path(str(tmpdirname))  / "api_logic_server_run.py" )):
                        os.remove(str(Path(str(tmpdirname)) / "api_logic_server_run.py"))
                    delete_dir(realpath(project_directory), "")
                    recursive_overwrite(from_dir, project_directory)  # ApiLogic Proto -> new project
                else:
                    shutil.copytree(from_dir, project_directory)  # normal path (fails if project_directory not empty)
            except OSError as e:
                print(f'\n==>Error - unable to copy to {project_directory} -- see log below'
                    f'\n\n{str(e)}\n\n'
                    f'Suggestions:\n'
                    f'.. Verify the --project_name argument\n'
                    f'.. If you are using Docker, verify the -v argument\n\n')
        if nw_db_status in ["nw", "nw+"]:
            print(".. ..Copy in nw customizations: logic, custom api, readme, tests, admin app")
            nw_dir = (Path(api_logic_server_dir_str)).\
                joinpath('project_prototype_nw')  # /Users/val/dev/ApiLogicServer/api_logic_server_cli/project_prototype
            recursive_overwrite(nw_dir, project_directory)

            create_nw_tutorial(project_directory, api_logic_server_dir_str)

        if nw_db_status in ["nw-"]:
            print(".. ..Copy in nw- customizations: readme, perform_customizations")
            nw_dir = (Path(api_logic_server_dir_str)).\
                joinpath('project_prototype_nw_no_cust')  # /Users/val/dev/ApiLogicServer/project_prototype_nw_no_cust
            recursive_overwrite(nw_dir, project_directory)

        create_utils.replace_string_in_file(search_for="creation-date",
                            replace_with=str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                            in_file=f'{project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_version",
                            replace_with=__version__,
                            in_file=f'{project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_template",
                            replace_with=f'{from_dir}',
                            in_file=f'{project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_project_directory",
                            replace_with=f'{project_directory}',
                            in_file=f'{project_directory}/readme.md')
        create_utils.replace_string_in_file(search_for="api_logic_server_api_name",
                            replace_with=f'{api_name}',
                            in_file=f'{project_directory}/readme.md')

        do_fix_docker_for_vscode_dockerfile = True
        """
        if do_fix_docker_for_vscode_dockerfile:
            if arch.get_platform():
                create_utils.replace_string_in_file(search_for="apilogicserver/api_logic_server",
                                    replace_with=f'apilogicserver/arm-slim',
                                    in_file=f'{project_directory}/For_VSCode.dockerfile')
        """

        project_directory_actual = os.path.abspath(project_directory)  # make path absolute, not relative (no /../)
        return_abs_db_url = abs_db_url
        copy_sqlite = True
        if copy_sqlite == False or "sqlite" not in abs_db_url:
            db_uri = get_windows_path_with_slashes(abs_db_url)
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=db_uri,
                                in_file=f'{project_directory}/config.py')
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=db_uri,
                                in_file=f'{project_directory}/database/alembic.ini')
        else:
            """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
            """
            # strip sqlite://// from sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/nw.sqlite
            db_loc = abs_db_url.replace("sqlite:///", "")
            target_db_loc_actual = project_directory_actual + '/database/db.sqlite'
            copyfile(db_loc, target_db_loc_actual)
            backup_db = project_directory_actual + '/database/db-backup.sqlite'
            copyfile(db_loc, backup_db)

            if os.name == "nt":  # windows
                # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
                target_db_loc_actual = get_windows_path_with_slashes(project_directory_actual + '\database\db.sqlite')
            # db_uri = f'sqlite:///{target_db_loc_actual}'
            return_abs_db_url = f'sqlite:///{target_db_loc_actual}'
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=return_abs_db_url,
                                in_file=f'{project_directory}/config.py')
            create_utils.replace_string_in_file(search_for="replace_db_url",
                                replace_with=return_abs_db_url,
                                in_file=f'{project_directory}/database/alembic.ini')
            api_config_file_name = \
                os.path.dirname(os.path.realpath(__file__)) +"/create_from_model/templates/api_config.txt"
            with open(api_config_file_name, 'r') as file:
                api_config = file.read()
            create_utils.insert_lines_at(lines=api_config,
                                        at="override SQLALCHEMY_DATABASE_URI here as required",
                                        file_name=f'{project_directory}/config.py')

            print(f'.. ..Sqlite database setup {target_db_loc_actual}...')
            print(f'.. .. ..From {db_loc}')
            print(f'.. .. ..db_uri set to: {return_abs_db_url} in <project>/config.py')
        if merge_into_prototype:
            recursive_overwrite(str(tmpdirname), project_directory)
            # delete_dir(realpath(Path(str(tmpdirname))), "")
            # os.removedirs(Path(str(tmpdirname)))
            # tmpdirname.cleanup()
    return return_abs_db_url


def create_basic_web_app(db_url, project_name, msg):  # remove - now creating by simple copy directory
    project_abs_path = abspath(project_name)
    fab_project = project_abs_path + "/ui/basic_web_app"
    cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
    result = create_utils.run_command(cmd, msg=msg)
    pass


def write_expose_api_models(project_name, apis):
    text_file = open(project_name + '/api/expose_api_models.py', 'a')
    text_file.write(apis)
    text_file.close()


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
    if db_types != "":
        print(f'.. .. ..Injecting file {db_types} into database/models.py')
        with open(db_types, 'r') as file:
            db_types_data = file.read()
        create_utils.insert_lines_at(lines=db_types_data, at="(typically via --db_types)", file_name=models_file_name)
    if nw_db_status in ["nw", "nw+"]:
        print(f'.. .. ..Setting cascade delete for sample database database/models.py')
        create_utils.replace_string_in_file(in_file=models_file_name,
            search_for="OrderDetailList = relationship('OrderDetail', cascade_backrefs=True, backref='Order')",
            replace_with="OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=True, backref='Order')  # manual fix")


def final_project_fixup(msg, project_name, project_directory, api_name,
                        host, port, swagger_host, use_model, copy_to_project_directory) -> str:
    print(msg)  # "7. Final project fixup"

    if False and use_model == "" and command != "rebuild-from-model":  # TODO remove dead code
        msg = f' a.   Appending "from database import customize_models" to database/models.py'
        fix_database_models__import_customize_models(project_directory, msg)

    copy_project_result = ""
    if command.startswith("rebuild"):
        pass
    else:
        print(f' b.   Update api_logic_server_run.py with '
              f'project_name={project_name} and api_name, host, port')
        update_api_logic_server_run(project_name, project_directory, api_name, host, port, swagger_host)

        fix_host_and_ports(" c.   Fixing api/expose_services - port, host", project_directory, host, port)

        copy_project_result = ""
        if copy_to_project_directory != "":
            copy_project_result = \
                copy_project_to_local(project_directory, copy_to_project_directory,
                                      f'10. Copy temp_created_project over {copy_to_project_directory} ')

        api_logic_server_info_file_dict["last_created_project_name"] = project_directory  # project_name - twiddle
        api_logic_server_info_file_dict["last_created_date"] = str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
        api_logic_server_info_file_dict["last_created_version"] = __version__
        with open(api_logic_server_info_file_name, 'w') as api_logic_server_info_file_file:
            yaml.dump(api_logic_server_info_file_dict, api_logic_server_info_file_file, default_flow_style=False)
    return copy_project_result


def fix_database_models__import_customize_models(project_directory: str, msg: str):
    """ Append "from database import customize_models" to database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    print(msg)
    models_file = open(models_file_name, 'a')
    models_file.write("\n\nfrom database import customize_models\n")
    models_file.close()


def update_api_logic_server_run(project_name, project_directory, api_name, host, port, swagger_host):
    """
    Updates project_name, ApiLogicServer hello, project_dir in api_logic_server_run_py

    Note project_directory is from user, and may be relative (and same as project_name)
    """
    project_directory_actual = os.path.abspath(project_directory)  # make path absolute, not relative (no /../)
    api_logic_server_run_py = f'{project_directory}/api_logic_server_run.py'
    create_utils.replace_string_in_file(search_for="\"api_logic_server_project_name\"",  # fix logic_bank_utils.add_python_path
                           replace_with='"' + os.path.basename(project_name) + '"',
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="ApiLogicServer hello",
                           replace_with="ApiLogicServer generated at:" +
                                        str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                           in_file=api_logic_server_run_py)
    project_directory_fix = project_directory_actual
    if os.name == "nt":  # windows
        project_directory_fix = get_windows_path_with_slashes(str(project_directory_actual))
    create_utils.replace_string_in_file(search_for="\"api_logic_server_project_dir\"",  # for logging project location
                           replace_with='"' + project_directory_fix + '"',
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_api_name",  # last node of server url
                           replace_with=api_name,
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_host",
                           replace_with=host,
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_swagger_host",
                           replace_with=swagger_host,
                           in_file=api_logic_server_run_py)
    replace_port = f', port="{port}"' if port else ""  # TODO: consider reverse proxy

    create_utils.replace_string_in_file(search_for="api_logic_server_version",
                           replace_with=__version__,
                           in_file=api_logic_server_run_py)

    create_utils.replace_string_in_file(search_for="api_logic_server_created_on",
                           replace_with=str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                           in_file=api_logic_server_run_py)

    create_utils.replace_string_in_file(search_for="api_logic_server_port",   # server port
                           replace_with=port,
                           in_file=api_logic_server_run_py)
    pass


def fix_host_and_ports(msg, project_name, host, port):
    """ c.   Fixing api/expose_services - port, host """
    print(msg)  # c.   Fixing api/expose_services - port, host
    replace_port = f':{port}' if port else ""
    # replace_with = host + replace_port
    in_file = f'{project_name}/api/customize_api.py'
    create_utils.replace_string_in_file(search_for="api_logic_server_host",
                           replace_with=host,
                           in_file=in_file)
    create_utils.replace_string_in_file(search_for="api_logic_server_port",
                           replace_with=replace_port,
                           in_file=in_file)
    print(f' d.   Updated customize_api_py with port={port} and host={host}')
    full_path = os.path.abspath(project_name)
    create_utils.replace_string_in_file(search_for="python_anywhere_path",
                           replace_with=full_path,
                           in_file=f'{project_name}/python_anywhere_wsgi.py')
    print(f' e.   Updated python_anywhere_wsgi.py with {full_path}')


def start_open_with(open_with: str, project_name: str):
    """ Creation complete.  Opening {open_with} at {project_name} """
    print(f'\nCreation complete - Opening {open_with} at {project_name}')
    print(".. See the readme for install / run instructions")
    create_utils.run_command(f'{open_with} {project_name}', None, "no-msg")


def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    assert path_result == env_result
    return path_result


def get_abs_db_url(msg, db_url):
    """
    non-relative db location - we work with this

    but NB: we copy sqlite db to <project>/database - see create_project_with_nw_samples

    also: compute physical nw db name (usually nw-gold) to be used for copy

    returns abs_db_url - the real url (e.g., for nw), and whether it's really nw
    """
    rtn_nw_db_status = ""  # presume not northwind
    rtn_abs_db_url = db_url

    # SQL/Server urls make VScode fail due to '?', so unfortunate work-around... (better: internalConsole)
    if rtn_abs_db_url.startswith('{install}'):
        install_db = str(Path(get_api_logic_server_dir()).joinpath('database'))
        rtn_abs_db_url = rtn_abs_db_url.replace('{install}', install_db)
    if rtn_abs_db_url.startswith('SqlServer-arm'):
        pass

    if db_url in [default_db, "", "nw", "sqlite:///nw.sqlite"]:     # nw-gold:      default sample
        # abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
        rtn_abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/database/nw-gold.sqlite'
        rtn_nw_db_status = "nw"
        print(f'{msg} from: {rtn_abs_db_url}')  # /Users/val/dev/ApiLogicServer/api_logic_server_cli/database/nw-gold.sqlite
    elif db_url == "nw-":                                           # nw:           just in case
        rtn_abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/database/nw-gold.sqlite'
        rtn_nw_db_status = "nw-"
    elif db_url == "nw--":                                           # nw:           unused - avoid
        rtn_abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/database/nw.sqlite'
        rtn_nw_db_status = "nw-"
    elif db_url == "nw+":                                           # nw-gold-plus: next version
        rtn_abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/database/nw-gold-plus.sqlite'
        rtn_nw_db_status = "nw+"
        print(f'{msg} from: {rtn_abs_db_url}')
    elif db_url.startswith('sqlite:///'):
        url = db_url[10: len(db_url)]
        rtn_abs_db_url = abspath(url)
        rtn_abs_db_url = 'sqlite:///' + rtn_abs_db_url
    return rtn_abs_db_url, rtn_nw_db_status


def print_options(project_name: str, api_name: str, db_url: str,
                  host: str, port: str, swagger_host: str, not_exposed: str,
                  from_git: str, db_types: str, open_with: str, run: bool, use_model: str, admin_app: bool,
                  flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin:bool,
                  extended_builder: str, multi_api: bool, infer_primary_key: bool):
    """ Creating ApiLogicServer with options: (or uri helo) """
    if db_url == "?":
        print_uri_info()
        exit(0)

    print_options = True
    if print_options:
        print(f'\n\nCreating ApiLogicServer with options:')
        print(f'  --db_url={db_url}')
        print(f'  --project_name={project_name}   (pwd: {os_cwd})')
        print(f'  --api_name={api_name}')
        print(f'  --admin_app={admin_app}')
        print(f'  --react_admin={react_admin}')
        print(f'  --flask_appbuilder={flask_appbuilder}')
        print(f'  --from_git={from_git}')
        #        print(f'  --db_types={db_types}')
        print(f'  --run={run}')
        print(f'  --host={host}')
        print(f'  --port={port}')
        print(f'  --swagger_host={swagger_host}')
        print(f'  --not_exposed={not_exposed}')
        print(f'  --open_with={open_with}')
        print(f'  --use_model={use_model}')
        print(f'  --favorites={favorites}')
        print(f'  --non_favorites={non_favorites}')
        print(f'  --extended_builder={extended_builder}')
        print(f'  --multi_api={multi_api}')
        print(f'  --infer_primary_key={infer_primary_key}')


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

    print(" b.  Create api/expose_api_models.py from models")
    # print(f'---> cwd: {model_creation_services.os_cwd}')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/api_expose_api_models_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)  # runs "bare" module code (e.g., initialization)
    creator.create(model_creation_services)  # invoke create function

    if model_creation_services.admin_app:
        print(" c.  Create ui/admin/admin.yaml from models")
        spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/ui_admin_creator.py')
        creator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(creator)
        creator.create(model_creation_services)
    else:
        pass
        # print(".. .. ..ui/admin_app creation declined")

    if model_creation_services.flask_appbuilder:
        print(" d.  Create ui/basic_web_app/app/views.py (import / iterate models)")
        creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
        spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/ui_basic_web_app_creator.py')
        creator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(creator)
        creator.create(model_creation_services)
    else:
        print(" d.  Create ui/basic_web_app -- declined")

    model_creation_services.close_app()  # this may no longer be required


def api_logic_server(project_name: str, db_url: str, api_name: str,
                     host: str, port: str, swagger_host: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str, admin_app: bool,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin: bool,
                     extended_builder: str, multi_api: bool, infer_primary_key: bool):
    """
    Creates logic-enabled Python safrs api/admin project, options for FAB and execution

    main driver

    :param project_name could be ~, or volume - creates this folder
    :param db_url SQLAlchemy url
    :param host where safrs finds the api
    :param port where safrs finds the port
    :param extended_builder python file invoked to augment project
    :returns: none
    """

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
    print_options(project_name = project_name, db_url=db_url, api_name=api_name,
                  host=host, port=port, swagger_host = swagger_host, not_exposed=not_exposed,
                  from_git=from_git, db_types=db_types, open_with=open_with, run=run, use_model=use_model,
                  flask_appbuilder=flask_appbuilder, favorites=favorites, non_favorites=non_favorites,
                  react_admin=react_admin, admin_app=admin_app,
                  extended_builder=extended_builder, multi_api=multi_api, infer_primary_key=infer_primary_key)

    print(f"\nApiLogicServer {__version__} Creation Log:")

    global nw_db_status
    abs_db_url, nw_db_status = get_abs_db_url("0. Using Sample DB", db_url)

    if extended_builder == "*":
        extended_builder = abspath(f'{abspath(get_api_logic_server_dir())}/extended_builder.py')
        print(f'0. Using default extended_builder: {extended_builder}')

    project_directory, api_name, merge_into_prototype = \
        get_project_directory_and_api_name(project_name=project_name,
                                           api_name=api_name,
                                           multi_api=multi_api)

    project_directory, copy_to_project_directory = copy_if_mounted(project_directory)
    if not command.startswith("rebuild"):
        abs_db_url = create_project_with_nw_samples(project_directory, # no twiddle, resolve .
                                                    project_name,      # actual user parameter
                                                    merge_into_prototype,
                                                    api_name,
                                                    from_git, "2. Create Project:",
                                                    abs_db_url,        # sqlite DBs are copied to proj/database
                                                    nw_db_status)
    else:
        print("1. Not Deleting Existing Project")
        print("2. Using Existing Project")

    print(f'3. Create/verify database/models.py, then use that to create api/ and ui/ models')
    model_creation_services = ModelCreationServices(  # Create database/models.py from db
        project_directory=project_directory, command = command, os_cwd=os_cwd,
        copy_to_project_directory = copy_to_project_directory,
        api_logic_server_dir = get_api_logic_server_dir(), api_name=api_name,
        abs_db_url=abs_db_url, db_url=db_url, nw_db_status=nw_db_status,
        host=host, port=port, use_model = use_model,
        not_exposed=not_exposed + " ", flask_appbuilder = flask_appbuilder, admin_app=admin_app,
        favorite_names=favorites, non_favorite_names=non_favorites,
        react_admin=react_admin, version = __version__, multi_api=multi_api, infer_primary_key=infer_primary_key)
    fix_database_models(project_directory, db_types, nw_db_status)
    invoke_creators(model_creation_services)  # MAJOR! creates api/expose_api_models, ui/admin & basic_web_app
    if extended_builder is not None and extended_builder != "":
        print(f'4. Invoke extended_builder: {extended_builder}({db_url}, {project_directory})')
        invoke_extended_builder(extended_builder, db_url, project_directory)

    copy_project_result = final_project_fixup("4. Final project fixup", project_name, project_directory, api_name,
                                              host, port, swagger_host, 
                                              use_model, copy_to_project_directory)

    if open_with != "":  # open project with open_with (vscode, charm, atom) -- NOT for docker!!
        start_open_with(open_with=open_with, project_name=project_name)

    print("\n\nApiLogicProject customizable project created.  Next steps:")
    print("==========================================================")
    if multi_api:
        print(f'Server already running.  To Access: Configuration > Load > //localhost:5656/{api_name}')
    else:
        print("\nRun API Logic Server:")
        if os.getenv('CODESPACES'):
            # print(f'  Add port 5656, with Public visibility') - automated in .devcontainer.json
            print(f'  Execute using Launch Configuration "ApiLogicServer"')
        else:
            print(f'  cd {project_name};  python api_logic_server_run.py')
    if copy_project_result != "":  # never used...  or project_directory.endswith("api_logic_server")?
        print(f'  copy project to local machine, e.g. cp -r {project_directory}/. {copy_to_project_directory}/ ')
        # cp -r '/Users/val/dev/ApiLogicServer/temp_created_project'. /Users/Shared/copy_test/
    if (is_docker()):
        if os.getenv('CODESPACES'):
            print(f'\nCustomize right here, in Browser/VSCode - just as you would locally')
            print(f'Save customized project to GitHub (TBD)')
        else:
            print(f'\nCustomize Docker project using IDE on local machine:')
            docker_project_name = project_name
            if project_name.startswith('/localhost/'):
                docker_project_name = project_name[11:]
            else:
                docker_project_name = f'<local machine directory for: {project_name}>'
            print(f'  exit  # exit the Docker container ')
            print(f'  code {docker_project_name}  # e.g., open VSCode on created project')
    else:
        print(f'\nCustomize using your IDE:')
        print(f'  code {project_name}  # e.g., open VSCode on created project')
        print(f'  Establish your Python environment - see https://valhuber.github.io/ApiLogicServer/Execute-VSCode-Local/')
    print("\n")  # api_logic_server  ApiLogicServer  SQLAlchemy

    if run:  # synchronous run of server - does not return
        # run_file = os.path.abspath(f'{project_directory}/api_logic_server_run.py')
        # create_utils.run_command(f'python {run_file} {host}', msg="\nRun created ApiLogicServer project")
        run_file = os.path.abspath(f'{resolve_home(project_name)}/api_logic_server_run.py')
        run_args = ""
        if command == "create-and-run":
            run_args = "--create_and_run=True"
        create_utils.run_command(f'python {run_file} {run_args}', msg="\nStarting created API Logic Project")

'''  exploring no-args, not a clue
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='no_args', default_if_no_args=True)
def main():
    """
    wonder if this can just do something
    """
    click.echo("group execution (never happens)")

# @click.pass_context
@main.command()
@click.option('--config', default=None)
def no_args(config):
    print("no args!!")


@click.group()
@click.pass_context
@main.command("mainZ")
def mainZ(ctx):
    """
    Creates [and runs] logic-enabled Python database API Logic Projects.

\b
    Doc: https://valhuber.github.io/ApiLogicServer

\b
    Examples:

\b
        ApiLogicServer create-and-run --db_url= project_name=  # defaults to Tutorial
        ApiLogicServer create                                  # prompts

    Then, customize created API Logic Project in your IDE
    """
    print("Never executed")
'''

@click.group()
@click.pass_context
def main(ctx):
    """
    Creates [and runs] logic-enabled Python database API Logic Projects.

\b
    Doc: https://valhuber.github.io/ApiLogicServer

\b
    Examples:

\b
        ApiLogicServer create-and-run --db_url= project_name=  # defaults to Tutorial
        ApiLogicServer create                                  # prompts

    Then, customize created API Logic Project in your IDE
    """
    # click.echo("main - called iff commands supplied")


@main.command("about")
@click.pass_context
def about(ctx):
    """
        Recent Changes, system information.
    """
    global recent_changes

    print(f'\tInstalled at {abspath(__file__)}\n')
    print(f'\thttps://valhuber.github.io/ApiLogicServer/Tutorial/\n')

    def print_at(label: str, value: str):
        tab_to = 30 - len(label)
        spaces = ' ' * tab_to
        print(f'{label}: {spaces}{value}')

    print("\nPYTHONPATH..")
    for p in sys.path:
        print(".." + p)
    print("")
    print("api_logic_server_info...")
    for key, value in api_logic_server_info_file_dict.items():
        print_at(f'  {key}', value)
    print("")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print_at('ApiLogicServer version', __version__)
    print_at('ip (gethostbyname)', local_ip)
    print_at('on hostname', hostname)
    print_at('cwd', os. getcwd())
    print_at("Python version", create_utils.run_command(f'python --version', msg="no-msg"))
    print_at("Docker", is_docker())

    click.echo(
        click.style(recent_changes)
    )


@main.command("welcome")
@click.pass_context
def welcome(ctx):
    """
        Just print version and exit.
    """


@main.command("create")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")  # option text shown on create --help
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--multi_api/--no_multi_api',
              default=False, is_flag=True,
              help="Create multiple APIs")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
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
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def create(ctx, project_name: str, db_url: str, not_exposed: str, api_name: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           multi_api: click.BOOL,
           infer_primary_key: click.BOOL):
    """
        Creates new customizable project (overwrites).
    """
    global command
    command = "create"
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url, api_name=api_name,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder, multi_api=multi_api, infer_primary_key=infer_primary_key)


@main.command("create-and-run")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
@click.option('--multi_api/--no_multi_api',
              default=False, is_flag=True,
              help="Create multiple APIs")
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
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def create_and_run(ctx, project_name: str, db_url: str, not_exposed: str, api_name: str,
        from_git: str,
        # db_types: str,
        open_with: str,
        run: click.BOOL,
        admin_app: click.BOOL,
        flask_appbuilder: click.BOOL,
        react_admin: click.BOOL,
        use_model: str,
        host: str,
        port: str,
        swagger_host: str,
        favorites: str, non_favorites: str,
        extended_builder: str,
        multi_api: click.BOOL,
        infer_primary_key: click.BOOL):
    """
        Creates new project and runs it (overwrites).
    """
    global command
    command = "create-and-run"
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url, api_name=api_name,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder, multi_api=multi_api, infer_primary_key=infer_primary_key)


@main.command("rebuild-from-database")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
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
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def rebuild_from_database(ctx, project_name: str, db_url: str, api_name: str, not_exposed: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           infer_primary_key: click.BOOL):
    """
        Updates database, api, and ui from changed db.

\b
        ex
\b
        ApiLogicServer rebuild-from-database --project_name=~/dev/servers/ApiLogicProject --db_url=nw

    """
    global command
    command = "rebuild-from-database"
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url, api_name=api_name,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder, multi_api=False, infer_primary_key=infer_primary_key)


@main.command("rebuild-from-model")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
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
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def rebuild_from_model(ctx, project_name: str, db_url: str, api_name: str, not_exposed: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           infer_primary_key: click.BOOL):
    """
        Updates database, api, and ui from changed models.
    """
    global command
    command = "rebuild-from-model"
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url, api_name=api_name,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder, multi_api=False, infer_primary_key=infer_primary_key)


@main.command("run")
@click.option('--project_name',
              default=f'{last_created_project_name}',
              prompt="Project to run",
              help="Project to run")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.pass_context
def run_api(ctx, project_name: str, host: str="localhost", port: str="5656", swagger_host: str="localhost"):
    """
        Runs existing project.


\b
        Example

\b
            ApiLogicServer run --project_name=/localhost/ApiLogicProject
            ApiLogicServer run --project_name=    # runs last-created project
    """
    global command
    command = "run-api"
    proj_dir = project_name
    if proj_dir == "":
        proj_dir = last_created_project_name
    else:
        proj_dir = os.path.abspath(f'{resolve_home(project_name)}')
    run_file = f'{proj_dir}/api_logic_server_run.py '  # alert: sending args makes it hang: {host} {port} {swagger_host}
    create_utils.run_command(f'python {run_file}', msg="Run Created ApiLogicServer Project", new_line=True)
    print("run complete")


@main.command("create-ui")
@click.option('--use_model',
              default="models.py",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.pass_context
def create_ui(ctx, use_model: str,
              favorites: str, non_favorites: str,
              ):
    """
        Creates models.yaml from models.py (internal admin ui).


\b
        Example

\b
            ApiLogicServer create-ui --use_model=~/dev/ApiLogicServer/tests/models-nw-plus.py
    """
    global command
    command = "create-ui"
    admin_out = resolve_home(use_model.replace("py","yaml"))
    project_directory, ignore = os.path.split(resolve_home(use_model))
    print(f'1. Loading existing model: {use_model}')
    model_creation_services = ModelCreationServices(  # fills in rsource_list for ui_admin_creator
        use_model=use_model,
        favorite_names=favorites, non_favorite_names=non_favorites,
        project_directory=project_directory,
        command=command,
        version=__version__)

    print(f'2. Creating yaml from model')
    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/ui_admin_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)
    admin_yaml_dump = creator.create(model_creation_services)

    print(f'3. Writing yaml: {admin_out}')
    with open(admin_out, 'w') as yaml_file:
        yaml_file.write(admin_yaml_dump)


@main.command("examples")
@click.pass_context
def examples(ctx):
    """
    Example commands, including SQLAlchemy URIs.
    """
    print_uri_info()


log = logging.getLogger(__name__)


def print_uri_info():
    """
    Creates and optionally runs a customizable Api Logic Project, Example

    URI examples, Docs URL
    """
    header = [
        '',
        'Creates and optionally runs a customizable Api Logic Project',
        ''
    ]

    for each_line in header:
        sys.stdout.write(each_line + '\n')

    for each_line in expose_existing_callable.uri_info:
        sys.stdout.write(each_line + '\n')
    sys.stdout.write('\n')


def print_args(args, msg):
    print(msg)
    for each_arg in args:
        print(f'  {each_arg}')
    print(" ")


def check_ports():
    try:
        rtn_hostname = socket.gethostname()
        rtn_local_ip = socket.gethostbyname(rtn_hostname)
    except:
        print(f"cannot get local ip from {rtn_hostname}")
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


def start():               # target of setup.py
    sys.stdout.write("\nWelcome to API Logic Server " + __version__ + "\n\n")
    hostname, local_ip = check_ports()  #  = socket.gethostname()
    # sys.stdout.write("    SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html\n")
    main(obj={})


command = "not set"
if __name__ == '__main__':  # debugger & python command line start here
    # eg: python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project
    # unix: python api_logic_server_cli/cli.py create --project_name=/home/ApiLogicProject

    print(f'\nWelcome to API Logic Server, {__version__}\n')  #  at {local_ip} ')
    hostname, local_ip = check_ports()
    commands = sys.argv
    if len(sys.argv) > 1 and sys.argv[1] not in ["version", "sys-info", "welcome"] and \
            "show-args" in api_logic_server_info_file_dict:
        print_args(commands, f'\nCommand Line Arguments:')
    main()


def key_module_map():
    """ not called - just index of key code - use this for hover, goto etc 
        ctl-l (^l) for last edit
    """
    import create_from_model.ui_admin_creator as ui_admin_creator
    import create_from_model.api_expose_api_models_creator as api_expose_api_models_creator
    import sqlacodegen_wrapper.sqlacodegen_wrapper as sqlacodegen_wrapper

    api_logic_server()                                  # main driver, calls...
    create_project_with_nw_samples()                    # clone project, overlay nw
    model_creation_services = ModelCreationServices()   # creates resource_list (python db model); ctor calls...
    def and_the_ctor_calls():
        sqlacodegen_wrapper.create_models_py({})        # creates models.py via sqlacodegen
        model_creation_services.create_resource_list()  # creates resource_list via dynamic import of models.py
    invoke_creators(model_creation_services)            # creates api & ui, via create_from_model...
    api_expose_api_models_creator.create()              # creates api/expose_api_models.py, key input to SAFRS        
    ui_admin_creator.create()                           # creates ui/admin/admin.yaml from resource_list
    get_abs_db_url()                                    # nw set here, dbname