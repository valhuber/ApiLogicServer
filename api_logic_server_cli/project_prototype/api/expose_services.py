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

    util.log("\n\n")
    util.log(f'*** Customizable ApiLogicServer project created -- '
             f'open it in your IDE at {project_dir}')
    util.log(f'*** Server now running -- '
             f'explore with OpenAPI (Swagger) at http://localhost:5000/')
    util.log("\n")