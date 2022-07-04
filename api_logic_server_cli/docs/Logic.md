Logic consists of both:

* **Rules - 40X** more concise using a spreadsheet-like paradigm, and

* **Python - control and extensibility,** using standard tools and techniques

&nbsp;

## Basic Idea - Rules Are Spreadsheet-Like Derivations

Rules are spreadsheet-like expressions for multi-table derivations and constraints.  For example (not actual syntax):

    The Customer Balance is the sum of the unshipped Order AmountTotals

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/like-a-spreadsheet.png?raw=true"></figure>

The list of rules is short, easily learned in an hour.  To see the rules, [click here.](#rules-summary)

Their power lies in _chaining_, as shown by the examples in the link.  Just like in a spreadsheet.

&nbsp;&nbsp;&nbsp;


## Rules Summary
The table shows excerpts only; see the ```nw``` sample for full syntax.

| Rule | Summary   | Example | Notes |
| :-------------: |:-------------:| :-----:| :-----:|
| Constraint     | Boolean function must be True<br>else transaction rolled back | ```row.Balance <= row.CreditLimit```<br>```row.Salary >= Decimal('1.20') * old_row.Salary``` | Multi-field<br>```old_row``` |
| Formula | Function computes column value | row.UnitPrice * row.Quantity<br>row.OrderHeader.ShippedDate | lambda, or function<br>Parent ```(OrderHeader)``` references |
| Sum | Derive parent-attribute as sum of designated child attribute; optional child qualification | ```Rule.sum(derive=Customer.Balance, as_sum_of=Order.AmountTotal,where=lambda row: row.ShippedDate is None)``` | Parent attribute can be hybrid (virtual)<br>scalable: pruning, adjustment |
| Count | Derive parent-attribute as count of child rows; optional child qualification | ```Rule.sum(derive=Customer.Balance, as_sum_of=Order.AmountTotal,where=lambda row: row.ShippedDate is None)``` | Parent attribute can be hybrid (virtual)<br>scalable: pruning, adjustment |
| Copy      | Child value set from Parent     | OrderDetail.ProductPrice = copy(Product.Price) | Unlike formula references, parent changes are not propagated<br>e.g, Order totals for Monday are not affected by a Tuesday price increase |
| Event      | Python Function    | on insert, call ```congratulate_sales_rep``` | See [Extensibility](Extensibility) for a information on early, row and commit events |
| Parent Check      | Ensure Parent row exists | Orders must have a Customer | See [Referential Integrity](Referential-Integrity) |
| Allocation      | Allocate a provider amount to recipients | allocate a payment to outstanding orders | See [Allocation](Sample-Project__Allocation) for an example |
| Copy Row      | Create child row by copying parent | audit Employee Salary changes to EmployeeAudit | See [Rule Extensibility](Rule-Extensibility) |

&nbsp;

## Extensibility - Python Events

TBD, using your IDE

### Standard Python - Declare, Extend, Manage
Logic Bank is fully integrated with Python:

* **Declare** rules in Python as shown above (more details in How, below)
* **Extend** rules with Python (rule on line 51 invokes the Python function on line 32)
* **Manage** logic using your existing IDE (PyCharm, VSCode etc for code completion, debugging, etc),
and source control tools and procedures

&nbsp;

## Learning Rules

Inside the larger process above, here is the best way to learn how to use rules:

1. [Rule Summary](https://github.com/valhuber/LogicBank/wiki/Examples): there are a small number of rules, since their power lies in chaining (duplicated below)

2. Be aware of the [rule patterns](https://github.com/valhuber/LogicBank/wiki/Rule-Summary#rule-patterns), duplicated below

3. Use the _case study_ approach to learn about using rules, by exploring the examples in the report, below.

4. Be aware of [Rule Extensibility](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility).

&nbsp;&nbsp;


### Case Study

The best way to learn the rules is by a Case Study approach:

1. See the [Behave Logic Report](../Behave-Logic-Report)

2. On each, open the disclosure box: "Tests - and their logic - are transparent.. click to see Logic"

### Rule Patterns

| Pattern | Notes | Example
| :------------- | :-----| :---- |
| **Chain Up** | parent sums and counts mean that child row changes can ***adjust*** parents | [Derive Balance](../Logic:-Tutorial#scenario-bad-order-custom-service)
| **Chain Down** | child copy and parent references mean that parent row changes can ***cascade*** to children | [Ship Order](../Logic:-Tutorial#scenario-set-shipped---adjust-logic-reuse) 
| **Constrain a Derived Result** | constraints may require derived values | [Balance < creditLimit](../Logic:-Tutorial#scenario-bad-order-custom-service)
| **Auditing** | Note the Copy Row rule | [Salary Audit](../Logic:-Tutorial#scenario-audit-salary-change)
| **old_row** | useful for state transition logic | [Meaningful Raise](../Logic:-Tutorial#scenario-raise-must-be-meaningful)

&nbsp;&nbsp;


### Discovery by Code Completion

Your IDE code completion services can aid in discovering logic services.  There are 2 key elements:

1. Discover _rules_ by `Rule.`
2. Discovery _logic services_ made available through `logic_row`

  > If these aren't working, ensure your `venv` setup is correct - consult the [Trouble Shooting](../Troubleshooting#code-completion-fails) Guide.

You can find examples of these services in the sample `ApiLogicProject`.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/venv.png?raw=true"></figure>
