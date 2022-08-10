# -*- coding: utf-8 -*-

import subprocess, os
from pathlib import Path


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return str(parent_path)


def replace_string_in_file(search_for: str, replace_with: str, in_file: str):
    with open(in_file, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace(search_for, replace_with)
    with open(in_file, 'w') as file:
        file.write(file_data)


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
        print(f'{log_msg} {cmd}')
    if new_line:
        print("")

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
        result_b = subprocess.check_output(cmd, shell=True) # , stderr=subprocess.STDOUT)  # causes hang on docker
    result = str(result_b)  # b'pyenv 1.2.21\n'  # this code never gets reached...
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    if msg == "no-msg":
        pass
    elif result != "" and result != "Downloaded the skeleton app, good coding!":
        print(f'{log_msg} {cmd} result: {spaces}{result}')
    return result
