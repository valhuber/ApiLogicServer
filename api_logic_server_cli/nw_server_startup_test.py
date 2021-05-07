import sys
from pathlib import Path

import requests
import logging
import util

server_tests_enabled = True

prt_prefix = "test/server_startup_test.py --"
def prt(msg: any) -> None:
    util.log(f'{msg}')


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def server_tests(host, port):
    """ called by api_logic_server_run.py, for any tests on server start
        args
            host - server host
            port - server port
    """

    add_order_uri = f'http://{host}:{port}/ServicesEndPoint/add_order'
    args = {
      "meta": {
        "method": "add_order",
        "args": {
          "CustomerId": "ALFKI",
          "EmployeeId": 1,
          "Freight": 10,
          "OrderDetailList": [
            {
              "ProductId": 1,
              "Quantity": 1111,
              "Discount": 0
            },
            {
              "ProductId": 2,
              "Quantity": 2,
              "Discount": 0
            }
          ]
        }
      }
    }

    prt(f'\n\n{prt_prefix} server_tests("{host}", "{port}") called (v1.0)\n')

    # use swagger to get uri

    get_order_uri = f'http://{host}:{port}/Order/?' \
                    f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                    f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
    r = requests.get(url=get_order_uri)

    response_text = r.text
    assert "VINET" in response_text, f'Error - "VINET not in {response_text}'
    prt(f'\n{prt_prefix} Verified retrieval from table Order')

    svr_logger = logging.getLogger('safrs.safrs_init')
    save_level = svr_logger.getEffectiveLevel()
    svr_logger.setLevel(logging.FATAL)  # hide ugly stacktrace on startup - not required

    r = requests.post(url=add_order_uri, json=args)

    response_text = r.text
    assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'
    prt(f'\n{prt_prefix} STARTUP DIAGNOSTICS SUCCESS - \n'
        f'..Custom Service and Logic verified, as follows.'
        f'..Posted intentionally invalid order to Custom Service at: {add_order_uri}.\n'
        f'..Logic Log (above, best viewed without word wrap <mac: tput rmam/tput smam) '
        f'shows proper detection of Customer Constraint Failure.\n'
        f'..This illustrates multi-table chaining (per indention level).'
        f'  The logic at {get_project_dir()}/logic/logic_bank.py:\n'
        f'....COMPUTED OrderDetail.Amount (19998), which...\n'
        f'......ADJUSTS Order.AmountTotal (19998), which...\n'
        f'........ADJUSTS Customer.Balance (21014), which...\n'
        f'........Properly fails CONSTRAINT (balance exceeds limit of 2000), as intended.\n\n'
        f'ApiLogicServer PROJECT SUCCESSFULLY CREATED at {get_project_dir()} - open it with your IDE\n'
        f'..SERVER has been STARTED, and startup DIAGNOSTICS have run successfully (see above)\n'
        f'..Explore your API at http://{host}:{port}\n\n'
        f'===> For more information, see https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database\n')

    svr_logger.setLevel(save_level)