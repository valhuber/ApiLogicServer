
## How - Usage and Operation Overview
<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/architecture.png"></figure>
Logic Bank operates as shown above:

 1. **Automatic Configuration**

    a. Declare logic in `logic/declare_logic.py`.  Here is a [summary of the rule types](https://github.com/valhuber/LogicBank/wiki/Rule-Summary)
 
    b. The Basic Web App and JSON:API are already configured to load and execute this logic
    
    
 2. Basic Web App and JSON:API operate as usual: makes calls on `SQLAlchemy` for inserts, updates and deletes
    and issues `session.commit()`
      

 3. The **Logic Bank** engine handles SQLAlchemy `before_flush` events on
`Mapped Tables`, so executes on this ```session.commit()```
    

 4. The logic engine operates much like a spreadsheet:
    - **watch** for changes -  at the ___attribute___ level
    - **react** by running rules that referenced changed attributes, which can
    - **chain** to still other attributes that refer to
_those_ changes.  Note these might be in different tables,
providing automation for _multi-table logic_

Logic does not apply to updates outside SQLAlchemy,
nor to SQLAlchemy batch updates or unmapped sql updates.

Let's see how logic operates on a typical, multi-table transaction.

#### Logic Execution: Add Order - Watch, React, Chain

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/check-credit.png"></figure>


The `add_order` example illustrates how
__Watch / React / Chain__ operates to
check the Credit Limit as each OrderDetail is inserted:

1.  The `OrderDetail.UnitPrice` (copy, line 50) references Product, so inserts cause it to be copied
    
2.  `Amount` (formula, line 53) watches `UnitPrice`, so its new value recomputes `Amount`
    
3.  `AmountTotal` (sum, line 57) watches `Amount`, so `AmountTotal` is adjusted (more on adjustment, below)
    
4.  `Balance` (sum, line 61) watches `AmountTotal`, so it is adjusted
    
5.  And the Credit Limit constraint (line 65) is checked (exceptions are raised if constraints are violated, and the transaction is rolled back)
    
All of the dependency management to see which attributes have changed,
logic ordering, the SQL commands to read and adjust rows, and the chaining
are fully automated by the engine, based solely on the rules above.

#### Spreadsheet-like Automatic Reuse
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


#### Scalability: Automatic Prune / Optimize logic
Scalability requires more than clustering - SQLs must be pruned
and optimized.  For example, the balance rule:
* is **pruned** if only a non-referenced column is altered (e.g., Shipping Address)
* is **optimized** into a 1-row _adjustment_ update instead of an
expensive SQL aggregate

For more on how logic automates and optimizes multi-table transactions,
[click here](https://github.com/valhuber/LogicBank/wiki#scalability-automatic-pruning-and-optimization).

#### Ordering: automatic for derivations, with control for actions and constraints
The system parses your _derivation rules_ to determine dependencies, and uses this to order execution.  This occurs once per session on activation, so rule declaration changes automatically determine a new order.  This is significant for iterative development and maintenance, eliminating the bulk of time spent determining _where do I insert this new logic_.

Constraint and action rules are executed in their declaration order.

#### Debugging

As shown on the [readme video](https://github.com/valhuber/ApiLogicServer/blob/main/README.md), you can:

1. Use your IDE to set breakpoints in rules, then examine `row` variables

2. Visualize logic execution with the _logic log._ Shown below, the console shows a line for each rule that fires, with the full row content (old/new values), indented to show multi-table logic chaining.

> Note: the logic log creates long lines.  You will generally therefore want to suppress word wrap.  Most IDEs and text editors have mechanisms to do this; if you are using the console, you may want to copy/paste the log into a text editor that can suppress word wrap.  This is defaulted in `api_logic_server_run.py` for sqlite databases.

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/log.png"></figure>

##### VSCode debugging
In VSCode, you must set `"redirectOutput": true` in your **Launch Configuration.**

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/no-line-wrap.png"></figure>

#### Extensibility

Not only can you define Python events, but you can add new rule _types_.  This is an advanced topic, [described here](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility)