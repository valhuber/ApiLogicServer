import logging
import sys
import os
import datetime
from typing import NewType

import create_from_model.model_creation_services as create_from_model

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)

__version__ = "0.0"


def create_expose_api_models(model_creation_services):
    """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

    cwd = os.getcwd()
    result_apis = ''
    '''
    result_apis += '"""'
    result_apis += ("\nApiLogicServer Generate From Model "
                    + model_creation_services.version + "\n\n"
                    # + "From: " + sys.argv[0] + "\n\n"
                    + "Using Python: " + sys.version + "\n\n"
                    + "At: " + str(datetime.datetime.date()) + "\n\n"
                    + '"""\n\n')
    '''
    port_replace = model_creation_services.port if model_creation_services.port else "None"
    result_apis += \
        f'\n\ndef expose_models(app, HOST="{model_creation_services.host}", PORT={port_replace}, API_PREFIX="/api"):\n'
    # result_apis += '    my_host = HOST\n'
    # result_apis += '    if HOST == "0.0.0.0":\n'
    # result_apis += '        my_host = "localhost"  # override default HOST for pc"\n'
    result_apis += '    """ create SAFRSAPI, exposing each model (note: end point names are table names) """\n'
    result_apis += '    app_logger.debug(f"api/expose_api_models -- host = {HOST}, port = {PORT}")\n'
    result_apis += '    api = SAFRSAPI(app, host=HOST, port=PORT, prefix = API_PREFIX)\n'
    result_apis += '    safrs_log_level = safrs.log.getEffectiveLevel()\n'
    result_apis += '    if True or app_logger.getEffectiveLevel() >= logging.INFO:\n'
    result_apis += '        safrs.log.setLevel(logging.WARN)  # warn is 20, info 30\n'

    sys.path.append(cwd)

    for each_resource_name in model_creation_services.resource_list:
        log.debug("process_each_table: " + each_resource_name)
        if "TRANSFERFUNDx" in each_resource_name:
            log.debug("special table")  # debug stop here
        if each_resource_name + " " in model_creation_services.not_exposed:
            # result_apis += "# not_exposed: api.expose_object(models.{resource_name})"
            continue
        if "ProductDetails_V" in each_resource_name:
            log.debug("special table")  # should not occur (--noviews)
        if each_resource_name.startswith("Ab"):
            # result_apis += "# skip admin table: " + resource_name + "\n"
            continue
        elif 'sqlite_sequence' in each_resource_name:
            # result_apis +=  "# skip sqlite_sequence table: " + resource_name + "\n"
            continue
        else:
            result_apis += f'    api.expose_object(models.{each_resource_name})\n'
    result_apis += f'    safrs.log.setLevel(safrs_log_level)\n'
    result_apis += f'    return api\n'
    # self.session.close()
    text_file = open(model_creation_services.project_directory + '/api/expose_api_models.py', 'a')
    text_file.write(result_apis)
    text_file.close()

    return


def create(model_creation_services: create_from_model.CreateFromModel):
    """ called by ApiLogicServer CLI -- creates api/expose_api_models.py, key input to SAFRS
    """
    create_expose_api_models(model_creation_services)
