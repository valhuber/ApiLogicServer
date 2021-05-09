from pathlib import Path
import requests
import logging
import util

server_tests_enabled = True  # use True to invoke server_tests on server startup

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

    util.log(f'\n\n===================')
    util.log(f'STARTUP DIAGNOSTICS')
    util.log(f'.. server_tests("{host}", "{port}") called (v1.0)')
    util.log(f'.. see test/server_startup_test.py - diagnostics are good GET and POST examples')
    util.log(f'===================\n')

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

    # use swagger to get uri

    get_order_uri = f'http://{host}:{port}/Order/?' \
                    f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                    f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
    r = requests.get(url=get_order_uri)

    response_text = r.text
    assert "VINET" in response_text, f'Error - "VINET not in {response_text}'
    prt(f'\nRETRIEVAL DIAGNOSTICS PASSED for table Order... now verify Add Order check credit logic...')

    #  logic log hard to read with word wrap.  mac/unix can suppress with tput rmam/tput smam
    prt(f'.. Add Order logic log follows...')

    svr_logger = logging.getLogger('safrs.safrs_init')
    save_level = svr_logger.getEffectiveLevel()
    svr_logger.setLevel(logging.FATAL)  # hide ugly stacktrace on startup - not required

    r = requests.post(url=add_order_uri, json=args)

    response_text = r.text
    assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'

    util.log(f'\nADD ORDER CHECK CREDIT - STARTUP DIAGNOSTICS PASSED')
    util.log(f'===================================================')
    prt(f''
        f'Custom Service and Logic verified, by Posting intentionally invalid order to Custom Service to: {add_order_uri}.\n'
        f'Logic Log (above) shows proper detection of Customer Constraint Failure...\n'
        f'.. Best viewed without word wrap'
        f' - see https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#services-add-order\n'
        f'.. The logic illustrates MULTI-TABLE CHAINING (note indents):\n'
        f'....FORMULA OrderDetail.Amount (19998), which...\n'
        f'......ADJUSTS Order.AmountTotal (19998), which...\n'
        f'........ADJUSTS Customer.Balance (21014), which...\n'
        f'........Properly fails CONSTRAINT (balance exceeds limit of 2000), as intended.\n'
        f'All from just 5 rules in ({get_project_dir()}/logic/logic_bank.py)\n\n')

    util.log(f'\nAPILOGICSERVER SUMMARY')
    util.log(f'======================\n')
    prt(f''
        f'1. CUSTOMIZABLE PROJECT CREATED from supplied Sample DB\n'
        f'     .. Explore your project - open with IDE/Editor at {get_project_dir()}\n'
        f'2. SERVER has been STARTED (python api_logic_server_run.py)\n'
        f'     .. Explore your API - Swagger at http://{host}:{port}\n'
        f'3. BASIC WEB APP Created\n'
        f'     .. Start it: python ui/basic_web_app/run.py\n'
        f'     .. Then, explore it: http://0.0.0.0:8080/\n'
        f'     .. See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#3-explore-the-basic-web-app\n'
        f'4. Server Startup DIAGNOSTICS have PASSED (see log above)\n'
        f'     .. See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#customize-server-startup\n'
        f'\n'
        f'===> For more information, see https://github.com/valhuber/ApiLogicServer/wiki/Tutorial\n')

    svr_logger.setLevel(save_level)