from behave import *
import requests, pdb
import json
import test_utils

host = "localhost"
port = "5656"

@given('Customer Account: VINET')
def step_impl(context):
    pass

@when('GET Orders API')
def step_impl(context):
    # pdb.set_trace() # I want to add a break point in here (for whatever reason)
    # todo - host and port hard-coded
    get_order_uri = f'http://localhost:5656/api/Order/?' \
                f'fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal' \
                f'&page%5Boffset%5D=0&page%5Blimit%5D=10&filter%5BId%5D=10248'
    r = requests.get(url=get_order_uri, headers= test_utils.login())
    response_text = r.text
    context.response_text = response_text
    assert True is not False

@then('VINET retrieved')
def step_impl(context):
    response_text = context.response_text
    assert "VINET" in response_text, f'Error - "VINET not in {response_text}'


@given('Department 2')
def step_impl(context):
    pass  # sample db should contain this - verify by test

@when('GET Department with SubDepartments API')
def step_impl(context):
    assert True is not False

@then('SubDepartments returned')
def step_impl(context):
        get_dept_uri = f'http://{host}:{port}/api/Department/2/?' \
                    f'include=DepartmentList%2CEmployeeList%2CEmployeeList1%2CDepartment' \
                    f'&fields%5BDepartment%5D=Id%2CDepartmentId%2CDepartmentName'
        r = requests.get(url=get_dept_uri, headers= test_utils.login())
        response_text = r.text
        result_data = json.loads(response_text)  # 'str' object has no attribute 'read'
        relationships = result_data["data"]["relationships"]
        relationships_department = relationships["Department"]
        relationships_department_list = relationships["DepartmentList"]
        ceo_check = relationships_department["data"]["id"]  # should be '1'
        ne_sales_check = relationships_department_list["data"][0]["id"]  # should be 4
        assert ceo_check == '1' and ne_sales_check == '4', \
            f'Error - "CEO not in Department or NE Sales not in DepartmentList: {response_text}'
