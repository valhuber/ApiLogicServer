from pathlib import Path
import requests
import logging
import subprocess
import socket


def prt(msg: any) -> None:
    print(msg)


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
    pass

if __name__ == "__main__":
   # only to run when not called via 'import' here
   server_tests("localhost", "5656", "v0")