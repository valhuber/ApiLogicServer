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


def expose_services(app, api, project_dir, HOST: str, PORT: str):
    """ extend model end points with new end points for services

    This sample illustrates the classic hello world,
    and a more interesting add_order.

     """

    @app.route('/hello_world')
    def hello_world():  # test it with: http://api_logic_server_host:api_logic_server_port/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})

    app_logger = logging.getLogger("api_logic_server_app")
    app_logger.info(f'\n*** Customizable ApiLogicServer project created -- '
             f'open it with your IDE at {project_dir}')
    app_logger.info(f'*** Server now running -- '
             f'explore sample data and API at http://{HOST}:{PORT}/')

    app_logger.info("api/expose_service.py - Exposing custom services")
    api.expose_object(ServicesEndPoint)
    app_logger.info("\n")


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

        util.json_to_entities(kwargs, new_order)  # generic function - any db object
        return {}  # automatic commit, which executes transaction logic
