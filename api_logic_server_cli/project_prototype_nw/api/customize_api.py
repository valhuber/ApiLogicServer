from functools import wraps
import logging
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from config import Config
from security.system.authorization import Security
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

# Called by api_logic_server_run.py, to customize api (new end points, services -- see add_order).
# Separate from expose_api_models.py, to simplify merge if project recreated


def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ Customize API - new end points for services

    This sample illustrates
    * classic hello world,
    * a more interesting add_order,
    * and some endpoints illustrating SQLAlchemy usage (cats, order).

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


    def admin_required():
        """
        support option to bypass security (see cats, below).

        see https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
        """
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Config.SECURITY_ENABLED == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                return fn(*args, **kwargs)
            return decorator
        return wrapper


    @app.route('/cats')
    @admin_required()
    def cats():
        """
        Explore SQLAlchemy and/or filters.
        
        Test (returns rows 2-5):
            curl -X GET "http://localhost:5656/cats [no-filter | simple-filter]"
        """

        from sqlalchemy import and_, or_
        filter_type = request.args.get('filter')
        if filter_type is None:
            filter_type = "multiple filters"
        db = safrs.DB           # Use the safrs.DB, not db!
        session = db.session    # sqlalchemy.orm.scoping.scoped_session
        Security.set_user_sa()  # an endpoint that requires no auth header (see also @admin_required)

        if filter_type.startswith("n"):
            results = session.query(models.Category)    # .filter(models.Category.Id > 1)
        elif filter_type.startswith("s"):               # normally coded like this
            results = session.query(models.Category) \
                .filter(models.Category.Id > 1) \
                .filter(or_((models.Category.Client_id == 2), (models.Category.Id == 5)))
        else:                                           # simulate grant logic (multiple filters)
            client_grant = models.Category.Client_id == 2
            id_grant = models.Category.Id == 5
            grant_filter = or_( client_grant, id_grant)
            results = session.query(models.Category) \
                .filter(models.Category.Id > 1)  \
                .filter(grant_filter)
        return_result = []
        for each_result in results:
            row = { 'id': each_result.Id, 'name': each_result.CategoryName}
            return_result.append(row)
        return jsonify({ "success": True, "results":  return_result})


    @app.route('/order')
    def order():
        """
        Illustrates:
        * Returning a nested result set response
        * Using SQLAlchemy to obtain data
        * Restructuring row results to desired json (e.g., for tool such as Sencha)

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
    api.expose_object(CategoriesEndPoint)


class ServicesEndPoint(safrs.JABase):
    """
    Illustrate custom service - visible in swagger
    
    Quite small, since transaction logic comes from shared logic
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


class CategoriesEndPoint(safrs.JABase):
    """
    Illustrates swagger-visible RPC that requires authentication (@jwt_required()).

    Observe authorization is thus enforced.  Test in swagger --
    * Post to endpoint auth to obtain <access_token> value - copy it to clipboard
    * Authorize (top of swagger), using Bearer <access_token>
    * Post to CategoriesEndPoint/getcats, observe only rows 2-5 returned

    """

    @staticmethod
    @jwt_required()
    @jsonapi_rpc(http_methods=['POST'], valid_jsonapi=False)
    def get_cats():
        db = safrs.DB
        session = db.session
        # Security.set_user_sa()  # use to bypass authorization (also requires @admin_required)

        result = session.query(models.Category)
        for each_row in result:
            print(f'each_row: {each_row}')
        dont_rely_on_safrs_debug = True
        # response = {"result" : list(result)}
        if dont_rely_on_safrs_debug:
            rows = util.rows_to_dict(result)
            response = {"result": rows}
        return response
