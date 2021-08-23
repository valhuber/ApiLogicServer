import logging
import sys
import os
import datetime
from typing import NewType
from api_logic_server_cli.create_from_model.model_creation_services import CreateFromModel

log = logging.getLogger(__name__)

#  MetaData = NewType('MetaData', object)
MetaDataTable = NewType('MetaDataTable', object)

__version__ = "0.0"


def create_expose_api_models(model_creation_services, version=__version__):
    """ create strings for ui/basic_web_app/views.py and api/expose_api_models.py """

    cwd = os.getcwd()
    result_apis = '"""'
    result_apis += ("\nApiLogicServer Generate From Model " + version + "\n\n"
                                            # + "From: " + sys.argv[0] + "\n\n"
                                            + "Using Python: " + sys.version + "\n\n"
                                            + "At: " + str(datetime.datetime.now()) + "\n\n"
                                            + '"""\n\n')
    port_replace = model_creation_services.port if model_creation_services.port else "None"
    result_apis += \
        f'def expose_models(app, HOST="{model_creation_services.host}", PORT={port_replace}, API_PREFIX="/api"):\n'
    result_apis += '    """ called by api_logic_server_run.py """\n\n'
    result_apis += \
        '    api = SAFRSAPI(app, host=HOST, port=PORT)\n'

    sys.path.append(cwd)  # for banking Command Line test

    model_creation_services.find_meta_data(cwd, log_info=True)  # sets self.metadata
    meta_tables = model_creation_services.metadata.tables
    for each_table in meta_tables.items():
        table_name = each_table[1].name
        log.debug("process_each_table: " + table_name)
        if "TRANSFERFUNDx" in table_name:
            log.debug("special table")  # debug stop here
        if table_name + " " in model_creation_services.not_exposed:
            # result_apis += "# not_exposed: api.expose_object(models.{table_name})"
            continue
        if "ProductDetails_V" in table_name:
            log.debug("special table")  # should not occur (--noviews)
        if table_name.startswith("ab_"):
            # result_apis += "# skip admin table: " + table_name + "\n"
            continue
        elif 'sqlite_sequence' in table_name:
            # result_apis +=  "# skip sqlite_sequence table: " + table_name + "\n"
            continue
        else:
            class_name = model_creation_services.get_class_for_table(table_name)
            if class_name is None:
                # result_apis +=   "# skip view: " + table_name
                continue
            result_apis += f'    api.expose_object(models.{class_name})\n'
    result_apis += f'    return api\n'
    # self.session.close()
    text_file = open(model_creation_services.project_directory + '/api/expose_api_models.py', 'a')
    text_file.write(result_apis)
    text_file.close()

    return


def create(model_creation_services: CreateFromModel):
    """ called by ApiLogicServer CLI -- creates api/expose_api_models.py, key input to SAFRS
    """
    create_expose_api_models(model_creation_services)
