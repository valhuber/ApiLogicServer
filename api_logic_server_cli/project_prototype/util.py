"""
Utilities for API Logic Server Projects (1.0)
"""
import sqlite3
from os import path
import logging
import sys
from typing import Any, Optional, Tuple
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_mapper
import flask_sqlalchemy
from logic_bank.rule_bank.rule_bank import RuleBank

app_logger = logging.getLogger(__name__)

def log(msg: object) -> None:
    app_logger.debug(msg)
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


def json_to_entities(from_row: str or object, to_row):
    """
    transform json object to SQLAlchemy rows, for save & logic

    :param from_row: json service payload: dict - e.g., Order and OrderDetailsList
    :param to_row: instantiated mapped object (e.g., Order)
    :return: updates to_row with contents of from_row (recursively for lists)
    """

    def get_attr_name(mapper, attr)-> Tuple[Optional[Any], str]:
        """ returns name, type of SQLAlchemy attr metadata object """
        attr_name = None
        attr_type = "attr"
        if hasattr(attr, "key"):
            attr_name = attr.key
        elif isinstance(attr, hybrid_property):
            attr_name = attr.__name__
        elif hasattr(attr, "__name__"):
            attr_name = attr.__name__
        elif hasattr(attr, "name"):
            attr_name = attr.name
        if attr_name == "OrderDetailListX" or attr_name == "CustomerX":
            print("Debug Stop")
        if isinstance(attr, sqlalchemy.orm.relationships.RelationshipProperty):   # hasattr(attr, "impl"):   # sqlalchemy.orm.relationships.RelationshipProperty
            if attr.uselist:
                attr_type = "list"
            else: # if isinstance(attr.impl, sqlalchemy.orm.attributes.ScalarObjectAttributeImpl):
                attr_type = "object"
        return attr_name, attr_type

    row_mapper = object_mapper(to_row)
    for each_attr_name in from_row:
        if hasattr(to_row, each_attr_name):
            for each_attr in row_mapper.attrs:
                mapped_attr_name, mapped_attr_type = get_attr_name(row_mapper, each_attr)
                if mapped_attr_name == each_attr_name:
                    if mapped_attr_type == "attr":
                        value = from_row[each_attr_name]
                        setattr(to_row, each_attr_name, value)
                    elif mapped_attr_type == "list":
                        child_from = from_row[each_attr_name]
                        for each_child_from in child_from:
                            child_class = each_attr.entity.class_
                            # eachOrderDetail = OrderDetail(); order.OrderDetailList.append(eachOrderDetail)
                            child_to = child_class()  # instance of child (e.g., OrderDetail)
                            json_to_entities(each_child_from, child_to)
                            child_list = getattr(to_row, each_attr_name)
                            child_list.append(child_to)
                            pass
                    elif mapped_attr_type == "object":
                        log("a parent object - skip (future - lookups here?)")
                    break

rule_count = 0
from flask import request, jsonify

def rules_report():
    """
    logs report of all rules, using rules_bank.__str__()
    """
    global rule_count
    rules_bank = RuleBank()
    logic_logger = logging.getLogger("logic_logger")
    rule_count = 0
    logic_logger.debug(f'\nThe following rules have been activated\n')
    list_rules = rules_bank.__str__()
    loaded_rules = list(list_rules.split("\n"))
    for each_rule in loaded_rules:
        logic_logger.info(each_rule + '\t\t##  ')
        rule_count += 1
    logic_logger.info(f'Logic Bank - {rule_count} rules loaded')


