## TL;DR: no - optimized for transactions

The API Logic Server engine is not based on the RETE algorithm.  These technolgies are complemetarty:

* RETE is appropriate for Decision Logic, where there are no presumptions about a database

* API Logic Server optimizes performance, often by several orders of magnitude, since it can prune and optimize rule execution based on comparing the proposed / old state of the database.

&nbsp;

---

## Key Differences in Rules Engines: Process, Decision, Transaction
Let's consider these rule technologies in the light of the following requirements:


#### Transaction Logic Requirements

| Category |      Consideration    |
| ------------- | ------------- |
| **Scalable** | Rules should minimize SQL overhead, _automatically_ |
| **Extensible** | Developers must be able to extend rule-based logic |
| **Manageable** | Developers must be able to use existing developer tools and procedures for code editing, debugging, code management, etc |
| **Integrity** | The system should ensure that *all* the rules are consistently enforced, in *all* cases |
| **Architecture** | Logic should _automatically_ enforced over all apps and APIs |


#### Process Rules

Such rules are typically graphs governing problem areas such as work flow and
data flow integration.  These are completely appropriate applications.

Process rules are not well suited to highly interdependent transaction logic:
* they are user ordered, so logic changes require the diagrams be redesigned
* they are not concise - a "flowchart" of thousands of lines of procedural logic
is actually less readable than code.

Transaction and process rules are synergistic:
* process diagrams may need to update rows, leveraging transaction logic
* transaction logic may need to start processes ("start order process"),
or resume them ("order is approved - execute next steps").

#### Decision Rules

Decision rules look virtually identical to transaction rules -
a set of chained derivations.  The difference is in the fundamental
interface:
* logic engine processes rows changed in a transaction
   * logic operation begins by obtaining _old_ values of these rows
   * these enable pruning and optimization (discussed below)
   * old_rows also enable state transition semantics
      * e.g., _all raises must exceed 10%_
   (one of our favorite rules)
* decision logic processes an array of objects (rows),
and the name of the RuleSet to run

Decision engines _cannot_ make presumptions about old rows,
so when they encounter a rule like `balance is sum of order amounts`,
it has _no choice_ but to read all the Orders (and each of
their OrderDetails).

> This is fine for a single-user "what-if" request.  But
> for multi-user transaction processing, this can
> reduce performance by __multiple orders of magnitude.__

We also note that decision logic is _explicitly called_.  That
means that you need to audit _all_ of the accessing code
to verify the logic is enforced.  Transaction logic, by contrast,
ensures that all sqlalchemy access enforces the logic.

That said, these technologies are also synergistic:

* You can invoke Decision Logic using Python in transaction logic rules

#### Transaction Rules
This implementation is a Transaction Rules Engine:
rule execution is bound into update processing.

| Category |      Consideration    | Transaction Logic |
| ------------- | ------------- | ----------- |
| **Scalable** | Rules should minimize SQL overhead, _automatically_ | Old row access enables pruning and sql optimizations (see below) |
| **Extensible** | Developers must be able to extend rule-based logic | Many rules (events, constraints) invoke Python, providing access to all that entails |
| **Manageable** | Developers must be able to use existing developer tools and procedures for code editing, debugging, code management, etc | Rules are Python code - use standard editors (with code completion), debuggers, and source code control systems and procedures |
| **Integrity** | The system should ensure that *all* the rules are consistently enforced, in *all* cases | All ORM access enforces the rules |
| **Architecture** | Logic should _automatically_ enforced over all apps and APIs | Logic enforcement is factored out of UI controllers, so shared over all apps and APIs |

##### Multi-Table Logic Execution
Let's look more carefully at how the
__watch__, __react__ and __chain__ logic
operates for multi-table transactions.
Transactional systems can leverage the presumption that
a set of updates is being applied to an _existing_ database:

* each updated row has an _existing_ row on disk - the _old values_

* the system can compare the old values to the new update values, and

   1. Prune the rules that do not apply

   1. And when the rules must be run, the declarative nature of rules enables the system to execute the rules in any manner that returns the correct result.  In particular, the system can avoid expensive aggregate queries, and use the old/new delta to compute a 1-row adjustment to the parent row.

For example, imagine you need to compute the balance for the credit limit check.  You need to add all the order totals (an expensive SQL `sum`).  But it’s worse - the order total _itself_ is a summed field, so you need to add all of those too.

If a customer has thousands of orders, each with thousands of items, this will be painfully slow.

But if the system leverages the old/new to make an adjustment update, an order of $50 simply means _”add 50 to the existing balance”_ - no need to aggregate the totals.
 
##### Adjustments - sum / counts adjusted in 1 row updates, not expensive aggregate SQLs
Rollups provoke an important design choice: store the aggregate,
or sum things on the fly.  Here, the stored aggregates are `Customer.Balance`, and `Order.AmountTotal`
(a *chained* aggregate).  There are good cases to be made for both approaches:

   - **Sum on the fly** - use sql `select sum` queries to aggregate child data as required.
   This eliminates consistency risks with storing redundant data
   (i.e, the aggregate becomes invalid if an application fails to
   adjust it in *all* of the cases).
   
   - **Stored Aggregates** - a good choice when data volumes are large, and / or chain,
   since the application can **adjust** (make a 1 row update) the aggregate based on the
   *delta* of the children.

This design decision can dominate application coding.  It's nefarious,
since data volumes may not be known when coding begins.  (Ideally, this can be
a "late binding" decision, like a sql index.)

The logic engine uses the **Stored Aggregate** approach.  This optimizes
multi-table update logic chaining, where updates to 1 row
trigger updates to other rows, which further chain to still more rows.


##### Pruning

Pruning was core to changing Order dates:

* `DueDate` had no dependencies, so all the logic for adjusting Customers and cascading OrderDetails was pruned.

* Contrast this to the multiple rows retrieved / update when `ShippedDate` is changed.