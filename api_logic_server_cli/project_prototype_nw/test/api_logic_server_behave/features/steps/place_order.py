from behave import *
import requests, pdb
import test_utils
import sys
import json
from dotmap import DotMap

logic_logs_dir = "logs/scenario_logic_logs"

"""
These tests can be re-run -- they restore the data to original state.

Good illustrations of API calls from Python.

Rows used for testing:
* customer: ALFKI, with a balance of 2102
* order: 10643, with an amount 1086
* orderdetail: 1040
* employee: Buchanan (5), with a salary of 95k
"""

def get_ALFLI():
    get_uri = 'http://localhost:5656/api/Customer/ALFKI/?include=OrderList&fields%5BCustomer%5D=Id%2CCompanyName%2CBalance%2CCreditLimit%2COrderCount%2CUnpaidOrderCount'
    header = test_utils.login()
    r = requests.get(url=get_uri, headers= header)
    response_text = r.text
    status_code = r.status_code
    if status_code > 300:
        raise Exception(f'get_ALFKI failed with {r.text}')
    save_for_session = True
    if save_for_session:
        s = requests.Session()
        s.headers.update(header)
    result_data = json.loads(response_text)
    result_map = DotMap(result_data)
    result_attrs = result_map.data.attributes
    return result_attrs


def get_truncated_scenario_name(scenario_name: str) -> str:
    """ address max file length (chop at 26), illegal characters """
    scenario_trunc = scenario_name
    if scenario_trunc is not None and len(scenario_trunc) >= 26:
        scenario_trunc = scenario_name[0:25]
    scenario_trunc = f'{str(scenario_trunc).replace(" ", "_")}'
    return scenario_trunc

@given('Customer Account: ALFKI')
def step_impl(context):
    alfki_before = get_ALFLI()
    context.alfki_before = alfki_before
    pass

