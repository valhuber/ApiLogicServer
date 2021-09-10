import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging

app_logger = logging.getLogger("api_logic_server_app")
app_logger.info("logic/declare_logic.py - importing declare_logic")

def declare_logic():
    """
    Logic declared here, using code completion.

    This logic pre-created for default database, nw.sqlite.
        You would normally declare your *own* rules, using code completion.
        For details on these rules, see https://github.com/valhuber/LogicBank/wiki/Examples

    This logic is *activated* in api_logic_server_run.py:
        LogicBank.activate(session=session, activator=logic_bank.declare_logic, constraint_event=constraint_handler)

    Logic *runs* in response to transaction commits,
      for multi-table derivations and constraints,
      and events such as sending messages or mail
        it consists of spreadsheet-like Rules and Python code

    Rules operate much like a spreadsheet:
        Watch, for changes in referenced values
        React, by recomputing value
        Chain, to any referencing rules, including other tables
            SQL is automated, and optimized (e.g., adjust vs. select sum)

    Rules are automatically invoked, with
    execution ordered per their dependencies

    These 5 rules apply to all transactions (automatic re-use), eg.
        * place order
        * change Order Detail product, quantity
        * add/delete Order Detail
        * ship / unship order
        * delete order
        * move order to new customer, etc
    This reuse is how 5 rules replace 200 lines of legacy code: https://github.com/valhuber/LogicBank/wiki/by-code

    Rules are listed below to best illustrate chaining
    """

    # get Product Price (e,g., on insert, or ProductId change)
    Rule.copy(derive=models.OrderDetail.UnitPrice,
              from_parent=models.Product.UnitPrice)
    # compute price * qty
    Rule.formula(derive=models.OrderDetail.Amount,
                 as_expression=lambda row: row.UnitPrice * row.Quantity)

    # adjust AmountTotal iff Amount changes
    Rule.sum(derive=models.Order.AmountTotal,
             as_sum_of=models.OrderDetail.Amount)

    # adjust Balance iff AmountTotal or ShippedDate or CustomerID changes
    Rule.sum(derive=models.Customer.Balance,
             as_sum_of=models.Order.AmountTotal,
             where=lambda row: row.ShippedDate is None)  # adjusts - *not* a sql select sum...
    Rule.constraint(validate=models.Customer,
                    as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")

    """
        Demonstrate that logic == rules + Python
    """
    def congratulate_sales_rep(row: models.Order, old_row: models.Order, logic_row: LogicRow):
        """ demonstrate that logic == rules, plus Python """
        if logic_row.ins_upd_dlt == "ins":  # logic engine fills parents for insert
            sales_rep = row.Employee
            if sales_rep is None:
                logic_row.log("no salesrep for this order")
            else:
                logic_row.log(f'Hi, {sales_rep.Manager.FirstName} - '
                              f'Congratulate {sales_rep.FirstName} on their new order')

    Rule.commit_row_event(on_class=models.Order, calling=congratulate_sales_rep)

    """
        More complex rules follow - see: https://github.com/valhuber/LogicBank/wiki/Examples
    """

    Rule.formula(derive=models.OrderDetail.ShippedDate, as_exp="row.Order.ShippedDate")

    def units_in_stock(row: models.Product, old_row: models.Product, logic_row: LogicRow):
        result = row.UnitsInStock - (row.UnitsShipped - old_row.UnitsShipped)
        return result
    Rule.sum(derive=models.Product.UnitsShipped, as_sum_of=models.OrderDetail.Quantity,
             where="row.ShippedDate is not None")
    Rule.formula(derive=models.Product.UnitsInStock, calling=units_in_stock)

    Rule.count(derive=models.Customer.UnpaidOrderCount, as_count_of=models.Order,
             where=lambda row: row.ShippedDate is None)  # *not* a sql select sum...

    Rule.count(derive=models.Customer.OrderCount, as_count_of=models.Order)

    def raise_over_20_percent(row: models.Employee, old_row: models.Employee, logic_row: LogicRow):
        if logic_row.ins_upd_dlt == "upd" and row.Salary != old_row.Salary:
            return row.Salary >= Decimal('1.20') * old_row.Salary
        else:
            return True

    Rule.constraint(validate=models.Employee,
                    calling=raise_over_20_percent,
                    error_msg="{row.LastName} needs a more meaningful raise")

    def audit_by_event(row: models.Employee, old_row: models.Employee, logic_row: LogicRow):
        tedious = False  # tedious code to repeat for every audited class
        if tedious:      # see instead the following rule extension - nw_copy_row
            if logic_row.are_attributes_changed([models.Employee.Salary, models.Employee.Title]):
                copy_to_logic_row = logic_row.new_logic_row(models.EmployeeAudit)
                copy_to_logic_row.link(to_parent=logic_row)
                copy_to_logic_row.set_same_named_attributes(logic_row)
                copy_to_logic_row.insert(reason="Manual Copy " + copy_to_logic_row.name)  # triggers rules...
                # logic_row.log("audit_by_event (Manual Copy) complete")

    Rule.commit_row_event(on_class=models.Employee, calling=audit_by_event)

    RuleExtension.copy_row(copy_from=models.Employee,
                           copy_to=models.EmployeeAudit,
                           copy_when=lambda logic_row: logic_row.are_attributes_changed([models.Employee.Salary, models.Employee.Title]))

    def handle_all(logic_row: LogicRow):
        row = logic_row.row
        if logic_row.ins_upd_dlt == "ins" and hasattr(row, "CreatedOn"):
            row.CreatedOn = datetime.datetime.now()
            logic_row.log("early_row_event_all_classes - handle_all sets 'Created_on"'')

    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)

    app_logger.debug("\n\nlogic/logic_bank.py: declare_logic complete")

