from pathlib import Path
import requests
import logging
import util
import subprocess
import socket

server_tests_enabled = True  # use True to invoke server_tests on server startup
app_logger = logging.getLogger("api_logic_server_app")

"""
    These are server tests for the default Sample DB.
    See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#customize-server-startup

    Disable this, above
"""

api_logic_server_summary = True  # Prints a banner


def prt(msg: any) -> None:
    app_logger.info(msg)


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
    svr_logger = logging.getLogger('safrs.safrs_init')
    save_level = svr_logger.getEffectiveLevel()
    svr_logger.setLevel(logging.FATAL)  # hide ugly (scary) stacktrace on startup

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    my_host = host
    if host == "0.0.0.0":  # see https://github.com/valhuber/ApiLogicServer/issues/19
        my_host = "localhost"

    if api_logic_server_summary:
        app_logger.info(f'\nAPILOGICSERVER SUMMARY')
        app_logger.info(f'======================\n')
        prt(f''
            f'1. CUSTOMIZABLE SERVER PROJECT CREATED\n'
            f'     .. Explore your project - open with IDE/Editor at {get_project_dir()}\n'
            f'2. SERVER STARTED on host: {hostname}, on ip (gethostbyname): {local_ip}\n'
            f'     .. Explore your API - Swagger at http://{my_host}:{port}\n'
            f'     .. Re-run it later - python api_logic_server_run.py\n'
            f'3. LOGIC enabled\n'
            f'     .. Declare it in {get_project_dir()}/logic/declare_logic.py\n'
            f'     .. E.g., see https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/nw_logic.py\n'
            f'4. BASIC WEB APP Created\n'
            f'     .. Start it: python ui/basic_web_app/run.py [host port]]\n'
            f'     .. Then, explore it - http://{my_host}:8080/ (login: admin, p)\n'
            f'     .. See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#3-explore-the-basic-web-app\n'
            f'\n'
            f'===> For more information, see https://github.com/valhuber/ApiLogicServer/wiki/Tutorial\n'
            f'\n'
            f'SUCCESSFUL SERVER START (ApiLogicServer Version {version}) - see ApiLogicServer Summary, above\n')

    svr_logger.setLevel(save_level)