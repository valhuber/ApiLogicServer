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

from logic_bank.rule_bank.rule_bank import RuleBank

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated


def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ Customize API - new end points for services

    This sample illustrates the classic hello world,
    and a more interesting add_order.

     """

    app_logger = logging.getLogger("api_logic_server_app")  # only for create-and-run, no?


    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost:5656/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        # app_logger.info(f'hello_world returning:  hello, {user}')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello, {user}'})


    @app.route('/stop')
    def stop():  # test it with: http://localhost:5656/stop?msg=API stop - Stop API Logic Server
        """
        Use this to stop the server from the Browser.

        See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """

        import os, signal

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })


    @app.route('/order')
    def order():
        """
        Illustrates:
            Returning a nested result set response
            Using SQLAlchemy to obtain data
            Restructuring row results to desired json (e.g., for tool such as Sencha)
        Test:
            http://localhost:5656/order?Id=10643
            curl -X GET "http://localhost:5656/order?Id=10643"

        """
        order_id = request.args.get('Id')
        db = safrs.DB         # Use the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        order = session.query(models.Order).filter(models.Order.Id == order_id).one()

        result_std_dict = util.row_to_dict(order
                                        , replace_attribute_tag='data'
                                        , remove_links_relationships=True)
        result_std_dict['data']['Customer_Name'] = order.Customer.CompanyName # eager fetch
        result_std_dict['data']['OrderDetailListAsDicts'] = []
        for each_order_detail in order.OrderDetailList:       # lazy fetch
            each_order_detail_dict = util.row_to_dict(row=each_order_detail
                                                    , replace_attribute_tag='data'
                                                    , remove_links_relationships=True)
            each_order_detail_dict['data']['ProductName'] = each_order_detail.Product.ProductName
            result_std_dict['data']['OrderDetailListAsDicts'].append(each_order_detail_dict)
        return result_std_dict


    @app.route('/server_log')
    def server_log():
        """
        Used by test/*.py - enables client app to log msg into server
        """
        return util.server_log(request, jsonify)
    
    app_logger.info("..api/expose_service.py, exposing custom services: hello_world, add_order")
    api.expose_object(ServicesEndPoint)


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
