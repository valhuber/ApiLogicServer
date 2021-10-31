import sqlite3
from os import path
import logging
import safrs
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_mapper

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


def json_to_entities(from_row: object, to_row: safrs.DB.Model):
    """
    transform json object to SQLAlchemy rows, for save & logic

    :param from_row: json service payload: dict - e.g., Order and OrderDetailsList
    :param to_row: instantiated mapped object (e.g., Order)
    :return: updates to_row with contents of from_row (recursively for lists)
    """

    def get_attr_name(mapper, attr)-> str:
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
                        print("a parent object - skip (future - lookups here?)")
                    break