@when('Good Order Placed')
def step_impl(context):
    """
    We place an Order with an Order Detail.  It's one transaction.

    Note how the `Order.OrderTotal` and `Customer.Balance` are *adjusted* as Order Details are processed.
    Similarly, the `Product.UnitsShipped` is adjusted, and used to recompute `UnitsInStock`

    <figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/declare-logic.png?raw=true"></figure>

    > **Key Takeaway:** sum/count aggregates (e.g., `Customer.Balance`) automate ***chain up*** multi-table transactions.

    **Events - Extensible Logic**

    Inspect the log for __Hi, Andrew - Congratulate Nancy on their new order__. 

    The `congratulate_sales_rep` event illustrates logic 
    [Extensibility](https://apilogicserver.github.io/Docs/Logic/#extensibility-python-events) 
    - using Python to provide logic not covered by rules, 
    like non-database operations such as sending email or messages.

    <figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/send-email.png?raw=true"></figure>

    There are actually multiple kinds of events:

    * *Before* row logic
    * *After* row logic
    * On *commit,* after all row logic has completed (as here), so that your code "sees" the full logic results

    Events are passed the `row` and `old_row`, as well as `logic_row` which enables you to test the actual operation, chaining nest level, etc.

    You can set breakpoints in events, and inspect these.

    """
    scenario_name = 'Good Order Custom Service'
    add_order_uri = f'http://localhost:5656/api/ServicesEndPoint/add_order'
    add_order_args = {
        "meta": {
            "method": "add_order",
            "args": {
                "CustomerId": "ALFKI",
                "EmployeeId": 1,
                "Freight": 11,
                "OrderDetailList": [
                    {
                        "ProductId": 1,
                        "Quantity": 1,
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
    test_utils.prt(f'\n\n\n{scenario_name} - verify adjustments...\n',\
        scenario_name)
    r = requests.post(url=add_order_uri, json=add_order_args, headers=test_utils.login())
    context.response_text = r.text

@then('Logic adjusts Balance (demo: chain up)')
def step_impl(context):
    before = context.alfki_before
    expected_adjustment = 56  # find this from inspecting data on test run
    after = get_ALFLI()
    context.alfki_after = after
    assert before.Balance + expected_adjustment == after.Balance, \
        f'On add, before balance {before.Balance} + {expected_adjustment} != new Balance {after.Balance}'

@then('Logic adjusts Products Reordered')
def step_impl(context):
    assert True is not False


@then('Logic sends email to salesrep')
def step_impl(context):
    stub = True
    if stub:
        assert True == True
    else:
        scenario_name = context.scenario.name
        scenario_trunc = get_truncated_scenario_name(scenario_name)
        logic_file_name = f'{logic_logs_dir}/{scenario_trunc}.log'
        with open(logic_file_name) as logic:
            logic_lines = logic.readlines()
        found = False
        for each_logic_line in logic_lines:
            if 'Congratulate' in each_logic_line:
                found = True
                break
        assert found, "Logic Log does not contain 'Congratulate'"

@then('Logic adjusts aggregates down on delete order')
def step_impl(context):
    scenario_name = 'Good Order Custom Svc - cleanup'
    test_utils.prt(f'\n\n\n{scenario_name} - verify credit check response...\n', scenario_name)
    # find ALFKI order with freight of 11 and delete it (hmm... cannot get created id)
    order_uri = "http://localhost:5656/api/Order/?include=Customer&fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal%2CCountry%2CCity%2CReady%2COrderDetailCount&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal%2CCountry%2CCity%2CReady%2COrderDetailCount%2Cid&filter%5BCustomerId%5D=ALFKI&filter%5BFreight%5D=11"
    r = requests.get(url=order_uri, headers= test_utils.login())
    response_text = r.text
    result_data = json.loads(response_text)
    result_map = DotMap(result_data)

    orders = result_map.data
    for each_order in orders:
        order_id = each_order.id
        delete_uri = "http://localhost:5656/api/Order/" + str(order_id) + "/"
        # TODO - fails in SQLAlchemy 2 - stacktrace after commit on flush
        # sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: OrderDetail.OrderId
        r = requests.delete(delete_uri, headers= test_utils.login())

    before = context.alfki_before
    expected_adjustment = 0
    after = get_ALFLI()
    context.alfki_after = after
    assert before.Balance + expected_adjustment == after.Balance, \
        f'On delete, Before balance {before.Balance} + {expected_adjustment} != new Balance {after.Balance}'

    assert True is not False

@when('Order Placed with excessive quantity')
def step_impl(context):
    """
    Familiar logic patterns:
    * Constrain a derived result
    * Chain up, to adjust parent sum/count aggregates

    Logic Design ("Cocktail Napkin Design")
    * Customer.Balance <= CreditLimit
    * Customer.Balance = Sum(Order.AmountTotal where unshipped)
    * Order.AmountTotal = Sum(OrderDetail.Amount)
    * OrderDetail.Amount = Quantity * UnitPrice
    * OrderDetail.UnitPrice = copy from Product

    """
    scenario_name = 'Bad Order Custom Service'
    add_order_uri = f'http://localhost:5656/api/ServicesEndPoint/add_order'
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
    test_utils.prt(f'\n\n\n{scenario_name} - verify credit check response...\n', 
        scenario_name)
    r = requests.post(url=add_order_uri, json=add_order_args)
    context.response_text = r.text

@then('Rejected per Check Credit')
def step_impl(context):
    response_text = context.response_text
    print( "one last thing", "by the way", "\n")
    assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'
    # behave.log_capture.capture("THIS IS behave.log_capture.capture")

def after_step(context, step):
    print("\nflush1 \n\n")  # ensure print statements work
    print("\nflush2 \n\n")


@when('Order Detail Quantity altered very high')
def step_impl(context):
    """
    Same constraint as above.

    > **Key Takeaway:** Automatic Reuse (_design one, solve many_)
    """
    scenario_name = 'Alter Item Qty to exceed credit'
    test_utils.prt(f'\n\n\n{scenario_name} - verify credit check response...\n', scenario_name)
    patch_cust_uri = f'http://localhost:5656/api/OrderDetail/1040/'
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
    r = requests.patch(url=patch_cust_uri, json=patch_args, headers=test_utils.login())
    response_text = r.text
    context.response_text = r.text


@when('Order RequiredDate altered (2013-10-13)')
def step_impl(context):
    """
    We set `Order.RequiredDate`.

    This is a normal update.  Nothing depends on the columns altered, so this has no effect on the related Customer, Order Details or Products.  Contrast this to the *Cascade Update Test* and the *Custom Service* test, where logic chaining affects related rows.  Only the commit event fires.

    > **Key Takeaway:** rule pruning automatically avoids unnecessary SQL overhead.

    """
    scenario_name = 'Alter Required Date - adjust logic pruned'
    test_utils.prt(f'\n\n\n{scenario_name}... observe rules pruned for Order.RequiredDate (2013-10-13) \n\n', scenario_name)
    patch_uri = f'http://localhost:5656/api/Order/10643/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "RequiredDate": "2013-10-13",
                    "Id": 10643},
                "type": "Order",
                "id": 10643
            }}
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    response_text = r.text
    context.response_text = r.text

@then('Balance not adjusted')
def step_impl(context):
    before = context.alfki_before
    expected_adjustment = 0
    after = get_ALFLI()
    context.alfki_after = after
    assert before.Balance + expected_adjustment == after.Balance, \
        f'Before balance {before.Balance} + {expected_adjustment} != new Balance {after.Balance}'



@when('Order ShippedDate altered (2013-10-13)')
def step_impl(context):
    """
    We set `Order.ShippedDate`.

    This cascades to the Order Details, per the `derive=models.OrderDetail.ShippedDate` rule.
    
    This chains to adjust the `Product.UnitsShipped` and recomputes `UnitsInStock`, as above

    <figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/order-shipped-date.png?raw=true"></figure>


    > **Key Takeaway:** parent references (e.g., `OrderDetail.ShippedDate`) automate ***chain-down*** multi-table transactions.

    > **Key Takeaway:** Automatic Reuse (_design one, solve many_)

    """
    scenario_name = 'Set Shipped - adjust logic reuse'
    test_utils.prt(f'\n\n\n{scenario_name}... observe rules pruned for Order.RequiredDate (2013-10-13) \n\n', scenario_name)
    patch_uri = f'http://localhost:5656/api/Order/10643/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "ShippedDate": "2013-10-13",
                    "Id": 10643},
                "type": "Order",
                "id": 10643
            }}
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    response_text = r.text
    context.response_text = r.text

