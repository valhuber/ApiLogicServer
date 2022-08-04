Logic addresses backend multi-table constraint and derivation logic.  It's expressed in Python as rules, extensible with Python events as required.


## Problem: Code Explosion

In conventional approaches, such logic is **nearly half the system,** due to code explosion.  A typical design specification of 5 lines explodes into [200 lines of legacy code](https://github.com/valhuber/LogicBank/wiki/by-code){:target="_blank" rel="noopener"}).

<details markdown>
<summary>5 Line Spec Explodes into 200 Lines of Legacy Code... </summary>

Let's imagine we have a "cocktail napkin spec" for checking credit, shown (in blue) in the diagram below.  How might we enforce such logic?

* In UI controllers - this is the most common choice.  It's actually the worst choice, since it offers little re-use, and does not apply to non-UI cases such as API-based application integration.

* Centralized in the server - in the past, we might have written triggers, but a modern software architecture centralizes such logic in an App Server tier.  If you are using an ORM such as SQLAlchemy, you can _ensure sharing_ with `before_flush` events as shown below.

After we've determined _where_ to put the code, we then have to _write_ it.  Our simple 5 line cocktail napkin specification explodes into [200 lines of legacy code](https://github.com/valhuber/LogicBank/wiki/by-code){:target="_blank" rel="noopener"}):

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/rules-vs-code.png"></figure>

It's also incredibly repetitive - you often get the feeling you're doing the same thing over and over.

And you're right.  It's because backend logic follows patterns of "what" is supposed to happen.
And your code is the "how". 
</details>


## Solution: Rules are an Executable Design

API Logic -- unique to API Logic Server -- consists of __Rules, extensible with Python.__  

> Rules typically automate over **95% of such logic,** and are **40X more concise**.  Rules are conceptually similar to [spreadsheet cell formulas](../Logic-Operation/#basic-idea-like-a-spreadsheet).

For this typical check credit design (in blue), the __5 rules shown below (lines 64-79) represent the same logic as [200 lines of code](https://github.com/valhuber/LogicBank/wiki/by-code){:target="_blank" rel="noopener"}__:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/5-rules-cocktail.png?raw=true"></figure>


<details markdown>

  <summary>See the code here</summary>
```python
"""
Logic Design ("Cocktail Napkin Design") for User Story Check Credit
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

&nbsp;


## Declare, Extend, Manage

Use standard tools - standard language (Python), IDEs, and tools as described below.

### Declare: Python

Rules are declared in Python, using your IDE as shown above.

#### Code Completion

Your IDE code completion services can aid in discovering logic services.  There are 2 key elements:

1. Discover _rules_ by `Rule.`
2. Discovery _logic services_ made available through `logic_row`

  > If these aren't working, ensure your `venv` setup is correct - consult the [Trouble Shooting](../Troubleshooting#code-completion-fails) Guide.

You can find examples of these services in the sample `ApiLogicProject`.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/venv.png?raw=true"></figure>


### Extend: Python

While 95% is certainly remarkable, it's not 100%.  Automating most of the logic is of no value unless there are provisions to address the remainder.

That provision is standard Python, provided as standard events (lines 84-100 in the first screen shot above).  This will be typically be used for non-database oriented logic such as files and messages, and for extremely complex database logic.

### Manage: Your IDE, SCCS

The screen shot above illustrates you use your IDE (e.g., VSCode, PyCharm) to declare logic using Python, with all the familiar features of code completion and syntax high-lighting.  You can also use the debugger, and familiar Source Code Control tools such as `git`.


#### Debugging

As shown on the [readme video](https://github.com/valhuber/ApiLogicServer/blob/main/README.md), you can:

1. Use your IDE to set breakpoints in rules, then examine `row` variables

2. Visualize logic execution with the _logic log._ Shown below, the console shows a line for each rule that fires, with the full row content (old/new values), indented to show multi-table logic chaining.

> Note: the logic log creates long lines.  You will generally therefore want to suppress word wrap.  Most IDEs and text editors have mechanisms to do this; if you are using the console, you may want to copy/paste the log into a text editor that can suppress word wrap.  This is defaulted in `api_logic_server_run.py` for sqlite databases.

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/log.png"></figure>

###### VSCode debugging
In VSCode, set `"redirectOutput": true` in your **Launch Configuration.**  This directs logging output to the Debug Console, where it is not word-wrapped (word-wrap obscures the multi-table chaining).

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/no-line-wrap.png"></figure>


&nbsp;

## Key Aspects of Logic

While conciseness is the most immediately obvious aspect of logic, rules provide deeper value as summarized below.

| Concept | Rule Automation | Why It Matters|
| :--- |:---|:---|
| Re-use | Automatic re-use over all resources and actions | __Velocity / Conciseness:__ Eliminates logic replication over multiple UI controllers or services. |
| Invocation | Automatic logic execution, on referenced data changes |__Quality:__ Eliminates the _"code was there but not called"_ problem.<br><br>Rules are _active,_ transforming ‘dumb’ database objects into _smart_ business objects |
| Execution Order | Automatic ordering based on dependencies |__Maintenance:__ Eliminates the _"where do I insert this code"_ problem - the bulk of maintenance effort. |
| Dependency Management | Automatic chaining |__Conciseness:__ Eliminates the code that tests _"what's changed"_ to invoke relevant logic |
| Persistence | Automatic optimization |__Performance:__ Unlike Rete engines which have no concept of old values, transaction logic can prune rules for unchanged data, and optimize for adjustment logic based on the difference between old/new values.  This can literally result in sub-second performance instead of multiple minutes, and can be tuned without recoding.. |

See also the [FAQs](../FAQ-RETE).


### Automatic Reuse
Just as a spreadsheet reacts
to inserts, updates and deletes to a summed column,
rules automate _adding_, _deleting_ and _updating_ orders.
This is how 5 rules represent the same logic as 200 lines of code.

Our cocktail napkin spec is really nothing more than a set of spreadsheet-like rules that govern how to derive and constrain our data.  And by conceiving of the rules as associated with the _data_ (instead of a UI button), rules conceived for Place Order _automatically_ address these related transactions:

*   add order
* [**Ship Order**](https://github.com/valhuber/LogicBank/wiki/Ship-Order) illustrates *cascade*, another form of multi-table logic
*   delete order
*   assign order to different customer
*   re-assign an Order Detail to a different Product, with a different quantity
*   add/delete Order Detail


### Scalability: Prune and Optimize
Scalability requires more than clustering - SQLs must be pruned
and optimized.  For example, the balance rule:

* is **pruned** if only a non-referenced column is altered (e.g., Shipping Address)
* is **optimized** into a 1-row _adjustment_ update instead of an
expensive SQL aggregate

For more on how logic automates and optimizes multi-table transactions,
[click here](https://github.com/valhuber/LogicBank/wiki#scalability-automatic-pruning-and-optimization).

### Automatic Ordering

The system parses your _derivation rules_ to determine dependencies, and uses this to order execution.  This occurs once per session on activation, so rule declaration changes automatically determine a new order.  

This is significant for iterative development and maintenance, eliminating the bulk of time spent determining _where do I insert this new logic_.

#### Control for actions and constraints
Constraint and action rules are executed in their declaration order.
