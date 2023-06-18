import logging
from flask import request, jsonify
from database import models
import util


def row2dict(row):
    return {
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }


def flask_events(app, db):
    """ 
    Illustrate flask events
    """
    app_logger = logging.getLogger(__name__)

    @app.route('/hello_world')
    def hello_world():
        """
        Illustrates simplest possible endpoint, with url args.

        The url suffix is specified in the annotation.

        Test it with: http://localhost:8080/hello_world?user=Basic_App

        Returns:
            json : a simple string
        """
        user = request.args.get('user')  # obtain URL argument from Flask via built-in request object
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello, {user}'})  # the api response (in json)


    @app.route('/order', methods=['GET'])  # tell Flask: call this function when /order request occurs
    def order():
        """
        End point to return a nested result set response

        Illustrates:
        1. Obtain URL argument from Flask
        2. Read data from SQLAlchemy, and related data (via foreign keys)
        3. Restructure row results to desired json (e.g., for tool such as Sencha)
        4. Use Flask to return nested response json

        Test:
            http://localhost:8080/order?id=10643
            curl -X GET "http://localhost:8080/order?id=10643"

        """

        # 1. Obtain URL argument from Flask
        order_id = request.args.get('id')  

        # 2. Read data from SQLAlchemy
        order = db.session.query(models.Order).\
            filter(models.Order.Id == order_id).one()
        app_logger.info(f'\n Breakpoint - examine order in debugger \n')

        # 3. Restructure row results - format as result_std_dict
        result_std_dict = util.format_nested_object(row2dict(order)
                                        , remove_links_relationships=False)
        result_std_dict['Customer_Name'] = order.Customer.CompanyName # eager fetch
        result_std_dict['OrderDetailListAsDicts'] = []
        for each_order_detail in order.OrderDetailList:  # SQLAlchemy related data access
            each_order_detail_dict = util.format_nested_object(row=row2dict(each_order_detail)
                                                    , remove_links_relationships=False)
            each_order_detail_dict['ProductName'] = each_order_detail.Product.ProductName
            result_std_dict['OrderDetailListAsDicts'].append(each_order_detail_dict)

        # 4. Use Flask to return nested response json (Flask jsonifies dict)
        return result_std_dict  # rest response
    

    @app.route('/stop')
    def stop():  # test it with: http://localhost:8080/stop?msg=API stop - Stop Basic App Server
        """
        Use this to stop the server from the Browser.

        See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
        """

        import os, signal

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })


    logging.info("\n\n..Basic App, exposing end points: hello_world, order, stop\n")

