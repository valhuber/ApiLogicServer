import sys
from pathlib import Path
import requests
import logging
# import util
import subprocess
import socket


"""
    These are server tests for the default Sample DB.
    See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#customize-server-startup

    These verify the following, and are useful coding examples of API Usage:
"""

get_test = True  # Performs a basic get, with Fields and Filter
patch_test = True  # Updates a Customer with intentionally bad data to illustrate logic
post_test = True  # Posts a customer
delete_test = True  # Deletes the posted customer
custom_service_test = True  # See https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#services-add-order


def prt(msg: any) -> None:
    print(msg)


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def server_tests(host, port, version):
    """ called by api_logic_server_run.py, for any tests on server start
        args
            host - server host
            port - server port
            version - ApiLogicServer version
    """
    prt(f'\n\n===================+')
    prt(f'SAMPLEDB DIAGNOSTICS')
    prt(f' verify good GET, PATCH, POST, DELETE and Custom Service')
    prt(f'===============+====\n')

    add_order_uri = f'http://{host}:{port}/ServicesEndPoint/add_order'
    add_order_args = {
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
    if get_test:
        get_order_uri = f'http://{host}:{port}/Order/?' \
                        f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                        f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
        r = requests.get(url=get_order_uri)
        response_text = r.text
        assert "VINET" in response_text, f'Error - "VINET not in {response_text}'

        prt(f'\nGET DIAGNOSTICS PASSED for table Order... now verify PATCH Customer...')

    if patch_test:
        patch_cust_uri = f'http://{host}:{port}/Customer/ALFKI/'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "CreditLimit": 10,
                        "Id": "ALFKI"},
                    "type": "Customer",
                    "id": "ALFKI"
                }}
        r = requests.patch(url=patch_cust_uri, json=patch_args)
        response_text = r.text
        assert "exceeds credit" in response_text, f'Error - "exceeds credit not in this response:\n{response_text}'

        prt(f'\nPATCH DIAGNOSTICS PASSED for table Customer... now verify POST Customer...')

    if post_test:
        post_cust_uri = f'http://{host}:{port}/Customer/'
        post_args = \
            {
                "data": {
                    "attributes": {
                        "CreditLimit": 10,
                        "Balance": 0,
                        "Id": "ALFKJ"},
                    "type": "Customer",
                    "id": "ALFKJ"
                }}
        r = requests.post(url=post_cust_uri, json=post_args)
        response_text = r.text
        assert r.status_code == 201, f'Error - "status_code != 200 in this response:\n{response_text}'

        prt(f'\nPOST DIAGNOSTICS PASSED for table Customer... now verify DELETE Customer...')

    if delete_test:
        delete_cust_uri = f'http://{host}:{port}/Customer/ALFKJ/'
        r = requests.delete(url=delete_cust_uri, json={})
        # Generic Error: Entity body in unsupported format
        response_text = r.text
        assert r.status_code == 204, f'Error - "status_code != 204 in this response:\n{response_text}'

        prt(f'\nDELETE DIAGNOSTICS PASSED for table Customer... now verify Custom Service add_order - check credit logic...')

    if custom_service_test:
        r = requests.post(url=add_order_uri, json=add_order_args)
        response_text = r.text
        assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'

        prt(f'\nADD ORDER CHECK CREDIT - DIAGNOSTICS PASSED')
        prt(f'===========================================\n')
        prt(f''
            f'Custom Service and Logic verified, by Posting intentionally invalid order to Custom Service to: {add_order_uri}.\n'
            f'Logic Log shows proper detection of Customer Constraint Failure...\n'
            f' - see https://github.com/valhuber/ApiLogicServer/wiki/Tutorial#services-add-order\n'
            f'.. The logic illustrates MULTI-TABLE CHAINING (note indents):\n'
            f'....FORMULA OrderDetail.Amount (19998), which...\n'
            f'......ADJUSTS Order.AmountTotal (19998), which...\n'
            f'........ADJUSTS Customer.Balance (21014), which...\n'
            f'........Properly fails CONSTRAINT (balance exceeds limit of 2000), as intended.\n\n'
            f'All from just 5 rules in ({get_project_dir()}/logic/declare_logic.py)\n\n')



if __name__ == "__main__":
   # only to run when not called via 'import' here
   server_tests("localhost", "5656", "v0")