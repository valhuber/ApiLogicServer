import os
import sys
from sqlalchemy.sql import text
from typing import List
import sqlalchemy

def log(msg: any) -> None:
    print(msg, file=sys.stderr)

log("server_tests 1.0")


def server_tests(host, port):
    """ called by api_logic_server_run.py, for any tests on server start
        args
            host - server host
            port - server port
    """
    log(f'\n\ntest.server_startup_test -- server_tests("{host}", "{port}"')
    pass
