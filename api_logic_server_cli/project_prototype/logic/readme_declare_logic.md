This describes how to use Logic; for more information, [see here](https://apilogicserver.github.io/Docs/Logic-Why).

&nbsp;

## Examples      
Examples from tutorial project:
* Examples drawn from [tutorial project](https://github.com/ApiLogicServer/demo/blob/main/logic/declare_logic.py)
* Use Shift + "." to view in project mode

You can [find the rules here](https://apilogicserver.github.io/Docs/Logic).  Below, we explore the syntax of 3 typical rules.

&nbsp;

### 1. Multi-Table Derivations

This declares the Customer.Balance as the sum of the unshipped Order.AmountTotal:

```python
    Rule.sum(derive=models.Customer.Balance,
            as_sum_of=models.Order.AmountTotal,
            where=lambda row: row.ShippedDate is None)
```
It means the rule engine **watches** for these changes:
* Order inserted/deleted, or
* AmountTotal or ShippedDate or CustomerID changes

Iff changes are detected, the engine **reacts** by *adjusting* the Customer.Balance.  SQLs are [optimized](#declarative-logic-important-notes).

This would **chain** to check the Customers' Constraint rule, described below.

&nbsp;

### 2. Constraints: lambda or function

Constraints are multi-field conditions which must be true for transactions to succeed (else an exception is raised).  You can express the condition as a lambda or a function:

**As a lambda:**
```python
    Rule.constraint(validate=models.Customer,
        as_condition=lambda row: row.Balance <= row.CreditLimit,  # parent references are supported
        error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
```

**Or, as a function:**
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

### 3. Row Events: Extensible with Python

Events are procedural Python code, providing extensibility for declarative rules:
```python
    def congratulate_sales_rep(row: models.Order, old_row: models.Order, logic_row: LogicRow):
        pass  # event code here - sending email, messages, etc.

    Rule.commit_row_event(on_class=models.Order, calling=congratulate_sales_rep)
```
Note there are multiple kinds of events, so you can control whether they run before or after rule execution.  For more information, [see here](https://apilogicserver.github.io/Docs/Logic-Type-Constraint).

&nbsp;

## LogicRow: old_row, verb, etc

A key argument to functions is `logic_row`:

* **Wraps row and old_row,** plus methods for insert, update and delete - rule enforcement

* **Additional instance variables:** ins_upd_dlt, nest_level, session, etc.

* **Helper Methods:** are_attributes_changed, set_same_named_attributes, get_parent_logic_row(role_name), get_derived_attributes, log, is_inserted, etc

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

2. **Automatic Ordering:** you don't order the rules; execution order is based on system-discovered depencencies.

3. **Automatic Optimizations:** logic is optimized to reduce SQLs.

    * Rule execution is *pruned* if dependent attributes are not altered
    * SQL is optimized, e.g., `sum` rules operate by *adjustment*, not expensive SQL `select sum`

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

## How Logic works

*Activation* occurs in `api_logic_server_run.py`:
```python
    LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)
```

This installs the rule engine as a SQLAlchemy event listener (`before_flush`).  So, Logic *runs* automatically, in response to transaction commits (typically via the API).

Rules plug into SQLAlchemy events, and execute as follows:

| Logic Phase | Why It Matters |
|:-----------------------------|:---------------------|
| **Watch** for changes at the attribute level | Performance - Automatic Attribute-level Pruning |
| **React** by recomputing value | Ensures Reuse - Invocation is automatic<br>Derivations are optimized (e.g. *adjustment updates* - not aggregate queries) |
| **Chain** to other referencing data | Simplifies Maintenance - ordering is automatic<br>Multi-table logic automation |
