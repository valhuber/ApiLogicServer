import sys
import requests
import logging
import util

logic_logger = logging.getLogger("logic_logger")

server_tests_enabled = True

def prt(msg: any) -> None:
    logic_logger.debug(msg)
    util.log(msg)
    util.log(str(logic_logger.handlers))


logic_logger.debug("server_tests 1.0")


def server_tests(host, port):
    """ called by api_logic_server_run.py, for any tests on server start
        args
            host - server host
            port - server port
    """

    uri = f'http://{host}:{port}/ServicesEndPoint/add_order'
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

    prt(f'\n\ntest.server_startup_test -- server_tests("{host}", "{port}")')
    prt(f'.. verify custom service and logic - post invalid order to {uri} with {args}')

    svr_logger = logging.getLogger('safrs.safrs_init')
    save_level = svr_logger.getEffectiveLevel()
    svr_logger.setLevel(logging.FATAL)  # hide ugly stacktrace on startup - not required

    r = requests.post(url=uri, json=args)

    # extracting response text
    pastebin_url = r.text
    prt("The pastebin URL is:%s" % pastebin_url)

    svr_logger.setLevel(save_level)