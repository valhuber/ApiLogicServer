# -*- coding: utf-8 -*-

import subprocess, os, sys
from pathlib import Path
from os.path import abspath
from api_logic_server_cli.cli_args_project import Project
import logging

log = logging.getLogger(__name__)



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


def get_project_directory_and_api_name(project):
    """
    user-supplied project_name, less the tilde (which might be in project_name); typically relative to cwd.

    :param project_name: a file name, eg, ~/Desktop/a.b
    :param api_name: defaults to 'api'
    :param multi_api: cli arg - e.g., set by alsdock

    :return:
            rtn_project_directory -- /users/you/Desktop/a.b (removes the ~)

            rtn_api_name -- api_name, or last node of project_name if multi_api or api_name is "."

            rtn_merge_into_prototype -- preserve contents of current (".", "./") *prototype* project
    """

    rtn_project_directory = project.project_name    # eg, '../../servers/ApiLogicProject'
    rtn_api_name = project.api_name                 # typically api
    rtn_merge_into_prototype = False        
    if rtn_project_directory.startswith("~"):
        rtn_project_directory = str(Path.home()) + rtn_project_directory[1:]
    if rtn_project_directory == '.' or rtn_project_directory == './':
        rtn_project_directory = project.os_cwd
        rtn_merge_into_prototype = True
        msg = ''
        if rtn_project_directory == get_api_logic_server_dir():
            rtn_project_directory = str( Path(get_api_logic_server_dir()) / 'ApiLogicProject' )
            msg = ' <dev>'
        log.debug(f'1. Merge into project prototype: {rtn_project_directory}{msg}')
    project_path = Path(rtn_project_directory)
    project_path_last_node = project_path.parts[-1]
    if project.multi_api or project.api_name == ".":
        rtn_api_name = project_path_last_node
    return rtn_project_directory, \
        rtn_api_name, \
        rtn_merge_into_prototype

def get_abs_db_url(msg, project: Project):
    """
    non-relative db location - we work with this

    handle db_url abbreviations (nw, nw-, todo etc)

    but NB: we copy sqlite db to <project>/database - see create_project_with_nw_samples (below)

    also: compute physical nw db name (usually nw-gold) to be used for copy

    returns abs_db_url, nw_db_status - the real url (e.g., for nw), and whether it's really nw, and model_file_name
    """
    rtn_nw_db_status = ""  # presume not northwind
    rtn_abs_db_url = project.db_url

    # SQL/Server urls make VScode fail due to '?', so unfortunate work-around... (better: internalConsole)
    if rtn_abs_db_url.startswith('{install}'):
        install_db = str(Path(get_api_logic_server_dir()).joinpath('database'))
        rtn_abs_db_url = rtn_abs_db_url.replace('{install}', install_db)
    if rtn_abs_db_url.startswith('SqlServer-arm'):
        pass
    
    """
    per this: https://stackoverflow.com/questions/69950871/sqlalchemy-and-sqlite3-error-if-database-file-does-not-exist
    I would like to set URL like this to avoid creating empty db, but it fails
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file:/Users/val/dev/servers/ApiLogicProject/database/db.sqlite'  # ?mode=ro&uri=true'
    the file: syntax fails, though "current versions" should work:
    https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#uri-connections
    """

    if project.db_url in [project.default_db, "", "nw", "sqlite:///nw.sqlite"]:     # nw-gold:      default sample
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/nw-gold.sqlite"))}'
        rtn_nw_db_status = "nw"  # api_logic_server_dir_path
        log.debug(f'{msg} from: {rtn_abs_db_url}')  # /Users/val/dev/ApiLogicServer/api_logic_server_cli/database/nw-gold.sqlite
    elif project.db_url == "nw-":                                           # nw:           just in case
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/nw-gold.sqlite"))}'
        rtn_nw_db_status = "nw-"
    elif project.db_url == "nw--":                                           # nw:           unused - avoid
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/nw.sqlite"))}'
        rtn_nw_db_status = "nw-"
    elif project.db_url == "nw+":                                           # nw-gold-plus: next version
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/nw-gold-plus.sqlite"))}'
        rtn_nw_db_status = "nw+"
        log.debug(f'{msg} from: {rtn_abs_db_url}')
    elif project.db_url == "auth" or project.db_url == "authorization":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/authentication.sqlite"))}'
    elif project.db_url == "chinook":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/Chinook_Sqlite.sqlite"))}'
    elif project.db_url == "todo" or project.db_url == "todos":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/todos.sqlite"))}'
    elif  project.db_url == "new":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/new.sqlite"))}'
    elif  project.db_url == "table_filters_tests":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/table_filters_tests.sqlite"))}'
    elif project.db_url == "classicmodels":
        rtn_abs_db_url = f'sqlite:///{str(project.api_logic_server_dir_path.joinpath("database/classicmodels.sqlite"))}'
    elif project.db_url.startswith('sqlite:///'):
        url = project.db_url[10: len(project.db_url)]
        rtn_abs_db_url = abspath(url)
        rtn_abs_db_url = 'sqlite:///' + rtn_abs_db_url
    elif project.db_url.startswith('sqlsvr-sample'):  # work-around - VSCode run config arg parsing
        rtn_abs_db_url = 'mssql+pyodbc://sa:Posey3861@localhost:1433/SampleDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'
    elif project.db_url.startswith('sqlsvr-nwlogic'):  # work-around - VSCode run config arg parsing
        rtn_abs_db_url = 'mssql+pyodbc://sa:Posey3861@localhost:1433/nwlogic?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'
    elif project.db_url.startswith('sqlsvr-nw'):  # work-around - VSCode run config arg parsing
        rtn_abs_db_url = 'mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'
    model_file_name = "models.py"
    if project.bind_key != "":
        model_file_name = project.bind_key + "_" + "models.py"
    return rtn_abs_db_url, rtn_nw_db_status, model_file_name


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return str(parent_path)