def server_log(request, jsonify):
    """
    Used by test/*.py - enables client app to log msg into server
    """
    import os
    import datetime
    from pathlib import Path
    import logging
    global rule_count


    def add_file_handler(logger, name: str, log_dir):
        """Add a file handler for this logger with the specified `name` (and
        store the log file under `log_dir`)."""
        # Format for file log
        for each_handler in logger.handlers:
            each_handler.flush()
            handler_name = str(each_handler)
            if "stderr" in handler_name:
                pass
                # print(f'do not delete stderr')
            else:
                logger.removeHandler(each_handler)
        fmt = '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s'
        formatter = logging.Formatter(fmt)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')

        # Determine log path/file name; create log_dir if necessary
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_name = f'{str(name).replace(" ", "_")}'  # {now}'
        if len(log_name) >= 26:
            log_name = log_name[0:25]

        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except:
                app_logger.info(f'util.add_file_handler unable to create dir {log_dir}')
                log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
                app_logger.info(f'Defaulting to {log_dir}.')

        log_file = os.path.join(log_dir, log_name) + '.log'
        if os.path.exists(log_file):
            os.remove(log_file)
        else:
            pass  # file does not exist

        # Create file handler for logging to a file (log all five levels)
        # print(f'create file handler for logging: {log_file}')
        logger.file_handler = logging.FileHandler(log_file)
        logger.file_handler.setLevel(logging.DEBUG)
        logger.file_handler.setFormatter(formatter)
        logger.addHandler(logger.file_handler)

    msg = request.args.get('msg')
    test = request.args.get('test')
    if test is not None and test != "None":
        if test == "None":
            print(f'None for msg: {msg}')
        logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
        # logic_logger.info("\n\nLOGIC LOGGER HERE\n")
        dir = request.args.get('dir')
        add_file_handler(logic_logger, test, Path(os.getcwd()).joinpath(dir))
    if msg == "Rules Report":
        rules_report()
        logic_logger.info(f'Logic Bank {__version__} - {rule_count} rules loaded')
    else:
        app_logger.info(f'{msg}')
    return jsonify({"result": f'ok'})


def format_nested_object(row
                , replace_attribute_tag: str = ""
                , remove_links_relationships: bool = False) -> dict:
    """
    Args:
        row (safrs.DB.Model): models instance (object + related objects)
        replace_attribute_tag (str): replace _attribute_ tag with this name
        remove_links_relationships (bool): remove these tags

    Example: in sample nw project, see customize_api: order()

    Returns:
        _type_: row suitable for safrs response (a dict)
    """

    row_as_dict = jsonify(row).json
    log(f'row_to_dict: {row_as_dict}')
    if replace_attribute_tag != "":
        row_as_dict[replace_attribute_tag] = row_as_dict.pop('attributes')
    if remove_links_relationships:
        row_as_dict.pop('links')
        row_as_dict.pop('relationships')
    return row_as_dict


def rows_to_dict(result: flask_sqlalchemy.BaseQuery) -> list:
    """
    Converts SQLAlchemy result (mapped or raw) to dict array of un-nested rows

    Args:
        result (object): list of serializable objects (e.g., dict)

    Returns:
        list of rows as dicts
    """
    rows = []
    for each_row in result:
        row_as_dict = {}
        log(f'type(each_row): {type(each_row)}')
        if isinstance (each_row, sqlalchemy.engine.row.Row):  # raw sql, eg, sample catsql
            key_to_index = each_row._key_to_index             # note: SQLAlchemy 2 specific
            for name, value in key_to_index.items():
                row_as_dict[name] = each_row[value]
        else:
            row_as_dict = each_row.to_dict()                  # safrs helper
        rows.append(row_as_dict)
    return rows


def sys_info():  
    """
    Print env and path
    """  
    import os, socket
    print("\n\nsys_info here")
    print("\nEnvironment Variables...")
    env = os.environ
    for each_variable in os.environ:
            print(f'.. {each_variable} = {env[each_variable]}')

    print("\nPYTHONPATH..")
    for p in sys.path:
        print(".." + p)
        
    print("")
    print(f'sys.prefix (venv): {sys.prefix}\n')

    print("")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = f"Warning - Failed local_ip = socket.gethostbyname(hostname) with hostname: {hostname}"

    print(f"hostname={hostname} on local_ip={local_ip}\n\n")
