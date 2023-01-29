import logging
from flask import request, jsonify
from database import models
import util

app_logger = logging.getLogger(__name__)


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
    def hello_world():  # test it with: http://localhost:8080/hello_world?user=Basic_App
        """ simplest possible endpoint """
        user = request.args.get('user')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello, {user}'})


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


    @app.route('/order')
    def order():
        """
        Illustrates:
            Returning a nested result set response
            Using SQLAlchemy to obtain data
            Restructuring row results to desired json (e.g., for tool such as Sencha)
        Test:
            http://localhost:8080/order?Id=10643
            curl -X GET "http://localhost:8080/order?Id=10643"

        """
        order_id = request.args.get('Id')
        order = db.session.query(models.Order).filter(models.Order.Id == order_id).one()

        result_std_dict = util.row_to_dict(row2dict(order)
                                        # , replace_attribute_tag='data'
                                        , remove_links_relationships=False)
        result_std_dict['Customer_Name'] = order.Customer.CompanyName # eager fetch
        result_std_dict['OrderDetailListAsDicts'] = []
        for each_order_detail in order.OrderDetailList:
            each_order_detail_dict = util.row_to_dict(row=row2dict(each_order_detail)
                                                    # , replace_attribute_tag=None
                                                    , remove_links_relationships=False)
            each_order_detail_dict['ProductName'] = each_order_detail.Product.ProductName
            result_std_dict['OrderDetailListAsDicts'].append(each_order_detail_dict)
        return result_std_dict
    
    logging.info("\n\n..Basic App, exposing end points: hello_world, order, stop\n")

