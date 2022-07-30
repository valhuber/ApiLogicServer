import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging

app_logger = logging.getLogger("api_logic_server_app")
app_logger.debug("logic/declare_logic.py")

declared_rules = []  # rules are objects, you can collect them if you like (see @ end)

def declare_logic():
    """
    Declare, Activate and Run...

        *Declare* Logic here, using Python with code completion.

            This logic pre-created for default database, nw.sqlite.
                You would normally declare your *own* rules.
                For details on these rules, see
                    https://valhuber.github.io/ApiLogicServer/Logic/
                    https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/

        *Activation* occurs in api_logic_server_run.py:
            LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)

        Logic *runs* in response to transaction commits (typically via the API),
            for multi-table derivations and constraints,
            and events such as sending messages or mail
                it consists of spreadsheet-like Rules and Python code

    Rules operate much like a spreadsheet:
        Watch, for changes in referenced values
        React, by recomputing value
        Chain, to any referencing rules, including other tables (multi-table logic)
            SQL is automated, and optimized (e.g., adjust vs. select sum)

    Unlike procedural code, rules are declarative:
        automatically re-used                        (improves quality)
        automatically ordered per their dependencies (simplifies maintenance)
        automatically optimized (pruned, with sql optimizations such as adjust logic)

    These 5 rules apply to all transactions (automatic re-use), eg.
        * place order
        * change Order Detail product, quantity
        * add/delete Order Detail
        * ship / unship order
        * delete order
        * move order to new customer, etc
    This reuse is how 5 rules replace 200 lines of legacy code: https://github.com/valhuber/LogicBank/wiki/by-code


    Feature: Place Order
        Scenario: Bad Order Custom Service
            When Order Placed with excessive quantity
            Then Rejected per Credit Limit

    Logic Design ("Cocktail Napkin Design")
        Customer.Balance <= CreditLimit
        Customer.Balance = Sum(Order.AmountTotal where unshipped)
        Order.AmountTotal = Sum(OrderDetail.Amount)
        OrderDetail.Amount = Quantity * UnitPrice
        OrderDetail.UnitPrice = copy from Product
    """

    Rule.constraint(validate=models.Customer,       # logic design translates directly into rules
        as_condition=lambda row: row.Balance <= row.CreditLimit,
        error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")

    Rule.sum(derive=models.Customer.Balance,        # adjust iff AmountTotal or ShippedDate or CustomerID changes
        as_sum_of=models.Order.AmountTotal,
        where=lambda row: row.ShippedDate is None)  # adjusts - *not* a sql select sum...

    Rule.sum(derive=models.Order.AmountTotal,       # adjust iff Amount or OrderID changes
        as_sum_of=models.OrderDetail.Amount)

    Rule.formula(derive=models.OrderDetail.Amount,  # compute price * qty
        as_expression=lambda row: row.UnitPrice * row.Quantity)

    Rule.copy(derive=models.OrderDetail.UnitPrice,  # get Product Price (e,g., on insert, or ProductId change)
        from_parent=models.Product.UnitPrice)

    """
        Demonstrate that logic == Rules + Python (for extensibility)
    """
    def congratulate_sales_rep(row: models.Order, old_row: models.Order, logic_row: LogicRow):
        """ use events for sending email, messages, etc. """
        if logic_row.ins_upd_dlt == "ins":  # logic engine fills parents for insert
            sales_rep = row.Employee
            if sales_rep is None:
                logic_row.log("no salesrep for this order")
            elif sales_rep.Manager is None:
                logic_row.log("no manager for this order's salesrep")
            else:
                logic_row.log(f'Hi, {sales_rep.Manager.FirstName} - '
                              f'Congratulate {sales_rep.FirstName} on their new order')

    Rule.commit_row_event(on_class=models.Order, calling=congratulate_sales_rep)

    """
        More complex rules follow - see: 
            https://github.com/valhuber/LogicBank/wiki/Examples
            https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility
    """

    def units_in_stock(row: models.Product, old_row: models.Product, logic_row: LogicRow):
        result = row.UnitsInStock - (row.UnitsShipped - old_row.UnitsShipped)
        return result  # use lambdas for simple expressions, functions for complex logic (if/else etc)

    Rule.formula(derive=models.Product.UnitsInStock, calling=units_in_stock)  # compute reorder required

    Rule.sum(derive=models.Product.UnitsShipped,
        as_sum_of=models.OrderDetail.Quantity,
        where=lambda row: row.ShippedDate is None)

    Rule.formula(derive=models.OrderDetail.ShippedDate,  # unlike copy, referenced parent values cascade to children
        as_exp="row.Order.ShippedDate")


    Rule.count(derive=models.Customer.UnpaidOrderCount,
        as_count_of=models.Order,
        where=lambda row: row.ShippedDate is None)  # *not* a sql select sum...

    Rule.count(derive=models.Customer.OrderCount, as_count_of=models.Order)

    Rule.count(derive=models.Order.OrderDetailCount, as_count_of=models.OrderDetail)

    def raise_over_20_percent(row: models.Employee, old_row: models.Employee, logic_row: LogicRow):
        if logic_row.ins_upd_dlt == "upd" and row.Salary > old_row.Salary:
            return row.Salary >= Decimal('1.20') * old_row.Salary
        else:
            return True

    Rule.constraint(validate=models.Employee,
                    calling=raise_over_20_percent,
                    error_msg="{row.LastName} needs a more meaningful raise")

    def audit_by_event(row: models.Employee, old_row: models.Employee, logic_row: LogicRow):
        tedious = False  # tedious code to repeat for every audited class
        if tedious:      # see instead the following RuleExtension.copy_row below (you can create similar rule extensions)
            if logic_row.are_attributes_changed([models.Employee.Salary, models.Employee.Title]):
                copy_to_logic_row = logic_row.new_logic_row(models.EmployeeAudit)
                copy_to_logic_row.link(to_parent=logic_row)
                copy_to_logic_row.set_same_named_attributes(logic_row)
                copy_to_logic_row.insert(reason="Manual Copy " + copy_to_logic_row.name)  # triggers rules...

    Rule.commit_row_event(on_class=models.Employee, calling=audit_by_event)

    RuleExtension.copy_row(copy_from=models.Employee,
                           copy_to=models.EmployeeAudit,
                           copy_when=lambda logic_row: logic_row.are_attributes_changed([models.Employee.Salary, models.Employee.Title]))

    def clone_order(row: models.Order, old_row: models.Order, logic_row: LogicRow):
        if row.CloneFromOrder is not None and logic_row.nest_level == 0:
            which = ["OrderDetailList"]
            logic_row.copy_children(copy_from=row.parent,
                                    which_children=which)

    Rule.row_event(on_class=models.Order, calling=clone_order)

    def handle_all(logic_row: LogicRow):
        row = logic_row.row
        if logic_row.ins_upd_dlt == "ins" and hasattr(row, "CreatedOn"):
            row.CreatedOn = datetime.datetime.now()
            logic_row.log("early_row_event_all_classes - handle_all sets 'Created_on"'')

    time_stamp_rule = Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)
    declared_rules.append(time_stamp_rule)  # print ala api/customize_api#rules_report()
    
    app_logger.info("..logic/declare_logic.py (rules + code)")