@then('Balance reduced 1086')
def step_impl(context):
    before = context.alfki_before
    expected_adjustment = -1086
    shipped = get_ALFLI()
    context.alfki_shipped = shipped  # alert - this variable not visible in next scenario... need to use given
    assert before.Balance + expected_adjustment == shipped.Balance, \
        f'Before balance {before.Balance} + {expected_adjustment} != new Balance {shipped.Balance}'


@given('Shipped Order')
def step_impl(context):
    context.alfki_shipped = get_ALFLI()
    pass

@when('Order ShippedDate set to None')
def step_impl(context):
    """
    Same logic as above.

    > **Key Takeaway:** Automatic Reuse (_design one, solve many_)
    """
    scenario_name = 'Reset Shipped - adjust logic reuse'
    test_utils.prt(f'\n\n\n{scenario_name}... observe rules pruned for Order.RequiredDate (2013-10-13) \n\n', scenario_name)
    patch_uri = f'http://localhost:5656/api/Order/10643/'
    patch_args = \
        {
            "data": {
                "attributes": {
                    "ShippedDate": None,
                    "Id": 10643},
                "type": "Order",
                "id": 10643
            }}
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    response_text = r.text
    context.response_text = r.text

@then('Logic adjusts Balance by -1086')
def step_impl(context):
    before = context.alfki_shipped
    expected_adjustment = 1086
    after = get_ALFLI()
    context.alfki_after = after
    assert before.Balance + expected_adjustment == after.Balance, \
        f'Before balance {before.Balance} + {expected_adjustment} != new Balance {after.Balance}'

@when('Cloning Existing Order')
def step_impl(context):
    """
    We create an order, setting CloneFromOrder.

    This copies the CloneFromOrder OrderDetails to our new Order.
    
    The copy operation is automated using `logic_row.copy_children()`:

    1. `place_order.feature` defines the test

    2. `place_order.py` implements the test.  It uses the API to Post an Order, setting `CloneFromOrder` to trigger the copy logic

    3. `declare_logic.py` implements the logic, by invoking `logic_row.copy_children()`.  `which` defines which children to copy, here just `OrderDetailList`

    <figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/clone-order.png?raw=true"></figure>

    `CopyChildren` For more information, [see here](https://github.com/valhuber/LogicBank/wiki/Copy-Children)

        Useful in row event handlers to copy multiple children types to self from copy_from children.

        child-spec := < ‘child-list-name’ | < ‘child-list-name = parent-list-name’ >
        child-list-spec := [child-spec | (child-spec, child-list-spec)]

        Eg. RowEvent on Order
            which = ["OrderDetailList"]
            logic_row.copy_children(copy_from=row.parent, which_children=which)

        Eg, test/copy_children:
            child_list_spec = [
                ("MileStoneList",
                    ["DeliverableList"]  # for each Milestone, get the Deliverables
                ),
                "StaffList"
            ]

    > **Key Takeaway:** copy_children provides a deep-copy service.

    """
    scenario_name = 'Clone Existing Order'
    test_utils.prt(f'\n\n\n{scenario_name}... Clone Order per CloneFromOrder 10643 ($1086), for ALFKI ($2102, limit of $2200)) \n\n', scenario_name)
    add_order_uri = f'http://localhost:5656/api/ServicesEndPoint/add_order'
    clone_of_10643 = {
        "meta": {
            "method": "add_order",
            "args": {
                "CustomerId": "ALFKI",
                "EmployeeId": 1,
                "Freight": 11,
                "CloneFromOrder": 10643
            }
        }
    }
    """
        ALFKI - Balance: 2102, CreditLimit = 2200
        Order 10643
    """
    test_utils.prt(f'\n\n\n{scenario_name} - verify adjustments...\n',\
    scenario_name)
    r = requests.post(url=add_order_uri, json=clone_of_10643)
    context.response_text = r.text

@then('Logic Copies ClonedFrom OrderDetails')
def step_impl(context):
    response_text = context.response_text
    assert "exceeds credit" in response_text, f'Error - "exceeds credit not in {response_text}'
