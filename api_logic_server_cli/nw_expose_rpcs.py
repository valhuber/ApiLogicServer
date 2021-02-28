from typing import List

import safrs
import sqlalchemy
from flask import request, jsonify
from safrs import jsonapi_rpc, SAFRSAPI
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_mapper

from database import models
from database.db import Base


def expose_rpcs(app, api):
    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost:5000/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})

    api.expose_object(OrderRPC)
    print("RPCs exposed")

def get_attr_name(mapper, attr)-> str:
    """polymorhpism is for wimps - find the name
        returns None if bad name, or is collection, or is object
    """
    attr_name = None
    if hasattr(attr, "key"):
        attr_name = attr.key
    elif isinstance(attr, hybrid_property):
        attr_name = attr.__name__
    elif hasattr(attr, "__name__"):
        attr_name = attr.__name__
    elif hasattr(attr, "name"):
        attr_name = attr.name
    if attr_name == "Customerxx":
        print("Debug Stop")
    if hasattr(attr, "impl"):
        if attr.impl.collection:
            attr_name = None
        if isinstance(attr.impl, sqlalchemy.orm.attributes.ScalarObjectAttributeImpl):
            attr_name = None
    return attr_name


def copy_like_named_attrs(from_row: object, to_row: safrs.DB.Model):
    row_mapper = object_mapper(to_row)
    for each_attr_name in from_row:
        each_attr_name = get_attr_name(mapper=row_mapper, attr=each_attr_name)
        if each_attr_name is None:  # parent or child-list
            pass
        if hasattr(to_row, each_attr_name):
            attr = row_mapper.column_attrs
            if hasattr(attr, "impl"):
                if attr.impl.collection:
                    attr_name = None
                if isinstance(attr.impl, sqlalchemy.orm.attributes.ScalarObjectAttributeImpl):
                    attr_name = None

            if isinstance(getattr(to_row,each_attr_name), safrs.DB.Model):
                pass
            elif isinstance(getattr(to_row,each_attr_name), List):
                pass
            else:
                value = from_row[each_attr_name]
                setattr(to_row, each_attr_name, value)


class OrderRPC(models.Order):   # was experimenting with inheriting attrs - I see it's the args :

    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def add_order(self, *args, **kwargs):
        """
            args :
                product_id : 1
                test_arg: 2
        """

        """ test: POST to Order/add_order
        {
            "meta": {
                "method": "add_order",
                "args": {
                  "EmployeeId": 6,
                  "Freight": 10,
                  "OrderDetailList": [
                     {"ProductId": 1, "qty": 2},
                     {"ProductId": 2, "qty": 3}
                  ]
                }
            }
        }
        """
        # ok, can pass custom args, but what about a *list* of OrderDetails (5 hammers, 2 shovels)   <========
        print("adding ")  # POST /Order/add_order
        print(kwargs)
        db = safrs.DB  # User the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        assert session.autocommit == False
        session.begin()       # ERROR: A transaction is already begun.
        new_order = models.Order()  # immediately commits
        session.add(new_order)
        """  like this in LogicBank (not flask)
        session_maker = sqlalchemy.orm.sessionmaker()
        session_maker.configure(bind=engine)
        session = session_maker()
        """

        copy_like_named_attrs(kwargs, new_order)
        pass
        # ... add the order
        return {}
