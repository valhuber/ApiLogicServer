This describes how to use Logic; for more information, [see here](https://apilogicserver.github.io/Docs/Logic-Why).

&nbsp;

## Examples      
Examples from tutorial project:
* Examples drawn from [tutorial project](https://github.com/ApiLogicServer/demo/blob/main/logic/declare_logic.py)
* Use Shift + "." to view in project mode

&nbsp;

### Multi-Table Derivations

Balance automatically *adjusted* (*not* a sql `select sum`) iff:
* Order insert/delete, or
* AmountTotal or ShippedDate or CustomerID changes
```python
    Rule.sum(derive=models.Customer.Balance,
            as_sum_of=models.Order.AmountTotal,
            where=lambda row: row.ShippedDate is None)
```

&nbsp;

### Constraints: lambda or function

**As a lamda:**
```python
    Rule.constraint(validate=models.Customer,
        as_condition=lambda row: row.Balance <= row.CreditLimit,
        error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
```

**Or, as a function**
```python
    def check_balance(row: models.Customer, old_row: models.Customer, logic_row: LogicRow):
        if logic_row.ins_upd_dlt != "dlt":  # see also: logic_row.old_row
            return row.Balance <= row.CreditLimit
        else:
            return True

    Rule.constraint(validate=models.Customer,
        calling=check_balance,
        error_msg=f"balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
```

&nbsp;

### Events
```python
    def congratulate_sales_rep(row: models.Order, old_row: models.Order, logic_row: LogicRow):
        pass  # event code here - sending email, messages, etc.

    Rule.commit_row_event(on_class=models.Order, calling=congratulate_sales_rep)
```

&nbsp;

## LogicRow: old_row, verb, etc

A key argument to functions is `logic_row`:

* **Wraps row and old_row,** plus methods for insert, update and delete - rule enforcement

* **Additional instance variables:** ins_upd_dlt, nest_level, session, etc.

* **Helper Methods:** are_attributes_changed, set_same_named_attributes, get_parent_logic_row(role_name), get_derived_attributes, log, etc

Here is an example:

```python
"""
    STATE TRANSITION LOGIC, using old_row
"""
def raise_over_20_percent(row: models.Employee, old_row: models.Employee, logic_row: LogicRow):
    if logic_row.ins_upd_dlt == "upd" and row.Salary > old_row.Salary:
        return row.Salary >= Decimal('1.20') * old_row.Salary
    else:
        return True

Rule.constraint(validate=models.Employee,
                calling=raise_over_20_percent,
                error_msg="{row.LastName} needs a more meaningful raise")
```

Note the `log` method, which enables you to write row/old_row into the log with a short message:

```python
logic_row.log("no manager for this order's salesrep")
```

&nbsp;

## Declarative Logic: Important Notes

Logic *declarative*, which differs from conventional *procedural* logic:

1. **Automatic Invocation:** you don't call the rules; they execute in response to updates (via SQLAlchemy events).

2. **Automatic Ordering:** execution is ordered based on system-discovered depencencies.

These simplify maintenance / iteration: you can be sure new logic is always called, in the correct order.

&nbsp;

## Debugging

Debug rules using **system-generated logic log** and your **IDE debugger**; for more information, [see here](https://apilogicserver.github.io/Docs/Logic-Use).

&nbsp;

### Using the debugger

Use the debugger as shown below.  Note you can stop in lambda functions.

![Logic Debugger](https://apilogicserver.github.io/Docs/images/logic/logic-debug.png)

&nbsp;

### Logic Log

Logging is performed using standard Python logging, with a logger named `logic_logger`.  Use `info` for tracing, and `debug` for additional information (e.g., all declared rules are logged).

In addition, the system logs all rules that fire, to aid in debugging.  Referring the the screen shot above:

*   Each line represents a rule execution, showing row state (old/new values), and the _{reason}_ that caused the update (e.g., client, sum adjustment)
*   Log indention shows multi-table chaining

&nbsp;

