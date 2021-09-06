import logging

import util
from typing import List

import safrs
import sqlalchemy
from flask import request, jsonify
from safrs import jsonapi_rpc, SAFRSAPI
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_mapper

from database import models
from database.db import Base

# called by expose_api_models.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated


def expose_services(app, api, project_dir):

    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost:5000/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#customize-api

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})

    app_logger = logging.getLogger("api_logic_server_app")
    app_logger.info(f'\n*** Customizable ApiLogicServer project created -- '
             f'open it with your IDE at {project_dir}')
    app_logger.info(f'*** Server now running -- '
             f'explore with OpenAPI (Swagger) at http://localhost:5000/')

    app_logger.info("api/expose_service.py - Exposing custom services")
    api.expose_object(ServicesEndPoint)
    app_logger.info("\n")


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


class ServicesEndPoint(safrs.JABase):
    """
    Illustrate custom service
    Quite small, since transaction logic comes from shared rules
    """

    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def add_order(self, *args, **kwargs):  # yaml comment => swagger description
        """ # yaml creates Swagger description
            args :
                CustomerId: ALFKI
                EmployeeId: 1
                Freight: 10
                OrderDetailList :
                  - ProductId: 1
                    Quantity: 1
                    Discount: 0
                  - ProductId: 2
                    Quantity: 2
                    Discount: 0
        """

        # test using swagger -> try it out (includes sample data, above)

        db = safrs.DB         # Use the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        new_order = models.Order()
        session.add(new_order)

        json_to_entities(kwargs, new_order)  # generic function - any db object
        return {}  # automatic commit, which executes transaction logic
