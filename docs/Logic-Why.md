Logic automation is a _unique_ answer to a significant and unaddressed problem - the automation gap:

> For transaction systems, backend multi-table constraint and derivation logic is often **nearly half the system.**  It's the iceberg under the surface of the API.

> While there are varying degrees of front-end "low code" automation, **back-end logic is not addressed** by conventional approaches of *"your code goes here"*.

API Logic Server uses [Logic Bank](https://github.com/valhuber/logicbank#readme) to automate update transaction logic - multi-table derivations, constraints, and actions such as sending mail or messages.

Logic consists of both:

* **Rules - 40X** more concise using a spreadsheet-like paradigm, and

* **Python - control and extensibility,** using standard tools and techniques

&nbsp;

## Problem: Code Explosion

Let's imagine we have a "cocktail napkin spec" shown (in blue) in the diagram below.  How might we enforce such logic?

* In UI controllers - this is the most common choice.  It's actually the worst choice, since it offers little re-use, and does not apply to non-UI cases such as API-based application integration.

* Centralized in the database - in the past, we might have written triggers, but a modern software architecture centralizes such logic in an App Server tier.  If you are using an ORM such as SQLAlchemy, you can _ensure sharing_ with `before_flush` events as shown below

After we've determined _where_ to put the code, we then have to _write_ it.  Our simple cocktail napkin specification explodes into a massive amount of legacy code:

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/rules-vs-code.png"></figure>

It's also incredibly repetitive - you often get the feeling you're doing the same thing over and over.

And you're right.  It's because backend logic follows patterns of "what" is supposed to happen.
And your code is the "how".  

&nbsp;

---

## Rules: Executable Design

Declarative logic addresses this by automating the _why_ with spreadsheet-like rules that are 40x more concise than code.  The 5 rules below (lines 64-79) express the same logic as 200 lines of code [**(see them here)**](https://github.com/valhuber/LogicBank/wiki/by-code).  That's because rules are all about "what"
-- spreadsheet-like expressions that automate the tedious "how":

<details>

  <summary>See the code here</summary>
```python
"""
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
```
</details>
<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/5-rules-cocktail.png?raw=true"></figure>

Logic Bank was designed to make the cocktail napkin spec _executable_.

Conciseness can obviously improve velocity, but ___declarative logic___ - automatically re-used, invoked, ordered and optimized - can dramatically improve quality and accelerate iteration / maintenance cycles:

| Concept | Rule Automation | Why It Matters|
| :--- |:---|:---|
| Re-use | Automatic re-use over all resources and actions | __Velocity / Conciseness:__ Eliminates logic replication over multiple UI controllers or services. |
| Invocation | Automatic logic execution, on referenced data changes |__Quality:__ Eliminates the _"code was there but not called"_ problem.<br><br>Rules are _active,_ transforming ‘dumb’ database objects into _smart_ business objects |
| Execution Order | Automatic ordering based on dependencies |__Maintenance:__ Eliminates the _"where do I insert this code"_ problem - the bulk of maintenance effort. |
| Dependency Management | Automatic chaining |__Conciseness:__ Eliminates the code that tests _"what's changed"_ to invoke relevant logic |
| Persistence | Automatic optimization |__Performance:__ Unlike Rete engines which have no concept of old values, transaction logic can prune rules for unchanged data, and optimize for adjustment logic based on the difference between old/new values.  This can literally result in sub-second performance instead of multiple minutes, and can be tuned without recoding.. |

&nbsp;

### Metrics: 95% at 40X

In most transactional database systems, backend logic accounts for nearly half the code.

In past rule implementations addressing moderate-sized systems (typically consisting of 50-1000 tables):

* rules automate well over 95% of the logic.

* rules are 40x more concise than code as shown above


### Complexity: Extensible with Python

While 95% is certainly remarkable, it's not 100%.  Automating most of the logic is of no value unless there are provisions to address the remainder.

That provision is standard Python, provided as standard events (lines 84-96 in the screen shot above).  This will be typically be used for non-database oriented logic such as files and messages, and for extremely complex database logic.

### Your IDE

The screen shot above illustrates you use your IDE (e.g., VSCode, PyCharm) to declare logic using Python, with all the familiar features of code completion and syntax high-lighting.  You can also use the debugger, and familiar tools such as `git`.
