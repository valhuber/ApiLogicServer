import sys, os
import logging, logging.config
from flask import Flask, current_app, g
import sqlite3
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from safrs import jsonapi_rpc
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_mapper
from database import models
import util
from config import Config
import yaml

"""
This illustrates the use of "raw" (hand-coded) Flask.

API Logic Server creates your project and automates your API, Admin App, and Logic.

Or, you can code it all by hand.
See: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

"""

"""
 Logging configuration
"""
current_path = os.path.abspath(os.path.dirname(__file__))
with open(f'{current_path}/logging.yml','rt') as f:
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)  # log levels: critical < error < warning(20) < info(30) < debug
app_logger = logging.getLogger(__name__)
debug_value = os.getenv('APILOGICPROJECT')
if debug_value is not None:
    debug_value = debug_value.upper()
    if debug_value.startswith("F") or debug_value.startswith("N"):
        app_logger.setLevel(logging.INFO)
    else:
        app_logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

def row2dict(row):
    return {
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }


def flask_events(app):
    """ 
    Illustrate flask events
    """
    app_logger = logging.getLogger("api_logic_server_app")

    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost:8080/hello_world?user=ApiLogicServer
        """ simplest possible endpoint """
        user = request.args.get('user')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello, {user}'})


    @app.route('/stop')
    def stop():  # test it with: http://localhost:8080/stop?msg=API stop - Stop Raw Flask Server
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
    
    logging.info("\n\n..Raw Flask, exposing custom services: hello_world, order, stop\n")


db = SQLAlchemy()      # create the extension

app = Flask(__name__)  # create the app

app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI  # db location

db.init_app(app)  # initialize the app with the extension

flask_events(app)  # register endpoints

logging.info("Starting server: test as follows...")
logging.info('..curl -X GET "http://localhost:8080/hello_world"')
logging.info('..curl -X GET "http://localhost:8080/order?Id=10643"')
logging.info('')

app.run(host="localhost", port=8080, debug=True)  # start the server

