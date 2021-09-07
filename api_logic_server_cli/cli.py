# -*- coding: utf-8 -*-
"""
Given a database url,
create ApiLogicServer project by cloning prototype,
in particular create the ui/basic_web_app/app/views.py
and api/expose_api_models.

See: main driver

"""

__version__ = "3.00.00"
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

dup_code = False
if not dup_code:
    pass
else:
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    python_path_container = python_path.parent.absolute()
    or_this_path = get_api_logic_server_dir()
    debug_path = True
    if debug_path:
        print(f'\trunning_at:\t\t\t{running_at}'
              f'\n\tpython_path:\t\t\t{python_path}'
              f'\n\tpython_path_container:\t{python_path_container}'
              f'\n\tor_this_path:\t\t{or_this_path}')

sys.path.append(get_api_logic_server_dir())  # e.g, on Docker -- export PATH=" /home/app_user/api_logic_server_cli"

from create_from_model.model_creation_services import CreateFromModel

import expose_existing.expose_existing_callable as expose_existing_callable
import create_from_model.api_logic_server_utils as create_utils

default_db = "<default -- nw.sqlite>"

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


def clone_prototype_project_with_nw_samples(project_directory: str, from_git: str, msg: str, abs_db_url: str) -> str:
    """
    clone prototype to create and remove git folder

    if nw, Append logic/logic_bank.py with pre-defined...

    :param project_directory: name of project created
    :param from_git: name of git project to clone (blank for default)
    :param abs_db_url: non-relative location of db
    :return: abs_db_url (e.g., reflects sqlite copy)
    """
    cloned_from = from_git
    remove_project_debug = True
    if remove_project_debug:
        delete_dir(realpath(project_directory), "1.")

    if from_git.startswith("https://"):
        cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project_directory
        cmd = f'git clone --quiet {from_git} {project_directory}'
        result = create_utils.run_command(cmd, msg=msg)  # "2. Create Project")
        delete_dir(f'{project_directory}/.git', "3.")
    else:
        from_dir = from_git
        if from_dir == "":
            code_loc = str(get_api_logic_server_dir())
            if "\\" in code_loc:
                from_dir = code_loc + "\\project_prototype"
            else:
                from_dir = code_loc + "/project_prototype"
        print(f'{msg} copy {from_dir} -> {project_directory}')
        cloned_from = from_dir
        shutil.copytree(from_dir, project_directory)

    create_utils.replace_string_in_file(search_for="creation-date",
                           replace_with=str(datetime.datetime.now()),
                           in_file=f'{project_directory}/readme.md')
    create_utils.replace_string_in_file(search_for="cloned-from",
                           replace_with=cloned_from,
                           in_file=f'{project_directory}/readme.md')

    project_directory_actual = os.path.abspath(project_directory)  # make path absolute, not relative (no /../)
    target_db_loc_actual = abs_db_url
    copy_sqlite = True
    if copy_sqlite == False or "sqlite" not in abs_db_url:
        db_uri = get_windows_path_with_slashes(abs_db_url)
        create_utils.replace_string_in_file(search_for="replace_db_url",
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
        target_db_loc_actual = db_uri
        create_utils.replace_string_in_file(search_for="replace_db_url",
                               replace_with=db_uri,
                               in_file=f'{project_directory}/config.py')
        api_config_file_name = \
            os.path.dirname(os.path.realpath(__file__)) +"/create_from_model/templates/api_config.txt"
        with open(api_config_file_name, 'r') as file:
            api_config = file.read()
        create_utils.insert_lines_at(lines=api_config,
                                     at="override SQLALCHEMY_DATABASE_URI here as required",
                                     file_name=f'{project_directory}/config.py')

        print(f'.. ..Copied sqlite db to: {target_db_loc_actual} and '
              f'updated db_uri in {project_directory}/config.py')


    if abs_db_url.endswith("nw.sqlite"):
        print(".. ..Append logic/logic_bank.py with pre-defined nw_logic, rpcs")
        replace_logic_with_nw_logic(project_directory)
        replace_models_ext_with_nw_models_ext(project_directory)
        replace_expose_rpcs_with_nw_expose_rpcs(project_directory)
        replace_server_startup_test_with_nw_server_startup_test(project_directory)
    return target_db_loc_actual


def create_basic_web_app(db_url, project_name, msg):  # remove
    project_abs_path = abspath(project_name)
    fab_project = project_abs_path + "/ui/basic_web_app"
    cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
    result = create_utils.run_command(cmd, msg=msg)
    pass


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
        code_gen_args = get_codegen_args()
        expose_existing_callable.codegen(code_gen_args)
        pass


def write_expose_api_models(project_name, apis):
    text_file = open(project_name + '/api/expose_api_models.py', 'a')
    text_file.write(apis)
    text_file.close()


def update_api_logic_server_run(project_name, project_directory, host, port):
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
                           replace_with="ApiLogicServer generated at:" + str(datetime.datetime.now()),
                           in_file=api_logic_server_run_py)
    project_directory_fix = project_directory_actual
    if os.name == "nt":  # windows
        project_directory_fix = get_windows_path_with_slashes(str(project_directory_actual))
    create_utils.replace_string_in_file(search_for="\"api_logic_server_project_dir\"",  # for logging project location
                           replace_with='"' + project_directory_fix + '"',
                           in_file=api_logic_server_run_py)
    create_utils.replace_string_in_file(search_for="api_logic_server_host",  # server host
                           replace_with=host,
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


def replace_logic_with_nw_logic(project_name):
    """ Replace logic/logic_bank.py with pre-defined nw_logic """
    logic_file = open(project_name + '/logic/logic_bank.py', 'w')
    nw_logic_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_logic.py")
    nw_logic = nw_logic_file.read()
    logic_file.write(nw_logic)
    logic_file.close()


def replace_models_ext_with_nw_models_ext(project_name):
    """ Replace models/models_ext.py with pre-defined nw_models_ext """
    models_ext_file = open(project_name + '/database/models_ext.py', 'w')
    nw_models_ext_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_models_ext.py")
    nw_models_ext = nw_models_ext_file.read()
    models_ext_file.write(nw_models_ext)
    models_ext_file.close()


def replace_expose_rpcs_with_nw_expose_rpcs(project_name):
    """ replace api/expose_rpcs with nw version """
    rpcs_file = open(project_name + '/api/expose_services.py', 'w')
    nw_expose_rpcs_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_expose_services.py")
    nw_expose_rpcs = nw_expose_rpcs_file.read()
    rpcs_file.write(nw_expose_rpcs)
    rpcs_file.close()


def replace_server_startup_test_with_nw_server_startup_test(project_name):
    """ replace api/expose_rpcs with nw version """
    tests_file = open(project_name + '/test/server_startup_test.py', 'w')
    nw_tests_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_server_startup_test.py")
    nw_tests_file_data = nw_tests_file.read()
    tests_file.write(nw_tests_file_data)
    tests_file.close()


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


def fix_basic_web_app_run__python_path(project_directory):  # TODO remove these 2
    """ overwrite ui/basic_web_app/run.py (enables run.py) with logic_bank_utils call to fixup python path """
    project_ui_basic_web_app_run_file = open(project_directory + '/ui/basic_web_app/run.py', 'w')
    ui_basic_web_app_run_file = open(os.path.dirname(os.path.realpath(__file__)) + "/ui_basic_web_app_run.py")
    ui_basic_web_app_run = ui_basic_web_app_run_file.read()  # standard content
    project_ui_basic_web_app_run_file.write(ui_basic_web_app_run)
    project_ui_basic_web_app_run_file.close()

    proj = os.path.basename(project_directory)
    create_utils.replace_string_in_file(search_for="api_logic_server_project_directory",
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

    create_utils.replace_string_in_file(search_for="/Users/val/dev/servers/classicmodels/",
                           replace_with=unix_project_name,
                           in_file=f'{unix_project_name}/ui/basic_web_app/create_admin.sh')


def fix_host_and_ports(msg, project_name, host, port):
    """ 9. Fixing port / host -- update server, port in /api/expose_services.py """
    print(msg)  # 9. Fixing port / host
    replace_port = f':{port}' if port else ""
    replace_with = host + replace_port
    in_file = f'{project_name}/api/expose_services.py'
    create_utils.replace_string_in_file(search_for="localhost:5000",
                           replace_with=replace_with,
                           in_file=in_file)
    print(f'.. ..Updated expose_services_py with port={port} and host={host}')
    full_path = os.path.abspath(project_name)
    create_utils.replace_string_in_file(search_for="python_anywhere_path",
                           replace_with=full_path,
                           in_file=f'{project_name}/python_anywhere_wsgi.py')
    print(f'.. ..Updated python_anywhere_wsgi.py with {full_path}')


def fix_database_models__inject_db_types(project_directory: str, db_types: str):
    """ insert <db_types file> into database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    if db_types != "":
        print(f'.. ..Injecting file {db_types} into database/models.py')
        with open(db_types, 'r') as file:
            db_types_data = file.read()
        create_utils.insert_lines_at(lines=db_types_data, at="(typically via --db_types)", file_name=models_file_name)


def fix_database_models__import_models_ext(project_directory: str):
    """ Append "from database import models_ext" to database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    print(f'7. Appending "from database import models_ext" to database/models.py')
    models_file = open(models_file_name, 'a')
    models_file.write("\n\nfrom database import models_ext\n")
    models_file.close()


def start_open_with(open_with: str, project_name: str):
    """ Creation complete.  Opening {open_with} at {project_name} """
    print(f'\nCreation complete - Opening {open_with} at {project_name}')
    print(".. See the readme for install / run instructions")
    create_utils.run_command(f'{open_with} {project_name}', None, "no-msg")


def copy_if_mounted(project_directory):
    """
    fab is unable to create-app in mounted path
    so, if mounted, create files in "created_project" and later copy to project_directory

    :param project_directory: name of project created
    :return: project_directory: name of project created (or "created_project"), copy_to_project (target copy when mounted, else "")
    """
    return_project_directory = project_directory
    return_copy_to_directory = ""
    if os.name == "posix":  # mac, docker...
        directory_is_mounted = project_directory.startswith("/local") or "copy_test" in project_directory
        if directory_is_mounted:  # TODO: https://www.baeldung.com/linux/bash-is-directory-mounted
            running_at =  Path(__file__)
            cli_path = running_at.parent.absolute()
            root_path = cli_path.parent.absolute()
            return_project_directory = str(root_path) + f'/{temp_created_project}'
            return_copy_to_directory = project_directory
    return return_project_directory, return_copy_to_directory


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

def print_options(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                  from_git: str, db_types: str, open_with: str, run: bool, use_model: str,
                  flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin:bool,
                  extended_builder: str):
    """ Creating ApiLogicServer with options:"""
    print_options = True
    if print_options:
        print(f'\n\nCreating ApiLogicServer with options:')
        print(f'  --db_url={db_url}')
        print(f'  --project_name={project_name}')
        print(f'  --react_admin={react_admin}')
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


def invoke_creators(model_creation_services: CreateFromModel):
    # spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")

    print("4. Create api/expose_api_models.py (import / iterate models)")
    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/api_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)  # runs "bare" module code (e.g., initialization)
    creator.create(model_creation_services)  # invoke create function

    print("5. Create ui/react_admin app (import / iterate models)")
    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/react_admin_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)
    creator.create(model_creation_services)

    print("6. Create ui/basic_web_app (import / iterate models)")
    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/fab_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)
    creator.create(model_creation_services)

    model_creation_services.app.teardown_appcontext(None)
    if model_creation_services.engine:
        model_creation_services.engine.dispose()


