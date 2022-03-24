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

from logic_bank.rule_bank.rule_bank import RuleBank

# called by expose_api_models.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated


def expose_services(app, api, project_dir, HOST: str, PORT: str):
    """ extend model end points with new end points for services

    This sample illustrates the classic hello world,
    and a more interesting add_order.

     """


    app_logger = logging.getLogger("api_logic_server_app")
    app_logger.info(f'\n*** Customizable ApiLogicServer project created -- '
             f'open it with your IDE at {project_dir}')
    app_logger.info(f'*** Server now running -- '
             f'explore sample data and API at http://{HOST}:{PORT}/')


    def rules_report():
        rules_bank = RuleBank()
        logic_logger = logging.getLogger("logic_logger")
        rule_count = 0
        logic_logger.debug(f'\nThe following rules have been activated\n')
        list_rules = rules_bank.__str__()
        loaded_rules = list(list_rules.split("\n"))
        for each_rule in loaded_rules:
            logic_logger.info(each_rule + '\t\t##  ')
            rule_count += 1
        logic_logger.info(f'Logic Bank - {rule_count} rules loaded')

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

    @app.route('/server_log')
    def server_log():
        """
        Used by test/server_test.py - enables client app to log msg into server
        """
        import os
        import datetime
        from pathlib import Path
        import logging
        # import logging.Logger as Logger


        def add_file_handler(logger, name: str, log_dir):
            """Add a file handler for this logger with the specified `name` (and
            store the log file under `log_dir`)."""
            # Format for file log
            for each_handler in logger.handlers:
                each_handler.flush()
                handler_name = str(each_handler)
                if "stderr" in handler_name:
                    pass
                    # print(f'do not delete stderr')
                else:
                    logger.removeHandler(each_handler)
            fmt = '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s'
            formatter = logging.Formatter(fmt)
            formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')

            # Determine log path/file name; create log_dir if necessary
            now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            log_name = f'{str(name).replace(" ", "_")}'  # {now}'
            if len(log_name) >= 26:
                log_name = log_name[0:25]

            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except:
                    print('{}: Cannot create directory {}. '.format(
                        self.__class__.__name__, log_dir),
                        end='', file=sys.stderr)
                    log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
                    print(f'Defaulting to {log_dir}.', file=sys.stderr)

            log_file = os.path.join(log_dir, log_name) + '.log'
            if os.path.exists(log_file):
                os.remove(log_file)
            else:
                pass  # file does not exist

            # Create file handler for logging to a file (log all five levels)
            # print(f'create file handler for logging: {log_file}')
            logger.file_handler = logging.FileHandler(log_file)
            logger.file_handler.setLevel(logging.DEBUG)
            logger.file_handler.setFormatter(formatter)
            logger.addHandler(logger.file_handler)

        msg = request.args.get('msg')
        test = request.args.get('test')
        if test is not None and test != "None":
            if test == "None":
                print(f'None for msg: {msg}')
            logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
            # logic_logger.info("\n\nLOGIC LOGGER HERE\n")
            dir = request.args.get('dir')
            add_file_handler(logic_logger, test, Path(os.getcwd()).joinpath(dir))
        if msg == "Rules Report":
            rules_report()
            logic_logger.info(f'Logic Bank {__version__} - {rule_count} rules loaded')
        else:
            app_logger.info(f'{msg}')
        return jsonify({"result": f'ok'})


    app_logger.info(f'*** Customizable ApiLogicServer project created -- '
             f'open it in your IDE at {project_dir}')
    app_logger.info(f'*** Server now running -- '
             f'explore your data and API at http://{HOST}:{PORT}/')
    app_logger.info("\n")
    
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