def does_file_contain(search_for: str, in_file: str) -> bool:
    """ returns True if <search_for> is <in_file> """
    with open(in_file, 'r+') as fp:
        file_lines = fp.readlines()  # lines is list of lines, each element '...\n'
        found = False
        insert_line = 0
        for each_line in file_lines:
            if search_for in each_line:
                found = True
                break
        return found

def replace_string_in_file(search_for: str, replace_with: str, in_file: str):
    with open(in_file, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace(search_for, replace_with)
    with open(in_file, 'w') as file:
        file.write(file_data)


def insert_lines_at(lines: str, at: str, file_name: str, after: bool = False):
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
        if after:
            insert_line = insert_line + 1
        file_lines.insert(insert_line, lines)  # you can use any index if you know the line index
        fp.seek(0)  # file pointer locates at the beginning to write the whole file again
        fp.writelines(file_lines)  # write whole list again to the same file


def find_valid_python_name() -> str:
    '''
        sigh.  On *some* macs, python fails so we must use python3.
        
        return 'python3' in this case
    '''
    python3_worked = False
    try:
        result_b = subprocess.check_output('python --version', shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        python3_worked = False
        try:
            result_b = subprocess.check_output('python3 --version', shell=True, stderr=subprocess.STDOUT)
        except Exception as e1:
            python3_worked = False
        python3_worked = True
    if python3_worked:
        return "python3"
    else:
        return "python"


def run_command(cmd: str, env=None, msg: str = "", new_line: bool=False) -> str:
    """ run shell command

    :param cmd: string of command to execute
    :param env:
    :param msg: optional message (no-msg to suppress)
    :return:
    """
    if cmd.startswith('python'):
        valid_python_name = find_valid_python_name()
        cmd = cmd.replace("python", valid_python_name)
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    if msg == "no-msg":
        log_msg = ""
    else:
        log.debug(f'{log_msg} {cmd}')
    if new_line:
        log.debug("")

    use_env = env
    if env is None:
        project_dir = get_api_logic_server_dir()
        python_path = str(project_dir) + "/venv/lib/python3.9/site_packages"
        use_env = os.environ.copy()
        # log.debug("\n\nFixing env for cmd: " + cmd)
        if hasattr(use_env, "PYTHONPATH"):
            use_env["PYTHONPATH"] = python_path + ":" + use_env["PYTHONPATH"]  # eg, /Users/val/dev/ApiLogicServer/venv/lib/python3.9
            # log.debug("added PYTHONPATH: " + str(use_env["PYTHONPATH"]))
        else:
            use_env["PYTHONPATH"] = python_path
            # log.debug("created PYTHONPATH: " + str(use_env["PYTHONPATH"]))
    use_env_debug = False  # not able to get this working
    if use_env_debug:
        result_b = subprocess.check_output(cmd, shell=True, env=use_env)
    else:
        result_b = subprocess.check_output(cmd, shell=True) # , stderr=subprocess.STDOUT)  # causes hang on docker
    result = str(result_b)  # b'pyenv 1.2.21\n'  # this code never gets reached...
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    if msg == "no-msg":
        pass
    elif result != "" and result != "Downloaded the skeleton app, good coding!":
        log.debug(f'{log_msg} {cmd} result: {spaces}{result}')
    return result
