import sqlite3
from os import path
import sys
import logging

app_logger = logging.getLogger("api_logic_server_app")

def log(msg: any) -> None:
    app_logger.info(msg)
    # print("TIL==> " + msg)


def connection() -> sqlite3.Connection:
    ROOT: str = path.dirname(path.realpath(__file__))
    log(ROOT)
    _connection = sqlite3.connect(path.join(ROOT, "sqlitedata.db"))
    return _connection


def dbpath(dbname: str) -> str:
    ROOT: str = path.dirname(path.realpath(__file__))
    log('ROOT: '+ROOT)
    PATH: str = path.join(ROOT, dbname)
    log('DBPATH: '+PATH)
    return PATH
