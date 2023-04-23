from behave import *
import requests, pdb
import json
import test_utils

host = "localhost"
port = "5656"

@given('Employee 5 (Buchanan) - Salary 95k')
def step_impl(context):
    pass

@when('Patch Salary to 200k')
def step_impl(context):
    """
    Observe the logic log to see that it creates audit rows:

    1. **Discouraged:** you can implement auditing with events.  But auditing is a common pattern, and this can lead to repetitive, tedious code
    2. **Preferred:** approaches use [extensible rules](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility#generic-event-handlers).

    Generic event handlers can also reduce redundant code, illustrated in the time/date stamping `handle_all` logic.

    This is due to the `copy_row` rule.  Contrast this to the *tedious* `audit_by_event` alternative:

    <figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/salary_change.png?raw=true"></figure>

    > **Key Takeaway:** use **extensible own rule types** to automate pattern you identify; events can result in tedious amounts of code.

    """
    scenario_name = 'Audit Salary Change'
    test_utils.prt(f'\n\n\n{scenario_name}... alter salary, ensure audit row created (also available in shell script\n\n', scenario_name)
    patch_emp_uri = f'http://localhost:5656/api/Employee/5/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Salary": 200000,
                    "Id": 5},
                "type": "Employee",
                "id": 5
            }}
    r = requests.patch(url=patch_emp_uri, json=patch_args, headers= test_utils.login())
    context.response_text = r.text


@then("Salary_audit row created")
def step_impl(context):
    response_text = context.response_text
    assert '"Salary": 200000.0' in response_text or '"Salary":200000.0', \
        f'Error - "Salary": 200000.0 not in patch response:\n{response_text}'

    audit_uri = f'http://localhost:5656/api/EmployeeAudit/?' \
                'include=Employee&fields%5BEmployeeAudit%5D=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn&' \
                'page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn%2Cid'
    r = requests.get(url=audit_uri, headers= test_utils.login())
    response_text = r.text
    assert '"Salary": 200000.0' in response_text or '"Salary":200000.0', \
        f'Error - "Salary": 200000.0 not in audit response:\n{response_text}'

    test_utils.prt(f'\n then Salary_audit row created... return DB to original state\n')
    patch_emp_uri = f'http://localhost:5656/api/Employee/5/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Salary": 95000,
                    "Id": 5},
                "type": "Employee",
                "id": 5
            }}
    r = requests.patch(url=patch_emp_uri, json=patch_args, headers= test_utils.login())
    response_text = r.text



@when('Patch Salary to 96k')
def step_impl(context):
    """
    Observe the use of `old_row
    `
    > **Key Takeaway:** State Transition Logic enabled per `old_row`

    """
    scenario_name = 'Raise Must be Meaningful'
    test_utils.prt(f'\n\n\n{scenario_name}... alter salary, ensure audit row created (also available in shell script\n\n', scenario_name)
    patch_emp_uri = f'http://localhost:5656/api/Employee/5/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Salary": 96000,
                    "Id": 5},
                "type": "Employee",
                "id": 5
            }}
    r = requests.patch(url=patch_emp_uri, json=patch_args, headers= test_utils.login())
    context.response_text = r.text


@then("Reject - Raise too small")
def step_impl(context):
    response_text = context.response_text
    assert 'meaningful raise' in response_text, f'Error - "meaningful raise" not in response:\n{response_text}'


@when('Retrieve Employee Row')
def step_impl(context):
    """
    Observe the use of `old_row
    `
    > **Key Takeaway:** State Transition Logic enabled per `old_row`

    """
    scenario_name = 'Manage ProperSalary'
    test_utils.prt(f'\n\n\n{scenario_name}... Get Employee - verify contains virtual ProperSalary\n\n', scenario_name)
    header = test_utils.login()
    get_emp_uri = f'http://localhost:5656/api/Employee/5/'
    r = requests.get(url=get_emp_uri, headers= header)
    context.response_text = r.text


@then("Verify Contains ProperSalary")
def step_impl(context):
    response_text = context.response_text
    assert 'ProperSalary' in response_text, f'Error - "ProperSalary" not in response:\n{response_text}'
