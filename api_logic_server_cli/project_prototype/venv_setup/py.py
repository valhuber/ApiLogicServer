#!/usr/bin/env python
"""
quick view of python environment
"""

import os, sys
import subprocess
from pathlib import Path


def print_at(label: str, value: str):
    tab_to = 24 - len(label)
    spaces = ' ' * tab_to
    print(f'{label}: {spaces}{value}')


def show(cmd: str):
    try:
        result_b = subprocess.check_output(cmd, shell=True)
        result = str(result_b)  # b'pyenv 1.2.21\n'
        result = result[2: len(result)-3]
        print_at(cmd, result)
    except Exception as e:
        # print(f'Failed: {cmd} - {str(e)}')
        pass


def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    parent_path = python_path.parent.absolute()
    return str(parent_path)


def python_status():
    print(" ")
    print("\nPython Status here, 4.3\n")
    dir = get_api_logic_server_dir()
    test_env = "/workspaces/../home/api_logic_server/"
    if os.path.exists(test_env):
        dir = test_env
    sys.path.append(dir)  # e.g, on Docker -- export PATH=" /home/app_user/api_logic_server_cli"

    try:
        import api_logic_server_cli.cli as cli
    except Exception as e:
        cli = None
        pass
    command = "?"
    if sys.argv[1:]:
        if sys.argv[1] == "welcome":
            command = "welcome"
        elif sys.argv[1] == "sys-info":
            command = "sys-info"
        else:
            print("unknown command - using sys-info")
            command = "sys-info"

    if command == "sys-info":
        print("\nEnvironment Variables...")
        env = os.environ
        for each_variable in os.environ:
             print(f'.. {each_variable} = {env[each_variable]}')

        print("\nPYTHONPATH..")
        for p in sys.path:
            print(".." + p)
            
        print("")
        print(f'sys.prefix (venv): {sys.prefix}\n\n')


    import socket
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = f"cannot get local ip from {hostname}"
        print(f"{local_ip}")
    if cli:
        print_at('ApiLogicServer version', cli.__version__)
    else:
        print_at('ApiLogicServer version', f'*** ApiLogicServer not installed in this environment ***')
    if command == "sys-info":
        print_at('ip (gethostbyname)', local_ip)
        print_at('on hostname', hostname)
        print_at('python sys.version', sys.version)
    print("")
    print("Typical API Logic Server commands:")
    print("  ApiLogicServer create-and-run --project_name=/localhost/api_logic_server --db_url=")
    print("  ApiLogicServer run-api        --project_name=/localhost/api_logic_server")
    print("  ApiLogicServer run-ui         --project_name=/localhost/api_logic_server   # login admin, p")
    print("  ApiLogicServer sys-info")
    print("  ApiLogicServer version")
    print("")
    if command != "sys-info":
        print("For more information, use python py.py sys-info")
    print("")

if __name__ == '__main__':
    python_status()
