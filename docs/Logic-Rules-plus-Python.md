Logic automation is a _unique_ answer to a significant and unaddressed problem - the automation gap:

> For transaction systems, backend constraint and derivation logic is often nearly *half* the system.  It's the iceberg under the surface of the API.

> While there are varying degrees of front-end automation, **back-end logic is not addressed** by conventional approaches of *"your code goes here"*.

API Logic Server uses [Logic Bank](https://github.com/valhuber/logicbank#readme) to automate update transaction logic - multi-table derivations, constraints, and actions such as sending mail or messages.

Logic consists of both:

* **Rules - 40X** more concise using a spreadsheet-like paradigm, and

* **Python - control and extensibility,** using standard tools and techniques


&nbsp;&nbsp;&nbsp;

# TL;DR - Like a Spreadsheet

Rules are spreadsheet-like expressions for multi-table derivations and constraints.  For example (not actual syntax):

    The Customer Balance is the sum of the unshipped Order AmountTotals

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/like-a-spreadsheet.png?raw=true"></figure>

The list of rules is short, easily learned in an hour.  To see the rules, [click here.](https://github.com/valhuber/LogicBank/wiki/Examples)

Their power lies in _chaining_, as shown by the examples in the link.  Just like in a spreadsheet.

&nbsp;&nbsp;&nbsp;

# Background: Why, What, How

This article contains:

* [Why](#why---simple-cocktail-napkin-spec-explodes-into-massive-legacy-code) - problems addressed
* [What](#what---declare-spreadsheet-like-rules---40x-more-concise) - what are spreadsheet-like rules
* [How](#how---usage-and-operation-overview) - usage / operation overview, including
  * [Example - add order](#logic-execution-add-order---watch-react-chain) - sample transaction execution, reuse and scalability


## Why - Velocity, Quality, Agility, Performance

If you've coded backend database logic - multi-table derivations and constraints -
you know how much work it is, and how tedious.  Whether you code it in
triggers and stored procedures, in ORM events, or UI controllers, it's a lot:
typically nearly half the effort for a database project.

It's also incredibly repetitive - you often get the feeling you're doing the same thing over and over.

And you're right.  It's because backend logic follows patterns of "what" is supposed to happen.
And your code is the "how".  

Declarative logic addresses this by automating the _why_ with spreadsheet-like rules that are 40x more concise than code.  Conciseness can obviously improve velocity, but ___declarative logic___ - automatically re-used, invoked, ordered and optimized - can dramatically improve quality and accelerate iteration / maintenance cycles:

| Concept | Rule Automation | Why It Matters|
| :--- |:---|:---|
| Re-use | Automatic re-use over all resources and actions | __Velocity / Conciseness:__ Eliminates logic replication over multiple UI controllers or services. |
| Invocation | Automatic logic execution, on referenced data changes |__Quality:__ Eliminates the _"code was there but not called"_ problem.<br><br>Rules are _active,_ transforming ‘dumb’ database objects into _smart_ business objects |
| Execution Order | Automatic ordering based on dependencies |__Maintenance:__ Eliminates the _"where do I insert this code"_ problem - the bulk of maintenance effort. |
| Dependency Management | Automatic chaining |__Conciseness:__ Eliminates the code that tests _"what's changed"_ to invoke relevant logic |
| Persistence | Automatic optimization |__Performance:__ Unlike Rete engines which have no concept of old values, transaction logic can prune rules for unchanged data, and optimize for adjustment logic based on the difference between old/new values.  This can literally result in sub-second performance instead of multiple minutes, and can be tuned without recoding.. |

Logic Bank was designed to make the cocktail napkin spec _executable_.

### Metrics: 95% at 40X

In most transactional database systems, backend logic accounts for nearly half the code.

In past rule implementations addressing moderate-sized systems (typically consisting of 50-1000 tables):

* rules automate well over 95% of the logic.


* rules are 40x more concise than code.  We'll explore a typically complex multi-table transaction below; [here's the code vs. rules comparison](https://github.com/valhuber/LogicBank/wiki/by-code).

### Complexity: automate 95%, standard language for rest

The rule language is simple, by design.  Here is a [summary of the rule types](https://github.com/valhuber/LogicBank/wiki/Rule-Summary) - under a dozen.  The rules are deceptively simple, achieving power through chaining.

So, how do rules address complexity?

* The underlying design objective is _not to automate every problem_.  That would lead to a large set of rules that is difficult to understand and use.


* Instead, the focus is on _value,_ by automating the __most common__ cases (the 95%), with value noted above for quality, agility and performance.

While 95% is certainly remarkable, it's not 100%.  Automating most of the logic is of no value unless there are provisions to address the remainder.

That provision is standard Python, provided as standard events.  This will be typically be used for non-database oriented logic such as files and messages, and for extremely complex database logic.

## What - Declare Spreadsheet-like Rules - 40X More Concise
So, what _is_ declarative logic.  Let's review a representatively complex example.

### Current Approach - Simple Cocktail-Napkin Spec Explodes into Massive Legacy Code

Let's imagine we have a "cocktail napkin spec" shown (in blue) in the diagram below.  How might we enforce such logic?

* In UI controllers - this is the most common choice.  It's actually the worst choice, since it offers little re-use, and does not apply to non-UI cases such as API-based application integration.
* Centralized in the database - in the past, we might have written triggers, but a modern software architecture centralizes such logic in an App Server tier.  If you are using an ORM such as SQLAlchemy, you can _ensure sharing_ with `before_flush` events as shown below

After we've determined _where_ to put the code, we then have to _write_ it.  Our simple cocktail napkin specification explodes into a massive amount of legacy code:

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/rules-vs-code.png"></figure>

### Logic is 40x more concise
Logic Bank introduces rules that are 40X more concise than legacy code.
The 5 rules below (lines 40-49) express the same logic as 200 lines of code [**(see them here)**](https://github.com/valhuber/LogicBank/wiki/by-code).  That's because rules are all about "what"
-- spreadsheet-like expressions that automate the tedious "how":

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/5-rules-cocktail.png?raw=true"></figure>

### Standard Python - Declare, Extend, Manage
Logic Bank is fully integrated with Python:
* **Declare** rules in Python as shown above (more details in How, below)
* **Extend** rules with Python (rule on line 51 invokes the Python function on line 32)
* **Manage** logic using your existing IDE (PyCharm, VSCode etc for code completion, debugging, etc),
and source control tools and procedures


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

&nbsp;&nbsp;&nbsp;

# Logic Perspective

## Technology Perspective
Rule execution is via a _transaction logic_ engine, a complementary technology to traditional RETE engines.  The [transaction logic engine](https://github.com/valhuber/LogicBank/wiki/Rules-Engines) is specifically designed to optimize integrity and performance for transactional logic, which is not possible in RETE engines. See [here](https://github.com/valhuber/LogicBank/wiki/Logic-Walkthrough) for more information on their operation.

## An Agile Perspective
The core tenant of agile is

    Working software, driving collaboration, for rapid iterations

Here's how rules can help.

#### Working Software _Now_
The examples above illustrate how just a few rules can replace 
[pages of code](examples/nw/logic/legacy).

#### Collaboration: Running Screens - Admin App

Certainly business users are more easily able to
read rules than code.  But still, rules are
pretty abstract.

Business users relate best to actual working pages -
_their_ interpretation of working software.
The Admin App builds pages in moments.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/run-admin-app.png?raw=true"></figure>


#### Iteration - Automatic Ordering
Rules are _self-ordering_ - they recognize their interdependencies,
and order their execution and database access (pruning, adjustments etc)
accordingly.  This means:

* order is independent - you can state the rules in any order
and get the same result

* maintenance is simple - just make changes, additions and deletions,
the engine will reorganize execution order and database access, automatically


# Next Steps

### Explore Examples

Here some [examples](https://github.com/valhuber/LogicBank/wiki/Examples) that illustrate how to use rules, and how they can address complex transactions.
