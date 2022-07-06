## Logic Architecture

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/architecture.png"></figure>
Logic Bank operates as shown above:

 1. **Automatic Configuration**

    a. Declare logic in `logic/declare_logic.py`.  Here is a [summary of the rule types](../Logic)
 
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

## Basic Idea - Like a Spreadsheet

Rules are spreadsheet-like expressions for multi-table derivations and constraints.  For example (not actual syntax):

    The Customer Balance is the sum of the unshipped Order AmountTotals

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/like-a-spreadsheet.png?raw=true"></figure>

> You can imagine that the spreadsheet __watches__ for changes to referenced cells, __reacts__ by recomputing the cell, which may __chain__ to other cells.

&nbsp;

---

Let's see how logic operates on a typical, multi-table transaction.


## Watch, React, Chain

Let's consider a typical multi-table transaction.  Here is the 5 rule solution for check credit:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/5-rules-cocktail.png?raw=true"></figure>

As Order Details are inserted, the rule flow is shown below.

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/check-credit.png"></figure>


The `add_order` example illustrates how
__Watch / React / Chain__ operates to
check the Credit Limit as each Order Detail is inserted:

1.  The `OrderDetail.UnitPrice` (copy, line 78) references Product, so inserts cause it to be copied
    
2.  `Amount` (formula, line 75) watches `UnitPrice`, so its new value recomputes `Amount`
    
3.  `AmountTotal` (sum, line 72) watches `Amount`, so `AmountTotal` is adjusted (more on adjustment, below)
    
4.  `Balance` (sum, line 68) watches `AmountTotal`, so it is adjusted
    
5.  And the Credit Limit constraint (line 64) is checked (exceptions are raised if constraints are violated, and the transaction is rolled back)
    
All of the dependency management to see which attributes have changed,
logic ordering, the SQL commands to read and adjust rows, and the chaining
are fully automated by the engine, based solely on the rules above.

## Creating New Rule Types

Not only can you define Python events, but you can add new rule _types_.  This is an advanced topic, [described here](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility)

&nbsp;
