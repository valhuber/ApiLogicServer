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

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger("api_logic_server_app")


def expose_services(app, api, project_dir, HOST: str, PORT: str):
    """ extend model end points with new end points for services """
    app_logger.info("api/customize_api.py - expose custom services")

    @app.route('/hello_world')
    def hello_world():  # test it with: http://api_logic_server_host:api_logic_server_port/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})

    app_logger.info(f'*** Customizable ApiLogicServer project created -- '
             f'open it in your IDE at {project_dir}')
    app_logger.info(f'*** Server now running -- '
             f'explore your data and API at http://{HOST}:{PORT}/')
    app_logger.info("\n")