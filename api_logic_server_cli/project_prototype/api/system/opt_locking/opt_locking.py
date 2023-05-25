import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging

import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy import event
from safrs import SAFRSBase

from config import OptLocking
from config import Config

logger = logging.getLogger(__name__)

def opt_locking_setup(session):
    """
    Listen_for read events - set rows' CheckSum property for optimistic locking

    Called at Server start (api_logic_server_run)...
    """
    @event.listens_for(session, 'loaded_as_persistent')
    def receive_loaded_as_persistent(session, instance):
        "listen for the 'loaded_as_persistent' (get) event - set CheckSum"
        checksum_value = checksum_row(instance)
        logger.debug(f'checksum_value: {checksum_value}')
        setattr(instance, "_check_sum_property", checksum_value)

def checksum(list_arg: list) -> int:
    """
    Args:
        list_arg (list): list of (rows') attribute values

    Returns:
        int: hash(list values), with special handling for None
    """
    real_tuple = []
    skip_none = True  # work-around for non-repeatable hash(None)
    if skip_none:     # https://bugs.python.org/issue19224
        real_tuple = []
        for each_entry in list_arg:
            if each_entry is None:
                real_tuple.append(13)
            else:
                real_tuple.append(each_entry)
    result = hash(tuple(real_tuple))
    # print(f'checksum[{result}] from row: {list_arg})')
    return result

def checksum_row(row: object) -> int:
    """
    Args:
        row (object): SQLAlchemy row

    Returns:
        int: hash(row attributes), using checksum()
    """
    inspector = inspect(row)
    mapper = inspector.mapper
    iterate_properties = mapper.iterate_properties
    attr_list = []
    for each_property in iterate_properties:
        logger.debug(f'row.property: {each_property} <{type(each_property)}>')
        if isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(row, each_property.class_attribute.key))
    return_value = checksum(attr_list)
    inspector_class = inspector.mapper.class_ 
    logger.debug(f'checksum_row (get) [{return_value}], inspector: {inspector}')
    return return_value

def checksum_old_row(logic_row_old: object) -> int:
    """
    Args:
        logic_row_old (object): old_row (from LogicBank via declare_logic)

    Returns:
        int: hash(old_row attributes), using checksum()
    """
    attr_list = []
    for each_property in logic_row_old.keys():
        logger.debug(f'old_row.property: {each_property} <{type(each_property)}>')
        if True:  # isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(logic_row_old, each_property))
    return_value = checksum(attr_list)
    logger.debug(f'checksum_old_row [{return_value}] -- seeing -4130312969102546939 (vs. get: -4130312969102546939-4130312969102546939)')
    return return_value


def opt_lock_patch(logic_row: LogicRow):
    """
    Called by logic/declare_logic in early (before logic) event for updates (patch)

    Compares as_read_checksum to old_row_checksum, to determine whether row changed since read
    
    - as_read_checksum is submitted in patch by client, from initial get (see receive_loaded_as_persistent)
    - old_row_checksum is provided by Logicbank - it's the current row on disk

    Args:
        logic_row (LogicRow): LogicBank row being updated

    Raises:
        Exception: "Sorry, row altered by another user - please note changes, cancel and retry"
        Exception: "Optimistic Locking error - required CheckSum not present"
    """
    logger.debug(f'Opt Lock Patch')
    if hasattr(logic_row.row, "CheckSum"):
        as_read_checksum = logic_row.row.CheckSum
        if as_read_checksum != "!opt_locking_is_patch":
            old_row_checksum = checksum_old_row(logic_row.old_row)
            if as_read_checksum != old_row_checksum:
                logger.info(f"optimistic lock failure - as-read vs current: {as_read_checksum} vs {old_row_checksum}")
                raise Exception("Sorry, row altered by another user - please note changes, cancel and retry")
    else:
        if Config.OPT_LOCKING == OptLocking.OPTIONAL.value:
            logger.debug(f'No CheckSum -- ok, configured as optional')
        else:
            raise Exception("Optimistic Locking error - required CheckSum not present")
