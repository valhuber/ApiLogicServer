# -*- coding: utf-8 -*-
"""
Given a database url,
create ApiLogicServer project by cloning prototype,
in particular create the ui/basic_web_app/app/views.py
and api/expose_api_models.

See: main driver

"""

__version__ = "3.50.19"

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
from create_from_model.model_creation_services import CreateFromModel

import expose_existing.expose_existing_callable as expose_existing_callable
import create_from_model.api_logic_server_utils as create_utils


api_logic_server_info_file_name = get_api_logic_server_dir() + "/api_logic_server_info.yaml"
api_logic_server_info_file = open(api_logic_server_info_file_name)
api_logic_server_info_file_dict = yaml.load(api_logic_server_info_file, Loader=yaml.FullLoader)
api_logic_server_info_file.close()

last_created_project_name = api_logic_server_info_file_dict["last_created_project_name"]
default_db = "<default -- nw.sqlite>"
default_project_name = "api_logic_server"
default_fab_host = "localhost"
if os.path.exists('/home/api_logic_server'):  # docker?
    default_project_name = "/localhost/api_logic_server"
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


def recursive_overwrite(src, dest, ignore=None):
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
    so, if mounted, create files in "created_project" and later copy to project_directory

    :param project_directory: name of project created
    :return: project_directory: name of project created (or "created_project"), copy_to_project (target copy when mounted, else "")
    """
    return_project_directory = project_directory
    return_copy_to_directory = ""
    cwd = os.getcwd()
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


def clone_prototype_project_with_nw_samples(project_directory: str, project_name: str,
                                            from_git: str, msg: str,
                                            abs_db_url: str, nw_db_status: str) -> str:
    """
    clone prototype to  project directory, copy sqlite db, and remove git folder

    if nw/nw+, inject sample logic/declare_logic and api/customize_api.

    :param project_directory: name of project created
    :param project_name: actual user parameter (might have ~, .)
    :param from_git: name of git project to clone (blank for default)
    :param msg printed, such as Create Project
    :param abs_db_url: non-relative location of db
    :param nw_db_status one of ["", "nw", "nw+", "nw-"]
    :return: abs_db_url (e.g., reflects sqlite copy to project/database dir)
    """
    cloned_from = from_git
    remove_project_debug = True
    if remove_project_debug and project_name != ".":
        delete_dir(realpath(project_directory), "1.")

    from_dir = from_git
    if from_git.startswith("https://"):
        cmd = 'git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git ' + project_directory
        cmd = f'git clone --quiet {from_git} {project_directory}'
        result = create_utils.run_command(cmd, msg=msg)  # "2. Create Project")
        delete_dir(f'{project_directory}/.git', "3.")
    else:
        if from_dir == "":
            code_loc = str(get_api_logic_server_dir())
            from_dir = (Path(code_loc)).\
                joinpath('project_prototype')  # /Users/val/dev/ApiLogicServer/project_prototype
        print(f'{msg} copy {from_dir} -> {project_directory}')
        cloned_from = from_dir
        try:
            if project_name != ".":
                shutil.copytree(from_dir, project_directory)
            else:
                recursive_overwrite(from_dir, project_directory)
        except OSError as e:
            print(f'\n==>Error - unable to copy to {project_directory} -- see log below'
                  f'\n\n{str(e)}\n\n'
                  f'Suggestions:\n'
                  f'.. Verify the --project_name argument\n'
                  f'.. If you are using Docker, verify the -v argument\n\n')

    if nw_db_status in ["nw", "nw+"]:
        print(".. ..Append logic/declare_logic.py with pre-defined nw_logic, services")
        replace_readme_with_nw_readme(project_directory)
        replace_logic_with_nw_logic(project_directory)
        replace_customize_models_with_nw_customize_models(project_directory)
        replace_expose_rpcs_with_nw_expose_rpcs(project_directory)
        replace_server_test_with_nw_server_test(project_directory)

    create_utils.replace_string_in_file(search_for="creation-date",
                           replace_with=str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
                           in_file=f'{project_directory}/readme.md')
    create_utils.replace_string_in_file(search_for="api_logic_server_version",
                           replace_with=__version__,
                           in_file=f'{project_directory}/readme.md')
    create_utils.replace_string_in_file(search_for="api_logic_server_template",
                           replace_with=f'{from_dir}',
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

    return target_db_loc_actual


def create_basic_web_app(db_url, project_name, msg):  # remove
    project_abs_path = abspath(project_name)
    fab_project = project_abs_path + "/ui/basic_web_app"
    cmd = f'flask fab create-app --name {fab_project} --engine SQLAlchemy'
    result = create_utils.run_command(cmd, msg=msg)
    pass


def create_models(db_url: str, project: str, use_model: str, model_creation_services):
    """
    create model.py, normally via expose_existing.expose_existing_callable (sqlacodegen)

    or, use_model -- then just copy

    :param db_url:  the actual db_url (not relative, reflects sqlite [nw] copy)
    :param project: project dictory
    :param use_model: file name of existing models file ("" means create_models)
    :returns dict - key is table name, value is list of (role-name, relationship)
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
        codegen_args.model_creation_services = model_creation_services
        return codegen_args

    rtn_my_children_map = None
    rtn_my_parents_map = None
    if use_model != "":  # use this hand-edited model (e.g., added relns)
        model_file = resolve_home(use_model)
        print(f'.. .. ..Copy {model_file} to {project + "/database/models.py"}')
        copyfile(model_file, project + '/database/models.py')
    else:
        code_gen_args = get_codegen_args()
        rtn_my_children_map, rtn_my_parents_map = expose_existing_callable.codegen(code_gen_args)
        model_creation_services.resource_list_complete = True
        pass
    return rtn_my_children_map, rtn_my_parents_map


