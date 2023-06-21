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

# Customize this file to add endpoints/services, using SQLAlchemy as required
#     Separate from expose_api_models.py, to simplify merge if project rebuilt
# Called by api_logic_server_run.py

app_logger = logging.getLogger("api_logic_server_app")  # only for create-and-run, no?

def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ 
    Illustrates Customized APIs, Data Access.

    * Observe that APIs not limited to database objects, but are extensible.
    * See: https://apilogicserver.github.io/Docs/API-Customize/
    * See: https://github.com/thomaxxl/safrs/wiki/Customization

    Examples

    * order_nested_objects() - 
            * Uses util.format_nested_objects() (-> jsonify(row).json)

    * CategoriesEndPoint get_cats() - swagger, row security
            * Uses util.rows_to_dict            (-> row.to_dict())

    * filters_cats() - model query with filters
            * Uses manual result creation (not util)

    * raw_sql_cats() - raw sql (non-modeled objects)
            * Uses util.rows_to_dict            (-> iterate attributes)
    
    """

    app_logger.info("..api/expose_service.py, exposing custom services: hello_world, add_order")

    api.expose_object(ServicesEndPoint)  # Swagger-visible services
    api.expose_object(CategoriesEndPoint)

    @app.route('/hello_world')
    def hello_world():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/hello_world?user=ApiLogicServer
        """
        user = request.args.get('user')
        # app_logger.info(f'hello_world returning:  hello, {user}')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello, {user}'})


    @app.route('/stop')
    def stop():
        """
        Use this to stop the server from the Browser.
        * See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
        * See: https://github.com/thomaxxl/safrs/wiki/Customization

        Usage:

                http://localhost:5656/stop?msg=API stop - Stop API Logic Server
        """

        import os, signal

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })


    def admin_required():
        """
        Support option to bypass security (see cats, below).

        See: https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
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


    @app.route('/filters_cats')
    @admin_required()
    def filters_cats():
        """
        Illustrates:
        * Explore SQLAlchemy and/or filters.
        
        Test (returns rows 2-5) (no auth):
            curl -X GET "http://localhost:5656/filters_cats" [no-filter | simple-filter]"
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
        return jsonify({ "success": True, "result":  return_result})


    @app.route('/raw_sql_cats')
    @admin_required()
    def raw_sql_cats():
        """
        Illustrates:
        * "Raw" SQLAlchemy table queries (non-mapped objects)
        * Observe phyical column name: CategoryName_ColumnName
              * Contrast to models.py, get_cats()
        
        Test (auth optional):
            curl -X GET "http://localhost:5656/raw_sql_cats"

        """
        DB = safrs.DB 
        sql_query = DB.text("SELECT * FROM CategoryTableNameTest")
        with DB.engine.begin() as connection:
            query_result = connection.execute(sql_query).all()
            rows_to_dict_rows = util.rows_to_dict(query_result)
        response = {"result": rows_to_dict_rows} 
        return response


    @app.route('/order_nested_objects')
    def order_nested_objects():
        """
        Illustrates:
        * Returning a nested result set response
        * Using SQLAlchemy to obtain data, and related data
        * Restructuring row results to desired json (e.g., for tool such as Sencha)

        Test (auth optional):
            http://localhost:5656/order_nested_objects?Id=10643
            curl -X GET "http://localhost:5656/order_nested_objects?Id=10643"

        """
        order_id = request.args.get('Id')
        db = safrs.DB         # Use the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        order = session.query(models.Order).filter(models.Order.Id == order_id).one()

        result_std_dict = util.format_nested_object(order
                                        , replace_attribute_tag='data'
                                        , remove_links_relationships=True)
        result_std_dict['data']['Customer_Name'] = order.Customer.CompanyName # eager fetch
        result_std_dict['data']['OrderDetailListAsDicts'] = []
        for each_order_detail in order.OrderDetailList:       # lazy fetch
            each_order_detail_dict = util.format_nested_object(row=each_order_detail
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


class ServicesEndPoint(safrs.JABase):
    """
    Illustrates
    * Custom service - visible in swagger
    * Quite small, since leverages logic/declare_logic rules
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
        return {"Thankyou For Your Order"}  # automatic commit, which executes transaction logic


class CategoriesEndPoint(safrs.JABase):
    """
    Illustrates
    * Swagger-visible RPC that requires authentication (@jwt_required()).
    * Row Security

    Test in swagger (auth required)
    * Post to endpoint auth to obtain <access_token> value - copy to clipboard
            * Row Security - Users determines results
            * u1 - 1 row, u2 - 4 rows, admin - 9 rows
    * Authorize (top of swagger), using Bearer <access_token>
    * Post to CategoriesEndPoint/get_cats, observe results depend on login

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
            app_logger.debug(f'each_row: {each_row}')
        rows = util.rows_to_dict(result)
        response = {"result": rows}
        return response
