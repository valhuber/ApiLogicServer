import logging
import shutil
import sys
import os
import datetime
from pathlib import Path
from typing import NewType

import create_from_model.model_creation_services as create_from_model

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)

__version__ = "0.0"


def create_expose_api_models(model_creation_services: create_from_model.ModelCreationServices):
    """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

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
        f'\n\ndef expose_models(api):\n'
    # result_apis += '    my_host = HOST\n'
    # result_apis += '    if HOST == "0.0.0.0":\n'
    # result_apis += '        my_host = "localhost"  # override default HOST for pc"\n'
    result_apis += '    """\n'
    result_apis += '        Declare API - on existing SAFRSAPI \n'
    result_apis += '            This exposes each model (note: end point names are table names) \n'
    result_apis += '            Including get (filtering, pagination, related data access) \n'
    result_apis += '            And post/patch/update (including logic enforcement) \n'
    result_apis += '        You typically do not customize this file \n'
    result_apis += '            See https://valhuber.github.io/ApiLogicServer/Tutorial/#customize-and-debug \n'
    result_apis += '    """\n'

    sys.path.append(model_creation_services.os_cwd)

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
            result_apis += f'    api.expose_object(database.models.{each_resource_name})\n'
    result_apis += f'    return api\n'
    # self.session.close()
    expose_api_models_path = Path(model_creation_services.project_directory).joinpath('api/expose_api_models.py')
    if not model_creation_services.command.startswith("rebuild"):
        expose_api_models_file = open(expose_api_models_path, 'a')
        expose_api_models_file.write(result_apis)
        expose_api_models_file.close()
    else:
        expose_api_models_path = Path(model_creation_services.project_directory).\
            joinpath('api/expose_api_models_created.py')
        print(f'.. .. ..Rebuild - new api at api/expose_api_models_created (merge/replace expose_api_models as nec)')
        src = Path(model_creation_services.api_logic_server_dir)
        src = src.joinpath("project_prototype/api/expose_api_models.py")
        assert src.is_file()
        shutil.copyfile(src, expose_api_models_path)
        expose_api_models_file = open(expose_api_models_path, 'a')
        expose_api_models_file.write(result_apis)
        expose_api_models_file.close()
    return


def create(model_creation_services: create_from_model.ModelCreationServices):
    """ called by ApiLogicServer CLI -- creates api/expose_api_models.py, key input to SAFRS
    """
    create_expose_api_models(model_creation_services)
