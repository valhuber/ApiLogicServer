import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging

import sqlalchemy
from sqlalchemy import inspect
from safrs import SAFRSBase

logger = logging.getLogger(__name__)


def checksum(list_arg: list) -> int:

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
    print(f'checksum[{result}] from row: {list_arg})')
    return result


def checksum_row(row: object) -> int:
    inspector = inspect(row)
    mapper = inspector.mapper
    iterate_properties = mapper.iterate_properties
    attr_list = []
    for each_property in iterate_properties:
        print(f'row.property: {each_property} <{type(each_property)}>')
        if isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(row, each_property.class_attribute.key))
    return_value = checksum(attr_list)
    inspector_class = inspector.mapper.class_ 
    print(f'checksum_row (get) [{return_value}], inspector: {inspector}')
    return return_value  # eg. 6785985870086950264


def checksum_old_row(logic_row_old: object) -> int:
    attr_list = []
    for each_property in logic_row_old.keys():
        print(f'old_row.property: {each_property} <{type(each_property)}>')
        if True:  # isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(logic_row_old, each_property))
    return_value = checksum(attr_list)
    print(f'checksum_old_row [{return_value}] -- seeing -4130312969102546939 (vs. get: -4130312969102546939-4130312969102546939)')
    return return_value  # eg. -4130312969102546939 (get: -4130312969102546939)


def opt_locking_setup(session):
    pass

    from sqlalchemy import event

    @event.listens_for(session, 'loaded_as_persistent')
    def receive_loaded_as_persistent(session, instance):
        "listen for the 'loaded_as_persistent' (get) event - set CheckSum"

        # would be unconditional when models *all* have CheckSum
        if isinstance(instance, models.Department):
            logger.debug(f'{__name__} - hello there DEPT instance: {instance}')
            checksum_value = checksum_row(instance)
            print(f'checksum_value: {checksum_value}')
            setattr(instance, "_check_sum_property", checksum_value)
        elif isinstance(instance, models.Employee):
            logger.debug(f'{__name__} - setting CheckSum in EMP instance: {instance}')
            setattr(instance, "_chx_sum_property", 155)
            setattr(instance, "_check_sum_property", 55)
            setattr(instance, "_check_mix_property", 25)
            checksum_value = checksum_row(instance)
            print(f'setting CheckSum value (via setter): {checksum_value}')
            setattr(instance, "_check_sum_property", checksum_value)
        elif isinstance(instance, models.Category):
            checksum_value = checksum_row(instance)
            print(f'checksum_value: {checksum_value}')
            setattr(instance, "_check_sum_property", checksum_value)
            if getattr(instance, "Id") == 8:
                logger.debug(f'{__name__} - setting Description in Category instance: {instance}')
                setattr(instance, "Description", None)
        elif isinstance(instance, models.Order):
            checksum_value = checksum_row(instance)
            setattr(instance, "_check_sum_property", checksum_value)
            print(f'checksum_value: {checksum_value}')
        else:
            # todo discuss why SO many calls
            # logger.debug(f'{__name__} - hello there instance: {instance}')
            pass

from config import OptLocking
from config import Config

def opt_lock_patch(logic_row: LogicRow):
    logger.debug(f'Opt Lock Patch')
    if hasattr(logic_row.row, "CheckSum"):
        as_read_checksum = logic_row.row.CheckSum
        current_checksum = checksum_old_row(logic_row.old_row)
        assert as_read_checksum == current_checksum,\
            f"optimistic lock failure - as-read vs current: {as_read_checksum} vs {current_checksum}"
    else:
        if Config.OPT_LOCKING == OptLocking.OPTIONAL.value:
            logger.debug(f'No CheckSum -- ok, configured as optional')
        else:
            raise Exception("Optimistic Locking error - required CheckSum not present")