def write_expose_api_models(project_name, apis):
    text_file = open(project_name + '/api/expose_api_models.py', 'a')
    text_file.write(apis)
    text_file.close()


def replace_readme_with_nw_readme(project_name):
    """ Replace readme.md with pre-defined nw_readme """
    readme_file = open(project_name + '/readme.md', 'w')
    nw_readme_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_readme.md")
    nw_readme = nw_readme_file.read()
    readme_file.write(nw_readme)
    readme_file.close()


def replace_logic_with_nw_logic(project_name):
    """ Replace logic/declare_logic.py with pre-defined nw_logic """
    logic_file = open(project_name + '/logic/declare_logic.py', 'w')
    nw_logic_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_logic.py")
    nw_logic = nw_logic_file.read()
    logic_file.write(nw_logic)
    logic_file.close()


def replace_customize_models_with_nw_customize_models(project_name):
    """ Replace models/customize_models.py with pre-defined nw_customize_models """
    customize_models_file = open(project_name + '/database/customize_models.py', 'w')
    nw_customize_models_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_customize_models.py")
    nw_customize_models = nw_customize_models_file.read()
    customize_models_file.write(nw_customize_models)
    customize_models_file.close()


def replace_expose_rpcs_with_nw_expose_rpcs(project_name):
    """ replace api/expose_rpcs with nw version """
    rpcs_file = open(project_name + '/api/customize_api.py', 'w')
    nw_expose_rpcs_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_expose_services.py")
    nw_expose_rpcs = nw_expose_rpcs_file.read()
    rpcs_file.write(nw_expose_rpcs)
    rpcs_file.close()


def replace_server_test_with_nw_server_test(project_name):
    """ replace test/server_tests.py with nw version """
    tests_file = open(project_name + '/test/server_test.py', 'w')
    nw_tests_file = open(os.path.dirname(os.path.realpath(__file__)) + "/project_prototype_nw/nw_server_test.py")
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


def fix_database_models__inject_db_types(project_directory: str, db_types: str):
    """ injecting <db_types file> into database/models.py """
    models_file_name = f'{project_directory}/database/models.py'
    if db_types != "":
        print(f'.. .. ..Injecting file {db_types} into database/models.py')
        with open(db_types, 'r') as file:
            db_types_data = file.read()
        create_utils.insert_lines_at(lines=db_types_data, at="(typically via --db_types)", file_name=models_file_name)