def api_logic_server(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin: bool,
                     extended_builder: str):

    """ Creates logic-enabled Python JSON_API project, options for FAB and execution - main driver """

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
    print_options(project_name = project_name, db_url=db_url, host=host, port=port, not_exposed=not_exposed,
                  from_git=from_git, db_types=db_types, open_with=open_with, run=run, use_model=use_model,
                  flask_appbuilder=flask_appbuilder, favorites=favorites, non_favorites=non_favorites,
                  react_admin=react_admin,
                  extended_builder=extended_builder)
    print(f"\nApiLogicServer {__version__} Creation Log:")

    abs_db_url = db_url
    if abs_db_url == "":
        abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
        print(f'0. Using demo default db_url: {abs_db_url}')
    if extended_builder == "*":
        extended_builder = abspath(f'{abspath(get_api_logic_server_dir())}/extended_builder.py')
        print(f'0. Using default extended_builder: {extended_builder}')
    if db_url.startswith('sqlite:///'):
        url = db_url[10: len(db_url)]
        abs_db_url = abspath(url)
        if db_url == "sqlite:///nw.sqlite":
            abs_db_url = f'{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
            print(f'0. Using dev demo default db_url: {abs_db_url}')
        abs_db_url = 'sqlite:///' + abs_db_url
        pass

    project_directory = resolve_home(project_name)
    """user-supplied project_name, less the twiddle. Typically relative to cwd. """

    project_directory, copy_to_project_directory = copy_if_mounted(project_directory)
    abs_db_url = clone_prototype_project_with_nw_samples(project_directory, from_git, "2. Create Project", abs_db_url)

    print(f'3. Create {project_directory + "/database/models.py"} via expose_existing_callable / sqlacodegen: {abs_db_url}')
    create_models(abs_db_url, project_directory, use_model)  # exec's sqlacodegen
    fix_database_models__inject_db_types(project_directory, db_types)

    # print("4. Create api/expose_api_models.py (import / iterate models)")
    model_creation_services = CreateFromModel(  # Create views.py file from db, models.py
        project_directory=project_directory, abs_db_url=abs_db_url, db_url=db_url,
        host=host, port=port,
        not_exposed=not_exposed + " ", flask_appbuilder = flask_appbuilder,
        favorite_names=favorites, non_favorite_names=non_favorites,
        react_admin=react_admin, version = __version__)
    invoke_creators(model_creation_services)
    if extended_builder is not None and extended_builder != "":
        print(f'7. Invoke extended_builder: {extended_builder}({db_url}, {project_directory})')
        invoke_extended_builder(extended_builder, db_url, project_directory)

    if use_model == "":
        fix_database_models__import_models_ext(project_directory)

    print(f'8. Update api_logic_server_run.py with '
          f'project_name={project_name} and host, port')
    update_api_logic_server_run(project_name, project_directory, host, port)

    fix_host_and_ports("9. Fixing api/expose_services - port, host", project_directory, host, port)

    if open_with != "":
        start_open_with(open_with=open_with, project_name=project_name)

    if run:
        run_file = os.path.abspath(f'{project_directory}/api_logic_server_run.py')
        create_utils.run_command(f'python {run_file} {host}',
                    msg="\nRun created ApiLogicServer project")  # sync run of server - does not return

    else:
        copy_project_result = ""
        if copy_to_project_directory != "":
            copy_project_result = \
                copy_project_to_local(project_directory, copy_to_project_directory,
                                      f'10. Copy temp_created_project over {copy_to_project_directory} ')
        print("\n\nApiLogicServer customizable project created.  Next steps:")
        print("\nFor Local install:")
        print(f'  cd {project_name}')
        print(f'  python api_logic_server_run.py')
        print(f'  python ui/basic_web_app/run.py')
        print("\nFor Docker container:")
        if project_directory.endswith("api_logic_server") or copy_project_result != "":
            print(f'  copy project to local machine, e.g. cp -r {project_directory}/. {copy_to_project_directory}/ ')
            # cp -r /Users/Shared/copy_test/. /Users/Shared/copy_test/
        print(f'  python {project_name}/api_logic_server_run.py')  # defaults to host 0.0.0.0
        print(f'  python {project_name}/ui/basic_web_app/run.py')  # defaults to host 0.0.0.0
        print("\n")


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
            "\t09/06/2021 - 03.00.00: Docker foundation with .vscode, improved Python path / log handling\n"
            "\t08/23/2021 - 02.03.06: Create react-admin app (tech exploration), cmdline debug fix\n"
            "\t07/22/2021 - 02.02.29: help command arg for starting APILogicServer / Basic Web App; SAFRS 2.11.5\n"
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
@click.option('--react_admin/--no-react_admin',
              default=True, is_flag=True,
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
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           favorites: str, non_favorites: str,
           extended_builder: str):

    db_types = ""
    if db_url == default_db:
        db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin,
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
@click.option('--react_admin/--no-react_admin',
              default=True, is_flag=True,
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
        react_admin: click.BOOL,
        use_model: str,
        host: str,
        port: str,
        favorites: str, non_favorites: str,
        extended_builder: str):

    db_types = ""
    if db_url == default_db:
        db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin,
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
        '  ApiLogicServer run --db_url=mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no',
        '  ApiLogicServer run --db_url=postgresql://postgres:p@10.0.0.234/postgres',
        '  ApiLogicServer run --db_url=postgresql+psycopg2://postgres:password@localhost:5432/postgres?options=-csearch_path%3Dmy_db_schema',
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

    print(f'\nWelcome to API Logic Server CLI Utility, {__version__}')
    print_info()
    commands = sys.argv
    if len(sys.argv) > 1 and sys.argv[1] != "version":
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print_args(commands, f'API Logic Server CLI Utility, '
                             f'version {__version__} at {local_ip} -- Command Line Arguments:')
    main()