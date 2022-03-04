import sys
from pathlib import Path
import requests
import logging
# import util
import subprocess
import socket
import json

# print(f'args: {sys.argv}')
if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1].__contains__("help")):
    print("")
    print("Test server functions (including logic), on localhost:5656")
    print("  python server_test.py go")
    print("")
    sys.exit()


"""
    These are server tests for the default Sample DB.

    These verify the following, and are useful coding examples of API Usage:
"""

get_test = True  # Performs a basic get, with Fields and Filter
patch_test = True  # Updates a Customer with intentionally bad data to illustrate logic
post_test = True  # Posts a customer
delete_test = True  # Deletes the posted customer
custom_service_test = True  # See https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization
self_reln_test = True  # verify dept subDepts, headDept
cascade_update_test = True  # verify Order.ShippedDate 2013-10-13 adjusts balance 2102-1086->1016, product onhand


def prt(msg: any) -> None:
    '''
    print to console, and server log (see api/customize_api.py)
    '''
    print(msg)
    msg_url = f'http://localhost:5656/server_log?msg={msg}'
    r = requests.get(msg_url)


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

    def get_ALFKI():
        get_cust_uri = f'http://{host}:{port}/api/Customer/ALFKI?' \
                            f'fields%5B=Id%2CBalance' \
                            f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
        r = requests.get(url=get_cust_uri)
        response_text = r.text
        return response_text

    prt(f'\n\n====================\n'
        f'SAMPLEDB DIAGNOSTICS\n'
        f'verify good GET, PATCH, POST, DELETE and Custom Service\n'
        f'includes deliberate errors, to test constraints (these log strack traces, which are *NOT* errors\n'
        f'====================\n')

    add_order_uri = f'http://{host}:{port}/api/ServicesEndPoint/add_order'
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
        test_name = "GET test on Order"
        prt(f'\n\n\n{test_name} - verify VINET returned...\n')
        get_order_uri = f'http://{host}:{port}/api/Order/?' \
                        f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                        f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
        r = requests.get(url=get_order_uri)
        response_text = r.text
        assert "VINET" in response_text, f'Error - "VINET not in {response_text}'
        prt(f'\n{test_name} PASSED\n')

    if self_reln_test:
        test_name = "GET self-reln test on Department/DepartmentList"
        prt(f'\n\n\n{test_name}...\n\n')
        get_dept_uri = f'http://{host}:{port}/api/Department/2/?' \
                        f'include=DepartmentList%2CEmployeeList%2CEmployeeList1%2CDepartment' \
                       f'&fields%5BDepartment%5D=Id%2CDepartmentId%2CDepartmentName'
        r = requests.get(url=get_dept_uri)
        response_text = r.text
        result_data = json.loads(response_text)  # 'str' object has no attribute 'read'
        relationships = result_data["data"]["relationships"]
        relationships_department = relationships["Department"]
        relationships_department_list = relationships["DepartmentList"]
        ceo_check = relationships_department["data"]["id"]  # should be '1'
        ne_sales_check = relationships_department_list["data"][0]["id"]  # should be 4
        assert ceo_check == '1' and ne_sales_check == '4',\
            f'Error - "CEO not in Department or NE Sales not in DepartmentList: {response_text}'
        prt(f'\n{test_name} PASSED\n')

    if patch_test:
        test_name = "PATCH test"
        prt(f'\n\n\n{test_name}... deliberate errror - set credit_limit low to verify check credit constraint\n\n')
        patch_cust_uri = f'http://{host}:{port}/api/Customer/ALFKI/'
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

        prt(f'\n{test_name} PASSED\n')

    if post_test:
        test_name = "POST test"
        prt(f'\n\n\n{test_name}... create a customer\n\n')
        post_cust_uri = f'http://{host}:{port}/api/Customer/'
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

        prt(f'\n{test_name} PASSED\n')

    if delete_test:
        test_name = "DELETE test"
        prt(f'\n\n\n{test_name}... delete the customer just created\n\n')
        delete_cust_uri = f'http://{host}:{port}/api/Customer/ALFKJ/'
        r = requests.delete(url=delete_cust_uri, json={})
        # Generic Error: Entity body in unsupported format
        response_text = r.text
        assert r.status_code == 204, f'Error - "status_code != 204 in this response:\n{response_text}'

        prt(f'\n{test_name} PASSED\n')

    if cascade_update_test:
        test_name = "CASCADE UPDATE test"
        prt(f'\n\n\n{test_name}... verify Order.ShippedDate (2013-10-13) adjusts balance 2102-1086->1016, product onhand\n\n')
        patch_uri = f'http://{host}:{port}/api/Order/10643/'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "ShippedDate": "2013-10-13",
                        "Id": 10643},
                    "type": "Order",
                    "id": 10643
                }}
        r = requests.patch(url=patch_uri, json=patch_args)
        # response_text = r.text
        prt(response_text)
        response_text = get_ALFKI()
        # prt(f'\nget_ALFKI: {response_text}')
        assert '"Balance": 1016.0' in response_text, f'Error - "Balance": 1026.0 not in this response:\n{response_text}'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "ShippedDate": None,
                        "Id": 10643},
                    "type": "Order",
                    "id": 10643
                }}
        r = requests.patch(url=patch_uri, json=patch_args)
        response_text = r.text
        # prt(response_text)
        response_text = get_ALFKI()
        # prt(f'\nget_ALFKI after nullify: {response_text}')
        assert '"Balance": 2102.0' in response_text, f'Error - "Balance": 2102.0 not in this response:\n{response_text}'

        prt(f'\n{test_name} PASSED\n')
        
    if custom_service_test:
        test_name = "CUSTOM SERVICE  test"
        prt(f'\n\n\n{test_name}... post too-big an order to deliberately exceed credit - note multi-table logic chaining\n\n')
        r = requests.post(url=add_order_uri, json=add_order_args)
        response_text = r.text
        assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'

        prt(f'\n{test_name} PASSED\n')
        prt(f'===========================================\n')
        prt(f''
            f'Custom Service and Logic verified, by Posting intentionally invalid order to Custom Service to: {add_order_uri}.\n'
            f'Logic Log shows proper detection of Customer Constraint Failure...\n'
            f' - see https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization\n'
            f'.. The logic illustrates MULTI-TABLE CHAINING (note indents):\n'
            f'....FORMULA OrderDetail.Amount (19998), which...\n'
            f'......ADJUSTS Order.AmountTotal (19998), which...\n'
            f'........ADJUSTS Customer.Balance (21014), which...\n'
            f'........Properly fails CONSTRAINT (balance exceeds limit of 2000), as intended.\n\n'
            f'All from just 5 rules in ({get_project_dir()}/logic/declare_logic.py)\n\n')


if __name__ == "__main__":
   server_tests("localhost", "5656", "v0")