def final_project_fixup(msg, project_name, project_directory, host, port, use_model, copy_to_project_directory) -> str:
    print(msg)  # "7. Final project fixup"

    if use_model == "" and command != "rebuild-from-model":
        msg = f' a.   Appending "from database import customize_models" to database/models.py'
        fix_database_models__import_customize_models(project_directory, msg)

    copy_project_result = ""
    if command.startswith("rebuild"):
        pass
    else:
        print(f' b.   Update api_logic_server_run.py with '
              f'project_name={project_name} and host, port')
        update_api_logic_server_run(project_name, project_directory, host, port)

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
                           replace_with="ApiLogicServer generated at:" +
                                        str(datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")),
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
    """ running docker?  path exists: /home/api_logic_server
    """
    path = '/home/api_logic_server'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def print_options(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                  from_git: str, db_types: str, open_with: str, run: bool, use_model: str, admin_app: bool,
                  flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin:bool,
                  extended_builder: str):
    """ Creating ApiLogicServer with options:"""
    print_options = True
    if print_options:
        print(f'\n\nCreating ApiLogicServer with options:')
        print(f'  --db_url={db_url}')
        print(f'  --project_name={project_name}')
        print(f'  --admin_app={admin_app}')
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
    """ uses model_creation_services (resource_list, model iterator functions) to create api, apps
    """

    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')

    print(" b.  Create api/expose_api_models.py from models")
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/api_expose_api_models.py')
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
        print(".. ..ui/basic_web_app creation declined")

    model_creation_services.close_app()  # this may no longer be required


def api_logic_server(project_name: str, db_url: str, host: str, port: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str, admin_app: bool,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin: bool,
                     extended_builder: str):
    """
    Creates logic-enabled Python JSON_API project, options for FAB and execution

    main driver

    :param project_name maybe ~, or volume - create this folder
    :param db_url SQLAlchemy url
    :param host where safrs finds the api
    :param port where safrs finds the port
    :param extended_builder python file invoked to augment project
    :returns: none
    """

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database/db.sqlite")+ '?check_same_thread=False'
    print_options(project_name = project_name, db_url=db_url, host=host, port=port, not_exposed=not_exposed,
                  from_git=from_git, db_types=db_types, open_with=open_with, run=run, use_model=use_model,
                  flask_appbuilder=flask_appbuilder, favorites=favorites, non_favorites=non_favorites,
                  react_admin=react_admin, admin_app=admin_app,
                  extended_builder=extended_builder)
    print(f"\nApiLogicServer {__version__} Creation Log:")

    nw_db_status = ""  # presume not northwind
    abs_db_url = db_url
    """ non-relative db location - we work with this (but NB: we copy sqlite db to <project>/database) """
    if db_url in [default_db, "", "nw", "sqlite:///nw.sqlite"]:
        abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
        nw_db_status = "nw"
    elif db_url == "nw-":
        abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw.sqlite'
        nw_db_status = "nw-"
    elif db_url == "nw+":
        abs_db_url = f'sqlite:///{abspath(get_api_logic_server_dir())}/project_prototype_nw/nw-gold-plus.sqlite'
        nw_db_status = "nw+"
    elif db_url.startswith('sqlite:///'):
        url = db_url[10: len(db_url)]
        abs_db_url = abspath(url)
        abs_db_url = 'sqlite:///' + abs_db_url

    if extended_builder == "*":
        extended_builder = abspath(f'{abspath(get_api_logic_server_dir())}/extended_builder.py')
        print(f'0. Using default extended_builder: {extended_builder}')

    project_directory = resolve_home(project_name)
    """user-supplied project_name, less the twiddle (which might be in project_name). Typically relative to cwd. """

    project_directory, copy_to_project_directory = copy_if_mounted(project_directory)
    if not command.startswith("rebuild"):
        abs_db_url = clone_prototype_project_with_nw_samples(project_directory, # no twiddle, resolve .
                                                             project_name,      # actual user parameter
                                                             from_git, "2. Create Project",
                                                             abs_db_url,        # sqlite DBs are copied to proj/database
                                                             nw_db_status)
    else:
        print("1. Not Deleting Existing Project")
        print("2. Using Existing Project")

    print(f'3. Create/verify database/models.py, then use that to create api/ and ui/ models')
    model_creation_services = CreateFromModel(  # Create database/models.py from db
        project_directory=project_directory,
        command = command,
        copy_to_project_directory = copy_to_project_directory,
        api_logic_server_dir = get_api_logic_server_dir(),
        abs_db_url=abs_db_url, db_url=db_url, nw_db_status=nw_db_status,
        host=host, port=port, use_model = use_model,
        not_exposed=not_exposed + " ", flask_appbuilder = flask_appbuilder, admin_app=admin_app,
        favorite_names=favorites, non_favorite_names=non_favorites,
        react_admin=react_admin, version = __version__)
    fix_database_models__inject_db_types(project_directory, db_types)
    invoke_creators(model_creation_services)  # creates api/expose_api_models, ui/admin & basic_web_app
    if extended_builder is not None and extended_builder != "":
        print(f'4. Invoke extended_builder: {extended_builder}({db_url}, {project_directory})')
        invoke_extended_builder(extended_builder, db_url, project_directory)

    copy_project_result = final_project_fixup("4. Final project fixup", project_name, project_directory, host, port,
                        use_model, copy_to_project_directory)

    if open_with != "":  # open project with open_with (vscode, charm, atom) -- NOT for docker!!
        start_open_with(open_with=open_with, project_name=project_name)

    if run:  # synchronous run of server - does not return
        # run_file = os.path.abspath(f'{project_directory}/api_logic_server_run.py')
        # create_utils.run_command(f'python {run_file} {host}', msg="\nRun created ApiLogicServer project")
        run_file = os.path.abspath(f'{resolve_home(project_name)}/api_logic_server_run.py')
        create_utils.run_command(f'python {run_file}', msg="\nRun created ApiLogicServer project")
    else:
        print("\n\nApiLogicServer customizable project created.  Next steps:")
        print("\nRun API Logic Server:")
        print(f'  ApiLogicServer run --project_name={project_name}')
        print(f'  python {project_name}/api_logic_server_run.py       # equivalent to above')
        print("\nRun basic web app:")
        print(f'  python {project_name}/ui/basic_web_app/run.py')
        if copy_project_result != "":  # or project_directory.endswith("api_logic_server")?
            print(f'  copy project to local machine, e.g. cp -r {project_directory}/. {copy_to_project_directory}/ ')
            # cp -r '/Users/val/dev/ApiLogicServer/temp_created_project'. /Users/Shared/copy_test/
        print(f'\nOpen IDE on local machine, see https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs  e.g., ')
        if (is_docker()):
            print(f'  exit  # exit the Docker container ')
        print(f'  code <project-name>')
        print("\n")  # api_logic_server  ApiLogicServer  SQLAlchemy


@click.group()
@click.pass_context
def main(ctx):
    """
    Creates and runs logic-enabled Python database api projects.

\b
    Doc: https://github.com/valhuber/ApiLogicServer/blob/main/README.md

\b
    Examples:

\b
        ApiLogicServer create         --project_name=/localhost/api_logic_server   --db_url=
        ApiLogicServer run            --project_name=/localhost/api_logic_server
        ApiLogicServer run-ui         --project_name=/localhost/api_logic_server   # login with: admin, p
        ApiLogicServer create-and-run --project_name=/localhost/api_logic_server   --db_url=
    """


@main.command("about")
@click.pass_context
def about(ctx):
    """
        Recent Changes, system information.
    """
    # print_info()
    print(f'\tInstalled at {abspath(__file__)}\n')
    print(f'\thttps://github.com/valhuber/ApiLogicServer/wiki/Tutorial\n')

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

    click.echo(
        click.style(
            f'\n\nRecent Changes:\n'
            "\t11/26/2021 - 03.50.19: default search for favorite attr, indicate on label, yaml url fix  \n"
            "\t11/25/2021 - 03.50.17: working search support in Config.js, admin chooser  \n"
            "\t11/25/2021 - 03.50.16: patch to work with WSL as workaround for https://bugs.python.org/issue38633  \n"
            "\t11/25/2021 - 03.50.15: folder rename - safrs-react-admin-npm-build, url for starting browser  \n"
            "\t11/24/2021 - 03.50.14: constraint retry, pathlib fix  \n"
            "\t11/23/2021 - 03.50.12: fix admin - resource type bug.  Parent & child joins, admin-attr  \n"
            "\t11/22/2021 - 03.50.11: fixed config.js, child grids work.  No parent joins  \n"
            "\t11/22/2021 - 03.50.10: upd build, web page default now admin (not swagger); detail grids still blank  \n"
            "\t11/21/2021 - 03.50.09: web page default now admin (not swagger); detail grids still blank  \n"
            "\t11/20/2021 - 03.50.08: safrs-admn join included, use table-name as resource-name; detail grids blank \n"
            "\t11/20/2021 - 03.50.07: admin.yaml loaded/used by admin app, runs directly *and* ApiLogicServer run \n"
            "\t11/19/2021 - 03.50.06: admin.yaml loaded/accepted by admin app, runs \n"
            "\t11/18/2021 - 03.50.05: creates runnable admin-col.yaml, doc & console log info \n"
            "\t11/16/2021 - 03.50.03: safrs-react-admin fixes \n"
            "\t11/15/2021 - 03.50.02: minor diagnostics \n"
            "\t11/13/2021 - 03.50.01: port conflict warning (not failure) for Docker \n"
            "\t11/13/2021 - 03.50.00: rebuild-from-database/model, improved relationship support \n"
            "\t11/04/2021 - 03.40.01: Per MacOS Monterey, default ports to 5001, 5002 \n"
            "\t10/18/2021 - 03.20.11: Readme Tutorial for IDE users \n"
            "\t10/16/2021 - 03.20.07: dev-network no longer required (reduce errors) \n"
            "\t09/29/2021 - 03.01.15: run (now just runs without create), added create-and-run \n"
            "\t09/25/2021 - 03.01.10: run command for Docker, pyodbc, fab create-by-copy, localhost swagger \n"
            "\t09/15/2021 - 03.00.09: auto-create .devcontainer for vscode, configure network, python & debug \n"
            "\t09/10/2021 - 03.00.02: rename logic_bank to declare_logic, improved logging\n"
        )
    )


@main.command("create")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=True, is_flag=True,
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
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def create(ctx, project_name: str, db_url: str, not_exposed: str,
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
           favorites: str, non_favorites: str,
           extended_builder: str):
    """
        Creates new customizable project (overwrites).
    """
    global command
    command = "create"
    # print_info()
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


@main.command("create-and-run")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create and run",
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=True, is_flag=True,
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
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def create_and_run(ctx, project_name: str, db_url: str, not_exposed: str,
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
        favorites: str, non_favorites: str,
        extended_builder: str):
    """
        Creates new project and runs it (overwrites).
    """
    global command
    command = "create-and-run"
    # print_info()
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


@main.command("rebuild-from-database")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=True, is_flag=True,
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
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def rebuild_from_database(ctx, project_name: str, db_url: str, not_exposed: str,
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
           favorites: str, non_favorites: str,
           extended_builder: str):
    """
        Updates database, api, and ui from changed db.

\b
        ex
\b
        ApiLogicServer rebuild-from-database --project_name=~/dev/servers/api_logic_server --db_url=nw

    """
    global command
    command = "rebuild-from-database"
    # print_info()
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


@main.command("rebuild-from-model")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
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
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=True, is_flag=True,
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
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.pass_context
def rebuild_from_model(ctx, project_name: str, db_url: str, not_exposed: str,
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
           favorites: str, non_favorites: str,
           extended_builder: str):
    """
        Updates database, api, and ui from changed models.
    """
    global command
    command = "rebuild-from-model"
    # print_info()
    db_types = ""
    api_logic_server(project_name=project_name, db_url=db_url,
                     not_exposed=not_exposed,
                     run=run, use_model=use_model, from_git=from_git, db_types = db_types,
                     flask_appbuilder=flask_appbuilder,  host=host, port=port,
                     react_admin=react_admin, admin_app=admin_app,
                     favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                     extended_builder=extended_builder)


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
@click.pass_context
def run_api(ctx, project_name: str, host: str="localhost", port: str="5656"):
    """
        Runs existing project.


\b
        Example

\b
            ApiLogicServer run --project_name=/localhost/api_logic_server
            ApiLogicServer run --project_name=    # runs last-created project
    """
    global command
    command = "run-api"
    proj_dir = project_name
    if proj_dir == "":
        proj_dir = last_created_project_name
    else:
        proj_dir = os.path.abspath(f'{resolve_home(project_name)}')
    run_file = f'{proj_dir}/api_logic_server_run.py {host} {port}'
    create_utils.run_command(f'python {run_file}', msg="Run created ApiLogicServer project", new_line=True)
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
    model_creation_services = CreateFromModel(  # fills in rsource_list for ui_admin_creator
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


@main.command("run-ui")
@click.option('--project_name',
              default=f'{last_created_project_name}',
              prompt="Project to run",
              help="Project to run")
@click.option('--host',
              default=f'{default_fab_host}',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5002',
              help="Port (default 5002, or leave empty)")
@click.pass_context
def run_ui(ctx, project_name: str, host: str="localhost", port: str="5002"):
    """
        Runs existing basic web app.

\b
        Example

\b
            ApiLogicServer run-ui --project_name=/localhost/api_logic_server
            ApiLogicServer run-ui --project_name=    # runs last-created project
    """
    global command
    command = "run-ui"
    proj_dir = project_name
    if proj_dir == "":
        proj_dir = last_created_project_name
    else:
        proj_dir = os.path.abspath(f'{resolve_home(project_name)}')
    run_file = f'{proj_dir}/ui/basic_web_app/run.py'   # this fails to open: {host} 8080
    create_utils.run_command(f'python {run_file} {host} {port}', msg="Run created ApiLogicServer Basic Web App", new_line=True)


@main.command("examples")
@click.pass_context
def examples(ctx):
    """
    Example commands, including SQLAlchemy URIs.
    """
    info = [
        'Examples:',
        '  ApiLogicServer create-and-run',
        '  ApiLogicServer create-and-run --db_url=sqlite:///nw.sqlite',
        '  ApiLogicServer create-and-run --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels '
        '--project_name=/localhost/docker_db_project',
        '  ApiLogicServer create-and-run --db_url=mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?'
        'driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no',
        '  ApiLogicServer create-and-run --db_url=postgresql://postgres:p@10.0.0.234/postgres',
        '  ApiLogicServer create-and-run --db_url=postgresql+psycopg2:'
        '//postgres:password@localhost:5432/postgres?options=-csearch_path%3Dmy_db_schema',
        '  ApiLogicServer create --host=ApiLogicServer.pythonanywhere.com --port=',
        '',
        'Where --db_url defaults to supplied sample, or, specify URI for your own database:',
        '   SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html',
        '   Other URI examples:           https://github.com/valhuber/ApiLogicServer/wiki/Testing',
        ' ',
        'Docs: https://github.com/valhuber/ApiLogicServer#readme\n'
    ]
    for each_line in info:
        print(each_line)

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
        '  ApiLogicServer create-and-run',
        '  ApiLogicServer create-and-run --db_url=sqlite:///nw.sqlite',
        '  ApiLogicServer create-and-run --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels '
        '--project_name=/localhost/docker_db_project',
        '  ApiLogicServer create-and-run --db_url=mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?'
        'driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no',
        '  ApiLogicServer create-and-run --db_url=postgresql://postgres:p@10.0.0.234/postgres',
        '  ApiLogicServer create-and-run --db_url=postgresql+psycopg2:'
        '//postgres:password@localhost:5432/postgres?options=-csearch_path%3Dmy_db_schema',
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


def check_ports():
    rtn_hostname = socket.gethostname()
    rtn_local_ip = socket.gethostbyname(rtn_hostname)
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
    sys.stdout.write("\nWelcome to API Logic Server " + __version__ + "\n")
    hostname, local_ip = check_ports()  #  = socket.gethostname()
    # sys.stdout.write("    SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html\n")
    # sys.stdout.write("    Other examples are at:        https://github.com/valhuber/ApiLogicServer/wiki/Testing\n\n")
    main(obj={})


command = "not set"
if __name__ == '__main__':  # debugger & python command line start here
    # eg: python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project
    # unix: python api_logic_server_cli/cli.py create --project_name=/home/api_logic_server

    print(f'\nWelcome to API Logic Server, {__version__}\n')  #  at {local_ip} ')
    hostname, local_ip = check_ports()
    commands = sys.argv
    if len(sys.argv) > 1 and sys.argv[1] not in ["version", "sys-info", "welcome"] and \
            "show-args" in api_logic_server_info_file_dict:
        print_args(commands, f'\nCommand Line Arguments:')
    main()


def key_module_map():
    """ not called - just index of key code - use this for hover, goto etc """
    import create_from_model.ui_admin_creator as ui_admin_creator
    import create_from_model.api_expose_api_models as api_expose_api_models

    api_logic_server()                                          # main driver, calls...
    model_creation_services = CreateFromModel()                 # creates database/models.py by calling...
    model_creation_services.create_models()                     # creates database/models.py
    model_creation_services.create_resource_list_from_safrs()   # creates resource_list via dynamic import of models.py
    invoke_creators()                                           # creates api, ui via create_from_model...
    api_expose_api_models.create()                              # creates api/expose_api_models from resource_list
    ui_admin_creator.create()                                   # creates ui/admin/admin.yaml from resource_list
