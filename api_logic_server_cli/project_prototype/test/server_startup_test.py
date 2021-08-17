from pathlib import Path
import requests
import logging
import util
import subprocess

server_tests_enabled = True  # use True to invoke server_tests on server startup

"""
    These are server tests for the default Sample DB.
    See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#customize-server-startup

    Disable this, above
"""

api_logic_server_summary = True  # Prints a banner


def prt(msg: any) -> None:
    util.log(f'{msg}')


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def server_tests(host, port, version):
    """ called by api_logic_server_run.py, for any tests on server start
        args
            host - server host
            port - server port
            version - ApiLogicServer version
    """

    if api_logic_server_summary:
        util.log(f'\nAPILOGICSERVER SUMMARY')
        util.log(f'======================\n')
        prt(f''
            f'1. CUSTOMIZABLE SERVER PROJECT CREATED\n'
            f'     .. Explore your project - open with IDE/Editor at {get_project_dir()}\n'
            f'2. SERVER STARTED\n'
            f'     .. Explore your API - Swagger at http://{host}:{port}\n'
            f'     .. Re-run it later - python api_logic_server_run.py\n'
            f'3. LOGIC enabled\n'
            f'     .. Explore it at {get_project_dir()}/logic/logic_bank.py\n'
            f'     .. E.g., see https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/nw_logic.py\n'
            f'4. BASIC WEB APP Created\n'
            f'     .. Start it: python ui/basic_web_app/run.py [host port]]\n'
            f'     .. Then, explore it - http://0.0.0.0:8080/ (login: admin, p)\n'
            f'     .. See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#3-explore-the-basic-web-app\n'
            f'\n'
            f'===> For more information, see https://github.com/valhuber/ApiLogicServer/wiki/Tutorial\n'
            f'\n'
            f'SUCCESSFUL SERVER START (ApiLogicServer Version {version}) - see ApiLogicServer Summary, above\n')
