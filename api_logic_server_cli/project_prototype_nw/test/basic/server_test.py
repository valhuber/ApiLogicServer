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
self_reln_test = True  # Get dept, verify subDepts, headDept
post_test = True  # Posts a customer
delete_test = True  # Deletes the posted customer

patch_test = True   # simple constraint test (set credit limit low)
adjust_test = True  # Update Order Detail with intentionally bad data to illustrate chaining, constraint, reuse
audit_test = True   # alter salary, check for audit row
prune_test = True   # observe rules pruned for Order.RequiredDate (2013-10-13)
cascade_update_test = True  # verify Order.ShippedDate 2013-10-13 adjusts balance 2102-1086->1016, product onhand
custom_service_test = True  # See https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization


def prt(msg: any, test: str= None) -> None:
    """
    print to console, and server_log (see api/customize_api.py)
    """
    print(msg)
    msg_url = f'http://localhost:5656/server_log?msg={msg}&test={test}&dir=test/basic/results'
    r = requests.get(msg_url)


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return str(parent_path)


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
        f'====================\n', "BEGIN")

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
        prt(f'\n\n\n{test_name} - verify VINET returned...\n', test_name)
        get_order_uri = f'http://{host}:{port}/api/Order/?' \
                        f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                        f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
        r = requests.get(url=get_order_uri)
        response_text = r.text
        assert "VINET" in response_text, f'Error - "VINET not in {response_text}'
        prt(f'\n{test_name} PASSED\n')

    if self_reln_test:
        test_name = "GET self-reln Dept-SubDepts"
        prt(f'\n\n\n{test_name}...\n\n', test_name)
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
        assert ceo_check == '1' and ne_sales_check == '4', \
            f'Error - "CEO not in Department or NE Sales not in DepartmentList: {response_text}'
        prt(f'\n{test_name} PASSED\n')

    if patch_test:
        test_name = "PATCH - low credit"
        prt(f'\n\n\n{test_name}... deliberate errror - set credit_limit low to verify check credit constraint\n\n', test_name)
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
        assert "exceeds credit" in response_text, f'Error - "exceeds credit" not in this response:\n{response_text}'

        prt(f'\n{test_name} PASSED\n')

    if adjust_test:
        test_name = "ADJUST test - OrderDetail Qty"
        prt(f'\n\n\n{test_name}... deliberate error - update Order Detail with intentionally bad data '
            f'to illustrate chaining, constraint, reuse\n\n', test_name)
        patch_cust_uri = f'http://{host}:{port}/api/OrderDetail/1040/'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Id": 1040,
                        "Quantity": 1110
                    },
                    "type": "OrderDetail",
                    "id": "1040"
                }
            }
        r = requests.patch(url=patch_cust_uri, json=patch_args)
        response_text = r.text
        assert "exceeds credit" in response_text, f'Error - "exceeds credit" not in this response:\n{response_text}'

        prt(f'\n{test_name} PASSED\n')

    if audit_test:
        test_name = "AUDIT test - Emp Sal"
        prt(f'\n\n\n{test_name}... alter salary, ensure audit row created (also available in shell script\n\n', test_name)
        patch_emp_uri = f'http://{host}:{port}/api/Employee/5/'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Salary": 200000,
                        "Id": 5},
                    "type": "Employee",
                    "id": 5
                }}
        r = requests.patch(url=patch_emp_uri, json=patch_args)
        response_text = r.text
        assert '"Salary": 200000.0' in response_text, f'Error - "Salary": 200000.0 not in patch response:\n{response_text}'

        audit_uri = f'http://{host}:{port}/api/EmployeeAudit/?' \
                    'include=Employee&fields%5BEmployeeAudit%5D=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn&' \
                    'page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn%2Cid'
        r = requests.get(url=audit_uri)
        response_text = r.text
        assert '"Salary": 200000.0' in response_text, f'Error - "Salary": 200000.0 not in audit response:\n{response_text}'

        prt(f'\n{test_name}... return DB to original state\n')
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Salary": 95000,
                        "Id": 5},
                    "type": "Employee",
                    "id": 5
                }}
        r = requests.patch(url=patch_emp_uri, json=patch_args)
        response_text = r.text

        prt(f'\n{test_name} PASSED\n')

    if post_test:
        test_name = "POST test - Cust"
        prt(f'\n\n\n{test_name}... create a customer\n\n', test_name)
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
        test_name = "DELETE test - Cust"
        prt(f'\n\n\n{test_name}... delete the customer just created\n\n', test_name)
        delete_cust_uri = f'http://{host}:{port}/api/Customer/ALFKJ/'
        r = requests.delete(url=delete_cust_uri, json={})
        # Generic Error: Entity body in unsupported format
        response_text = r.text
        assert r.status_code == 204, f'Error - "status_code != 204 in this response:\n{response_text}'

        prt(f'\n{test_name} PASSED\n')

    if prune_test:
        test_name = "PRUNE test - ReqdDate"
        prt(f'\n\n\n{test_name}... observe rules pruned for Order.RequiredDate (2013-10-13) \n\n', test_name)
        patch_uri = f'http://{host}:{port}/api/Order/10643/'
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "RequiredDate": "2013-10-13",
                        "Id": 10643},
                    "type": "Order",
                    "id": 10643
                }}
        r = requests.patch(url=patch_uri, json=patch_args)
        response_text = r.text
        # prt(response_text)
        response_text = get_ALFKI()

    if cascade_update_test:
        test_name = "CASCADE UPDATE - ShippedDate"
        prt(f'\n\n\n{test_name}... verify Order.ShippedDate (2013-10-13) adjusts balance 2102-1086->1016, product onhand\n\n', test_name)
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
        response_text = r.text
        # prt(response_text)
        response_text = get_ALFKI()
        # prt(f'\nget_ALFKI: {response_text}')
        assert '"Balance": 1016.0' in response_text, f'Error - "Balance": 1026.0 not in this response:\n{response_text}'

        prt(f'\n{test_name}... return DB to original state\n')
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
        test_name = "CUSTOM SERVICE Bad Order"
        prt(f'\n\n\n{test_name}... post too-big an order to deliberately exceed credit - note multi-table logic chaining\n\n', test_name)
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
            f'Per the rules in ({get_project_dir()}/logic/declare_logic.py)\n\n'
            f'\n\nNote: Log is truncated by default; override as desired in api_logic_server_run.py')


if __name__ == "__main__":
    server_tests("localhost", "5656", "v0")

    # todo - empty order test, credit-limit from Order Detail change