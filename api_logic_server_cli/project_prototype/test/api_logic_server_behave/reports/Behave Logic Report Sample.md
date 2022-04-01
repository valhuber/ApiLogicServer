# Behave Creates Executable Test Suite, Documentation

You can optionally use the Behave test framework to (here is an [Agile Approach for using Behave](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Tutorial)):

1. **Create and Run an Executable Test Suite:** in your IDE, create test definitions (similar to what is shown in the report below), and Python code to execute tests.  You can then execute your test suite with 1 command.

2. **Requirements and Test Documentation:** as shown below, you can then create a wiki report that documents your requirements, and the tests (**Scenarios**) that confirm their proper operation.

   * **Integrated Logic Documentation:** the report integrates your logic, including a logic report showing your logic (rules and Python), and a Logic Log that shows exactly how the rules executed.  Logic Doc is transparent to business users, so can further contribute to Agile Collaboration.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/behave-summary.png?raw=true"  height="600"></figure>

[Behave](https://behave.readthedocs.io/en/stable/tutorial.html) is a framework for defining and executing tests.  It is based on [TDD (Test Driven Development)](http://dannorth.net/introducing-bdd/), an Agile approach for defining system requirements as executable tests.

&nbsp;&nbsp;

# Using Behave

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/TDD-ide.png?raw=true"></figure>

Behave is pre-installed with API Logic Server.  Use it as shown above:

1. Create `.feature` files to define ***Scenarios*** (aka tests) for ***Features*** (aka Stories)

2. Code `.py` files to implement Scenario tests

3. Run Test Suite: Launch Configuration `Behave Run`.  This runs all your Scenarios, and produces a summary report of your Features and the test results.

4. Report: Launch Configuration `Behave Report` to create the wiki file shown at the top of this page.

These steps are further defined, below.  Explore the samples in the sample project.

&nbsp;&nbsp;

## 1. Create `.feature` file to define Scenario

Feature (aka Story) files are designed to promote IT / business user collaboration.  

&nbsp;&nbsp;

## 2. Code `.py` file to implement test

Implement your tests in Python.  Here, the tests are largely _read existing data_, _run transaction_, and _test results_, using the API.  You can obtain the URLs from the swagger.

Key points:

* Link your scenario / implementations with annotations, as shown for _Order Placed with excessive quantity_.

* Include the `test_utils.prt()` call; be sure to use specify the scenario name as the 2nd argument.  This is what drives the name of the Logic Log file, discussed below.

* Optionally, include a Python docstring on your `when` implementation as shown above, delimited by `"""` strings (see _"Familiar logic pattern"_ in the screen shot, above). If provided, this will be written into the wiki report.

* Important: the system assumes the following line identifies the scenario_name; be sure to include it.

&nbsp;&nbsp;

## 3. Run Test Suite: Launch Configuration `Behave Run`

You can now execute your Test Suite.  Run the `Behave Run` Launch Configuration, and Behave will run all of the tests, producing the outputs (`behave.log` and `<scenario.logs>` shown above.

* Windows users will need to run `Windows Behave Run`

* You can run just 1 scenario using `Behave Scenario`

* You can set breakpoints in your tests

The server must be running for these tests.  Use the Launch Configuration `ApiLogicServer`, or `python api_logic_server_run.py`.  The latter does not run the debugger, which you may find more convenient since changes to your test code won't restart the server.

&nbsp;&nbsp;

## 4. Report: Launch Configuration `Behave Report'

Run this to create the wiki reports from the logs in step 3.


&nbsp;
&nbsp;


# Behave Logic Report
&nbsp;
&nbsp;
## Feature: About Sample  
  
&nbsp;
&nbsp;
### Scenario: Transaction Processing
&emsp;  Scenario: Transaction Processing  
&emsp;&emsp;    Given Sample Database  
&emsp;&emsp;    When Transactions are submitted  
&emsp;&emsp;    Then Enforce business policies with Logic (rules + code)  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Rules Used** in Scenario: Transaction Processing
```
```
**Logic Log** in Scenario: Transaction Processing
```
AbstractRule Bank[0x7f3e85d57f10] (loaded 2022-03-31 23:23:26.639531
Mapped Class[Customer] rules
  Constraint Function: None
  Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>
  Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>
  Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None
Mapped Class[Order] rules
  Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None
  RowEvent Order.congratulate_sales_rep()
  Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None
Mapped Class[OrderDetail] rules
  Derive OrderDetail.Amount as Formula (1): as_expression=lambda row: row.UnitPrice * row.Qua [...
  Derive OrderDetail.UnitPrice as Copy(Product.UnitPrice
  Derive OrderDetail.ShippedDate as Formula (2): row.Order.ShippedDat
Mapped Class[Product] rules
  Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>
  Derive Product.UnitsInStock as Formula (1): <function
Mapped Class[Employee] rules
  Constraint Function: <function declare_logic.<locals>.raise_over_20_percent at 0x7f3e85bf74c0>
  RowEvent Employee.audit_by_event()
  Copy to: EmployeeAudi
Logic Bank - 21 rules loaded - 2022-03-31 23:24:45,374 - logic_logger - INF
```
</details>
  
&nbsp;
&nbsp;
## Feature: Application Integration  
  
&nbsp;
&nbsp;
### Scenario: GET Customer
&emsp;  Scenario: GET Customer  
&emsp;&emsp;    Given Customer Account: VINET  
&emsp;&emsp;    When GET Orders API  
&emsp;&emsp;    Then VINET retrieved  
  
&nbsp;
&nbsp;
### Scenario: GET Department
&emsp;  Scenario: GET Department  
&emsp;&emsp;    Given Department 2  
&emsp;&emsp;    When GET Department with SubDepartments API  
&emsp;&emsp;    Then SubDepartments returned  
  
&nbsp;
&nbsp;
## Feature: Place Order  
  
&nbsp;
&nbsp;
### Scenario: Good Order Custom Service
&emsp;  Scenario: Good Order Custom Service  
&emsp;&emsp;    Given Customer Account: ALFKI  
&emsp;&emsp;    When Good Order Placed  
&emsp;&emsp;    Then Logic adjusts Balance (demo: chain up)  
&emsp;&emsp;    Then Logic adjusts Products Reordered  
&emsp;&emsp;    Then Logic sends email to salesrep  
&emsp;&emsp;    Then Logic adjusts aggregates down on delete order  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Good Order Custom Service
   
We place an Order with an Order Detail.  It's one transaction.

Note how the `Order.OrderTotal` and `Customer.Balance` are *adjusted* as Order Details are processed.
Similarly, the `Product.UnitsShipped` is adjusted, and used to recompute `UnitsInStock`

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/declare-logic.png?raw=true"></figure>

> **Key Takeaway:** sum/count aggregates (e.g., `Customer.Balance`) automate ***chain up*** multi-table transactions.

**Events - Extensible Logic**

Inspect the log for __Hi, Andrew - Congratulate Nancy on their new order__. 

The `congratulate_sales_rep` event illustrates logic 
[Extensibility](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility) 
- using Python to provide logic not covered by rules, 
like non-database operations such as sending email or messages.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/send-email.png?raw=true"></figure>

There are actually multiple kinds of events:

* *Before* row logic
* *After* row logic
* On *commit,* after all row logic has completed (as here), so that your code "sees" the full logic results

Events are passed the `row` and `old_row`, as well as `logic_row` which enables you to test the actual operation, chaining nest level, etc.

You can set breakpoints in events, and inspect these.



&nbsp;
&nbsp;


**Rules Used** in Scenario: Good Order Custom Service
```
  Customer  
    1. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    2. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    3. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Employee  
    4. RowEvent Employee.audit_by_event()   
  Order  
    5. Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None)  
    6. Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)  
    7. RowEvent Order.congratulate_sales_rep()   
  OrderDetail  
    8. Derive OrderDetail.ShippedDate as Formula (2): row.Order.ShippedDate  
    9. Derive OrderDetail.Amount as Formula (1): as_expression=lambda row: row.UnitPrice * row.Qua [...]  
    10. Derive OrderDetail.UnitPrice as Copy(Product.UnitPrice)  
  Product  
    11. Derive Product.UnitsInStock as Formula (1): <function>  
    12. Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>)  
  
```
**Logic Log** in Scenario: Good Order Custom Service
```
Logic Phase:		ROW LOGIC(session=0x7f3e8562a280) (sqlalchemy before_flush)			 - 2022-03-31 23:24:45,508 - logic_logger - INF
..Order[None] {Insert - client} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 11, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal: None, Country: None, City: None, Ready: None, OrderDetailCount: None  row: 0x7f3e8562a7c0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,510 - logic_logger - INF
....Customer[ALFKI] {Update - Adjusting Customer: UnpaidOrderCount, OrderCount} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 2102.0000000000, CreditLimit: 2300.0000000000, OrderCount:  [15-->] 16, UnpaidOrderCount:  [10-->] 11  row: 0x7f3e84da6a00  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,522 - logic_logger - INF
..OrderDetail[None] {Insert - client} Id: None, OrderId: None, ProductId: 1, UnitPrice: None, Quantity: 1, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e8563dfd0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,524 - logic_logger - INF
..OrderDetail[None] {copy_rules for role: Product - UnitPrice} Id: None, OrderId: None, ProductId: 1, UnitPrice: 18.0000000000, Quantity: 1, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e8563dfd0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,530 - logic_logger - INF
..OrderDetail[None] {Formula Amount} Id: None, OrderId: None, ProductId: 1, UnitPrice: 18.0000000000, Quantity: 1, Discount: 0, Amount: 18.0000000000, ShippedDate: None  row: 0x7f3e8563dfd0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,531 - logic_logger - INF
....Product[1] {Update - Adjusting Product: UnitsShipped} Id: 1, ProductName: Chai, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 10 boxes x 20 bags, UnitPrice: 18.0000000000, UnitsInStock: 39, UnitsOnOrder: 0, ReorderLevel: 10, Discontinued: 0, UnitsShipped:  [0-->] 1  row: 0x7f3e84dadd90  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,533 - logic_logger - INF
....Product[1] {Formula UnitsInStock} Id: 1, ProductName: Chai, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 10 boxes x 20 bags, UnitPrice: 18.0000000000, UnitsInStock:  [39-->] 38, UnitsOnOrder: 0, ReorderLevel: 10, Discontinued: 0, UnitsShipped:  [0-->] 1  row: 0x7f3e84dadd90  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,536 - logic_logger - INF
....Order[None] {Update - Adjusting Order: AmountTotal, OrderDetailCount} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 11, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal:  [None-->] 18.0000000000, Country: None, City: None, Ready: None, OrderDetailCount:  [None-->] 1  row: 0x7f3e8562a7c0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,538 - logic_logger - INF
......Customer[ALFKI] {Update - Adjusting Customer: Balance} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 2120.0000000000, CreditLimit: 2300.0000000000, OrderCount: 16, UnpaidOrderCount: 11  row: 0x7f3e84da6a00  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,540 - logic_logger - INF
..OrderDetail[None] {Insert - client} Id: None, OrderId: None, ProductId: 2, UnitPrice: None, Quantity: 2, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e8563de80  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,543 - logic_logger - INF
..OrderDetail[None] {copy_rules for role: Product - UnitPrice} Id: None, OrderId: None, ProductId: 2, UnitPrice: 19.0000000000, Quantity: 2, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e8563de80  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,548 - logic_logger - INF
..OrderDetail[None] {Formula Amount} Id: None, OrderId: None, ProductId: 2, UnitPrice: 19.0000000000, Quantity: 2, Discount: 0, Amount: 38.0000000000, ShippedDate: None  row: 0x7f3e8563de80  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,549 - logic_logger - INF
....Product[2] {Update - Adjusting Product: UnitsShipped} Id: 2, ProductName: Chang, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 24 - 12 oz bottles, UnitPrice: 19.0000000000, UnitsInStock: 17, UnitsOnOrder: 40, ReorderLevel: 25, Discontinued: 0, UnitsShipped:  [0-->] 2  row: 0x7f3e85675250  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,551 - logic_logger - INF
....Product[2] {Formula UnitsInStock} Id: 2, ProductName: Chang, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 24 - 12 oz bottles, UnitPrice: 19.0000000000, UnitsInStock:  [17-->] 15, UnitsOnOrder: 40, ReorderLevel: 25, Discontinued: 0, UnitsShipped:  [0-->] 2  row: 0x7f3e85675250  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,553 - logic_logger - INF
....Order[None] {Update - Adjusting Order: AmountTotal, OrderDetailCount} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 11, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal:  [18.0000000000-->] 56.0000000000, Country: None, City: None, Ready: None, OrderDetailCount:  [1-->] 2  row: 0x7f3e8562a7c0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,554 - logic_logger - INF
......Customer[ALFKI] {Update - Adjusting Customer: Balance} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2120.0000000000-->] 2158.0000000000, CreditLimit: 2300.0000000000, OrderCount: 16, UnpaidOrderCount: 11  row: 0x7f3e84da6a00  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,565 - logic_logger - INF
Logic Phase:		COMMIT(session=0x7f3e8562a280)   										 - 2022-03-31 23:24:45,568 - logic_logger - INF
..Order[None] {Commit Event} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 11, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal: 56.0000000000, Country: None, City: None, Ready: None, OrderDetailCount: 2  row: 0x7f3e8562a7c0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,570 - logic_logger - INF
..Order[None] {Hi, Andrew - Congratulate Nancy on their new order} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 11, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal: 56.0000000000, Country: None, City: None, Ready: None, OrderDetailCount: 2  row: 0x7f3e8562a7c0  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,578 - logic_logger - INF
....Employee[1] {Commit Event} Id: 1, LastName: Davolio, FirstName: Nancy, Title: Sales Representative, TitleOfCourtesy: Ms., BirthDate: 1980-12-08, HireDate: 2024-05-01, Address: 507 - 20th Ave. E. Apt. 2A, City: Seattle, Region: North America, PostalCode: 98122, Country: USA, HomePhone: (206) 555-9857, Extension: 5467, Photo: None, Notes: Education includes a BA in psychology from Colorado State University in 1970.  She also completed 'The Art of the Cold Call.'  Nancy is a member of Toastmasters International., ReportsTo: 2, PhotoPath: http://accweb/emmployees/davolio.bmp, IsCommissioned: 1, Salary: 91000.0000000000, WorksForDepartmentId: 2, OnLoanDepartmentId: 1  row: 0x7f3e85615f70  session: 0x7f3e8562a280 - 2022-03-31 23:24:45,580 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Bad Order Custom Service
&emsp;  Scenario: Bad Order Custom Service  
&emsp;&emsp;    Given Customer Account: ALFKI  
&emsp;&emsp;    When Order Placed with excessive quantity  
&emsp;&emsp;    Then Rejected per Credit Limit  
&emsp;&emsp;    Then exceeds credit in response  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Bad Order Custom Service
   
Familiar logic pattern:
* constrain a derived result
* chain up, to adjust parent sum/count aggregates

Logic Design ("Cocktail Napkin Design")
* Customer.Balance <= CreditLimit
* Customer.Balance = Sum(Order.AmountTotal where unshipped)
* Order.AmountTotal = Sum(OrderDetail.Amount)
* OrderDetail.Amount = Quantity * UnitPrice
* OrderDetail.UnitPrice = copy from Product



&nbsp;
&nbsp;


**Rules Used** in Scenario: Bad Order Custom Service
```
  Customer  
    1. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    2. Constraint Function: None   
    3. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    4. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Order  
    5. Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None)  
    6. Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)  
  OrderDetail  
    7. Derive OrderDetail.ShippedDate as Formula (2): row.Order.ShippedDate  
    8. Derive OrderDetail.Amount as Formula (1): as_expression=lambda row: row.UnitPrice * row.Qua [...]  
    9. Derive OrderDetail.UnitPrice as Copy(Product.UnitPrice)  
  Product  
    10. Derive Product.UnitsInStock as Formula (1): <function>  
    11. Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>)  
  
```
**Logic Log** in Scenario: Bad Order Custom Service
```
Logic Phase:		ROW LOGIC(session=0x7f3e84d46280) (sqlalchemy before_flush)			 - 2022-03-31 23:24:46,095 - logic_logger - INF
..Order[None] {Insert - client} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 10, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal: None, Country: None, City: None, Ready: None, OrderDetailCount: None  row: 0x7f3e84d464f0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,101 - logic_logger - INF
....Customer[ALFKI] {Update - Adjusting Customer: UnpaidOrderCount, OrderCount} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 2102.0000000000, CreditLimit: 2300.0000000000, OrderCount:  [15-->] 16, UnpaidOrderCount:  [10-->] 11  row: 0x7f3e84d50ee0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,115 - logic_logger - INF
..OrderDetail[None] {Insert - client} Id: None, OrderId: None, ProductId: 1, UnitPrice: None, Quantity: 1111, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e84d50550  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,118 - logic_logger - INF
..OrderDetail[None] {copy_rules for role: Product - UnitPrice} Id: None, OrderId: None, ProductId: 1, UnitPrice: 18.0000000000, Quantity: 1111, Discount: 0, Amount: None, ShippedDate: None  row: 0x7f3e84d50550  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,125 - logic_logger - INF
..OrderDetail[None] {Formula Amount} Id: None, OrderId: None, ProductId: 1, UnitPrice: 18.0000000000, Quantity: 1111, Discount: 0, Amount: 19998.0000000000, ShippedDate: None  row: 0x7f3e84d50550  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,128 - logic_logger - INF
....Product[1] {Update - Adjusting Product: UnitsShipped} Id: 1, ProductName: Chai, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 10 boxes x 20 bags, UnitPrice: 18.0000000000, UnitsInStock: 40, UnitsOnOrder: 0, ReorderLevel: 10, Discontinued: 0, UnitsShipped:  [-1-->] 1110  row: 0x7f3e84d503a0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,130 - logic_logger - INF
....Product[1] {Formula UnitsInStock} Id: 1, ProductName: Chai, SupplierId: 1, CategoryId: 1, QuantityPerUnit: 10 boxes x 20 bags, UnitPrice: 18.0000000000, UnitsInStock:  [40-->] -1071, UnitsOnOrder: 0, ReorderLevel: 10, Discontinued: 0, UnitsShipped:  [-1-->] 1110  row: 0x7f3e84d503a0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,135 - logic_logger - INF
....Order[None] {Update - Adjusting Order: AmountTotal, OrderDetailCount} Id: None, CustomerId: ALFKI, EmployeeId: 1, OrderDate: None, RequiredDate: None, ShippedDate: None, ShipVia: None, Freight: 10, ShipName: None, ShipAddress: None, ShipCity: None, ShipRegion: None, ShipPostalCode: None, ShipCountry: None, AmountTotal:  [None-->] 19998.0000000000, Country: None, City: None, Ready: None, OrderDetailCount:  [None-->] 1  row: 0x7f3e84d464f0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,139 - logic_logger - INF
......Customer[ALFKI] {Update - Adjusting Customer: Balance} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 22100.0000000000, CreditLimit: 2300.0000000000, OrderCount: 16, UnpaidOrderCount: 11  row: 0x7f3e84d50ee0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,143 - logic_logger - INF
......Customer[ALFKI] {Constraint Failure: balance (22100.0000000000) exceeds credit (2300.0000000000)} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 22100.0000000000, CreditLimit: 2300.0000000000, OrderCount: 16, UnpaidOrderCount: 11  row: 0x7f3e84d50ee0  session: 0x7f3e84d46280 - 2022-03-31 23:24:46,147 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Alter Item Qty to exceed credit
&emsp;  Scenario: Alter Item Qty to exceed credit  
&emsp;&emsp;    Given Customer Account: ALFKI  
&emsp;&emsp;    When Order Detail Quantity altered very high  
&emsp;&emsp;    Then Rejected per Credit Limit  
&emsp;&emsp;    Then exceeds credit in response  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Alter Item Qty to exceed credit
   
Same constraint as above.

> **Key Takeaway:** Automatic Reuse (_design one, solve many_)


&nbsp;
&nbsp;


**Rules Used** in Scenario: Alter Item Qty to exceed credit
```
  Customer  
    1. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    2. Constraint Function: None   
    3. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    4. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Order  
    5. Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None)  
    6. Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)  
  OrderDetail  
    7. Derive OrderDetail.Amount as Formula (1): as_expression=lambda row: row.UnitPrice * row.Qua [...]  
  Product  
    8. Derive Product.UnitsInStock as Formula (1): <function>  
    9. Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>)  
  
```
**Logic Log** in Scenario: Alter Item Qty to exceed credit
```
Logic Phase:		ROW LOGIC(session=0x7f3e84cdae20) (sqlalchemy before_flush)			 - 2022-03-31 23:24:46,277 - logic_logger - INF
..OrderDetail[1040] {Update - client} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity:  [15-->] 1110, Discount: 0.25, Amount: 684.0000000000, ShippedDate: None  row: 0x7f3e84cdad90  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,280 - logic_logger - INF
..OrderDetail[1040] {Formula Amount} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity:  [15-->] 1110, Discount: 0.25, Amount:  [684.0000000000-->] 50616.0000000000, ShippedDate: None  row: 0x7f3e84cdad90  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,282 - logic_logger - INF
..OrderDetail[1040] {Prune Formula: ShippedDate [['Order.ShippedDate']]} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity:  [15-->] 1110, Discount: 0.25, Amount:  [684.0000000000-->] 50616.0000000000, ShippedDate: None  row: 0x7f3e84cdad90  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,286 - logic_logger - INF
....Product[28] {Update - Adjusting Product: UnitsShipped} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock: 26, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [0-->] 1095  row: 0x7f3e84cdaa90  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,292 - logic_logger - INF
....Product[28] {Formula UnitsInStock} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock:  [26-->] -1069, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [0-->] 1095  row: 0x7f3e84cdaa90  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,295 - logic_logger - INF
....Order[10643] {Update - Adjusting Order: AmountTotal} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate: 2013-09-22, ShippedDate: None, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal:  [1086.00-->] 51018.0000000000, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84d7e5e0  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,301 - logic_logger - INF
......Customer[ALFKI] {Update - Adjusting Customer: Balance} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 52034.0000000000, CreditLimit: 2300.0000000000, OrderCount: 15, UnpaidOrderCount: 10  row: 0x7f3e84d50cd0  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,306 - logic_logger - INF
......Customer[ALFKI] {Constraint Failure: balance (52034.0000000000) exceeds credit (2300.0000000000)} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 52034.0000000000, CreditLimit: 2300.0000000000, OrderCount: 15, UnpaidOrderCount: 10  row: 0x7f3e84d50cd0  session: 0x7f3e84cdae20 - 2022-03-31 23:24:46,308 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Alter Required Date - adjust logic pruned
&emsp;  Scenario: Alter Required Date - adjust logic pruned  
&emsp;&emsp;    Given Customer Account: ALFKI  
&emsp;&emsp;    When Order RequiredDate altered (2013-10-13)  
&emsp;&emsp;    Then Balance not adjusted  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Alter Required Date - adjust logic pruned
   
We set `Order.RequiredDate`.

This is a normal update.  Nothing depends on the columns altered, so this has no effect on the related Customer, Order Details or Products.  Contrast this to the *Cascade Update Test* and the *Custom Service* test, where logic chaining affects related rows.  Only the commit event fires.

> **Key Takeaway:** rule pruning automatically avoids unnecessary SQL overhead.



&nbsp;
&nbsp;


**Rules Used** in Scenario: Alter Required Date - adjust logic pruned
```
  Customer  
    1. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    2. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    3. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Order  
    4. RowEvent Order.congratulate_sales_rep()   
  
```
**Logic Log** in Scenario: Alter Required Date - adjust logic pruned
```
Logic Phase:		ROW LOGIC(session=0x7f3e8562a430) (sqlalchemy before_flush)			 - 2022-03-31 23:24:46,432 - logic_logger - INF
..Order[10643] {Update - client} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate:  [2013-09-22-->] 2013-10-13 00:00:00, ShippedDate: None, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84cda9a0  session: 0x7f3e8562a430 - 2022-03-31 23:24:46,436 - logic_logger - INF
Logic Phase:		COMMIT(session=0x7f3e8562a430)   										 - 2022-03-31 23:24:46,441 - logic_logger - INF
..Order[10643] {Commit Event} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate:  [2013-09-22-->] 2013-10-13 00:00:00, ShippedDate: None, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84cda9a0  session: 0x7f3e8562a430 - 2022-03-31 23:24:46,445 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Set Shipped - adjust logic reuse
&emsp;  Scenario: Set Shipped - adjust logic reuse  
&emsp;&emsp;    Given Customer Account: ALFKI  
&emsp;&emsp;    When Order ShippedDate altered (2013-10-13)  
&emsp;&emsp;    Then Balance reduced 1086  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Set Shipped - adjust logic reuse
   
We set `Order.ShippedDate`.

This cascades to the Order Details, per the `derive=models.OrderDetail.ShippedDate` rule.

This chains to adjust the `Product.UnitsShipped` and recomputes `UnitsInStock`, as above

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/order-shipped-date.png?raw=true"></figure>


> **Key Takeaway:** parent references (e.g., `OrderDetail.ShippedDate`) automate ***chain-down*** multi-table transactions.

> **Key Takeaway:** Automatic Reuse (_design one, solve many_)



&nbsp;
&nbsp;


**Rules Used** in Scenario: Set Shipped - adjust logic reuse
```
  Customer  
    1. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    2. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    3. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Order  
    4. Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None)  
    5. Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)  
    6. RowEvent Order.congratulate_sales_rep()   
  OrderDetail  
    7. Derive OrderDetail.ShippedDate as Formula (2): row.Order.ShippedDate  
  Product  
    8. Derive Product.UnitsInStock as Formula (1): <function>  
    9. Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>)  
  
```
**Logic Log** in Scenario: Set Shipped - adjust logic reuse
```
Logic Phase:		ROW LOGIC(session=0x7f3e84c3cb80) (sqlalchemy before_flush)			 - 2022-03-31 23:24:46,649 - logic_logger - INF
..Order[10643] {Update - client} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate: 2013-10-13, ShippedDate:  [None-->] 2013-10-13, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84c75670  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,650 - logic_logger - INF
....Customer[ALFKI] {Update - Adjusting Customer: Balance, UnpaidOrderCount} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [2102.0000000000-->] 1016.0000000000, CreditLimit: 2300.0000000000, OrderCount: 15, UnpaidOrderCount:  [10-->] 9  row: 0x7f3e84c75f40  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,655 - logic_logger - INF
....OrderDetail[1040] {Update - Cascading Order.ShippedDate (,...)} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate: None  row: 0x7f3e84cda100  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,660 - logic_logger - INF
....OrderDetail[1040] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate: None  row: 0x7f3e84cda100  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,663 - logic_logger - INF
....OrderDetail[1040] {Formula ShippedDate} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate:  [None-->] 2013-10-13  row: 0x7f3e84cda100  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,664 - logic_logger - INF
......Product[28] {Update - Adjusting Product: UnitsShipped} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock: 26, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [0-->] -15  row: 0x7f3e84c75be0  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,670 - logic_logger - INF
......Product[28] {Formula UnitsInStock} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock:  [26-->] 41, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [0-->] -15  row: 0x7f3e84c75be0  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,671 - logic_logger - INF
....OrderDetail[1041] {Update - Cascading Order.ShippedDate (,...)} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate: None  row: 0x7f3e84cda220  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,673 - logic_logger - INF
....OrderDetail[1041] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate: None  row: 0x7f3e84cda220  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,677 - logic_logger - INF
....OrderDetail[1041] {Formula ShippedDate} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate:  [None-->] 2013-10-13  row: 0x7f3e84cda220  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,680 - logic_logger - INF
......Product[39] {Update - Adjusting Product: UnitsShipped} Id: 39, ProductName: Chartreuse verte, SupplierId: 18, CategoryId: 1, QuantityPerUnit: 750 cc per bottle, UnitPrice: 18.0000000000, UnitsInStock: 69, UnitsOnOrder: 0, ReorderLevel: 5, Discontinued: 0, UnitsShipped:  [0-->] -21  row: 0x7f3e84c3c8e0  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,686 - logic_logger - INF
......Product[39] {Formula UnitsInStock} Id: 39, ProductName: Chartreuse verte, SupplierId: 18, CategoryId: 1, QuantityPerUnit: 750 cc per bottle, UnitPrice: 18.0000000000, UnitsInStock:  [69-->] 90, UnitsOnOrder: 0, ReorderLevel: 5, Discontinued: 0, UnitsShipped:  [0-->] -21  row: 0x7f3e84c3c8e0  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,689 - logic_logger - INF
....OrderDetail[1042] {Update - Cascading Order.ShippedDate (,...)} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate: None  row: 0x7f3e84cdab80  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,691 - logic_logger - INF
....OrderDetail[1042] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate: None  row: 0x7f3e84cdab80  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,693 - logic_logger - INF
....OrderDetail[1042] {Formula ShippedDate} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate:  [None-->] 2013-10-13  row: 0x7f3e84cdab80  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,695 - logic_logger - INF
......Product[46] {Update - Adjusting Product: UnitsShipped} Id: 46, ProductName: Spegesild, SupplierId: 21, CategoryId: 8, QuantityPerUnit: 4 - 450 g glasses, UnitPrice: 12.0000000000, UnitsInStock: 95, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 0, UnitsShipped:  [0-->] -2  row: 0x7f3e84c55d90  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,703 - logic_logger - INF
......Product[46] {Formula UnitsInStock} Id: 46, ProductName: Spegesild, SupplierId: 21, CategoryId: 8, QuantityPerUnit: 4 - 450 g glasses, UnitPrice: 12.0000000000, UnitsInStock:  [95-->] 97, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 0, UnitsShipped:  [0-->] -2  row: 0x7f3e84c55d90  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,706 - logic_logger - INF
Logic Phase:		COMMIT(session=0x7f3e84c3cb80)   										 - 2022-03-31 23:24:46,711 - logic_logger - INF
..Order[10643] {Commit Event} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate: 2013-10-13, ShippedDate:  [None-->] 2013-10-13, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84c75670  session: 0x7f3e84c3cb80 - 2022-03-31 23:24:46,713 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Reset Shipped - adjust logic reuse
&emsp;  Scenario: Reset Shipped - adjust logic reuse  
&emsp;&emsp;    Given Shipped Order  
&emsp;&emsp;    When Order ShippedDate set to None  
&emsp;&emsp;    Then Logic adjusts Balance by -1086  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Reset Shipped - adjust logic reuse
   
Same logic as above.

> **Key Takeaway:** Automatic Reuse (_design one, solve many_)


&nbsp;
&nbsp;


**Rules Used** in Scenario: Reset Shipped - adjust logic reuse
```
  Customer  
    1. Derive Customer.Balance as Sum(Order.AmountTotal Where <function declare_logic.<locals>.<lambda> at 0x7f3e85c8b3a0>)  
    2. Derive Customer.OrderCount as Count(<class 'database.models.Order'> Where None)  
    3. Derive Customer.UnpaidOrderCount as Count(<class 'database.models.Order'> Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7d30>)  
  Order  
    4. Derive Order.OrderDetailCount as Count(<class 'database.models.OrderDetail'> Where None)  
    5. Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)  
    6. RowEvent Order.congratulate_sales_rep()   
  OrderDetail  
    7. Derive OrderDetail.ShippedDate as Formula (2): row.Order.ShippedDate  
  Product  
    8. Derive Product.UnitsInStock as Formula (1): <function>  
    9. Derive Product.UnitsShipped as Sum(OrderDetail.Quantity Where <function declare_logic.<locals>.<lambda> at 0x7f3e85bd7c10>)  
  
```
**Logic Log** in Scenario: Reset Shipped - adjust logic reuse
```
Logic Phase:		ROW LOGIC(session=0x7f3e84cda2e0) (sqlalchemy before_flush)			 - 2022-03-31 23:24:46,960 - logic_logger - INF
..Order[10643] {Update - client} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate: 2013-10-13, ShippedDate:  [2013-10-13-->] None, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84d46a00  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,962 - logic_logger - INF
....Customer[ALFKI] {Update - Adjusting Customer: Balance, UnpaidOrderCount} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57A, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [1016.0000000000-->] 2102.0000000000, CreditLimit: 2300.0000000000, OrderCount: 15, UnpaidOrderCount:  [9-->] 10  row: 0x7f3e84d35b80  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,978 - logic_logger - INF
....OrderDetail[1040] {Update - Cascading Order.ShippedDate (,...)} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30610  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,986 - logic_logger - INF
....OrderDetail[1040] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30610  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,988 - logic_logger - INF
....OrderDetail[1040] {Formula ShippedDate} Id: 1040, OrderId: 10643, ProductId: 28, UnitPrice: 45.6000000000, Quantity: 15, Discount: 0.25, Amount: 684.0000000000, ShippedDate:  [2013-10-13-->] None  row: 0x7f3e84d30610  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,990 - logic_logger - INF
......Product[28] {Update - Adjusting Product: UnitsShipped} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock: 41, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [-15-->] 0  row: 0x7f3e84d50a60  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:46,997 - logic_logger - INF
......Product[28] {Formula UnitsInStock} Id: 28, ProductName: Rössle Sauerkraut, SupplierId: 12, CategoryId: 7, QuantityPerUnit: 25 - 825 g cans, UnitPrice: 45.6000000000, UnitsInStock:  [41-->] 26, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 1, UnitsShipped:  [-15-->] 0  row: 0x7f3e84d50a60  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,000 - logic_logger - INF
....OrderDetail[1041] {Update - Cascading Order.ShippedDate (,...)} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30250  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,003 - logic_logger - INF
....OrderDetail[1041] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30250  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,005 - logic_logger - INF
....OrderDetail[1041] {Formula ShippedDate} Id: 1041, OrderId: 10643, ProductId: 39, UnitPrice: 18.0000000000, Quantity: 21, Discount: 0.25, Amount: 378.0000000000, ShippedDate:  [2013-10-13-->] None  row: 0x7f3e84d30250  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,007 - logic_logger - INF
......Product[39] {Update - Adjusting Product: UnitsShipped} Id: 39, ProductName: Chartreuse verte, SupplierId: 18, CategoryId: 1, QuantityPerUnit: 750 cc per bottle, UnitPrice: 18.0000000000, UnitsInStock: 90, UnitsOnOrder: 0, ReorderLevel: 5, Discontinued: 0, UnitsShipped:  [-21-->] 0  row: 0x7f3e84d50820  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,013 - logic_logger - INF
......Product[39] {Formula UnitsInStock} Id: 39, ProductName: Chartreuse verte, SupplierId: 18, CategoryId: 1, QuantityPerUnit: 750 cc per bottle, UnitPrice: 18.0000000000, UnitsInStock:  [90-->] 69, UnitsOnOrder: 0, ReorderLevel: 5, Discontinued: 0, UnitsShipped:  [-21-->] 0  row: 0x7f3e84d50820  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,016 - logic_logger - INF
....OrderDetail[1042] {Update - Cascading Order.ShippedDate (,...)} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30070  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,019 - logic_logger - INF
....OrderDetail[1042] {Prune Formula: Amount [['UnitPrice', 'Quantity']]} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate: 2013-10-13  row: 0x7f3e84d30070  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,021 - logic_logger - INF
....OrderDetail[1042] {Formula ShippedDate} Id: 1042, OrderId: 10643, ProductId: 46, UnitPrice: 12.0000000000, Quantity: 2, Discount: 0.25, Amount: 24.0000000000, ShippedDate:  [2013-10-13-->] None  row: 0x7f3e84d30070  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,023 - logic_logger - INF
......Product[46] {Update - Adjusting Product: UnitsShipped} Id: 46, ProductName: Spegesild, SupplierId: 21, CategoryId: 8, QuantityPerUnit: 4 - 450 g glasses, UnitPrice: 12.0000000000, UnitsInStock: 97, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 0, UnitsShipped:  [-2-->] 0  row: 0x7f3e84d50c10  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,029 - logic_logger - INF
......Product[46] {Formula UnitsInStock} Id: 46, ProductName: Spegesild, SupplierId: 21, CategoryId: 8, QuantityPerUnit: 4 - 450 g glasses, UnitPrice: 12.0000000000, UnitsInStock:  [97-->] 95, UnitsOnOrder: 0, ReorderLevel: 0, Discontinued: 0, UnitsShipped:  [-2-->] 0  row: 0x7f3e84d50c10  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,030 - logic_logger - INF
Logic Phase:		COMMIT(session=0x7f3e84cda2e0)   										 - 2022-03-31 23:24:47,032 - logic_logger - INF
..Order[10643] {Commit Event} Id: 10643, CustomerId: ALFKI, EmployeeId: 6, OrderDate: 2013-08-25, RequiredDate: 2013-10-13, ShippedDate:  [2013-10-13-->] None, ShipVia: 1, Freight: 29.4600000000, ShipName: Alfreds Futterkiste, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipRegion: Western Europe, ShipPostalCode: 12209, ShipCountry: Germany, AmountTotal: 1086.00, Country: None, City: None, Ready: True, OrderDetailCount: 3  row: 0x7f3e84d46a00  session: 0x7f3e84cda2e0 - 2022-03-31 23:24:47,033 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
## Feature: Salary Change  
  
&nbsp;
&nbsp;
### Scenario: Audit Salary Change
&emsp;  Scenario: Audit Salary Change  
&emsp;&emsp;    Given Employee 5 (Buchanan) - Salary 95k  
&emsp;&emsp;    When Patch Salary to 200k  
&emsp;&emsp;    Then Salary_audit row created  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Audit Salary Change
   
Observe the logic log to see that it creates audit rows:

1. **Discouraged:** you can implement auditing with events.  But auditing is a common pattern, and this can lead to repetitive, tedious code
2. **Preferred:** approaches use [extensible rules](https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility#generic-event-handlers).

Generic event handlers can also reduce redundant code, illustrated in the time/date stamping `handle_all` logic.

This is due to the `copy_row` rule.  Contrast this to the *tedious* `audit_by_event` alternative:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/salary_change.png?raw=true"></figure>

> **Key Takeaway:** use **extensible own rule types** to automate pattern you identify; events can result in tedious amounts of code.



&nbsp;
&nbsp;


**Rules Used** in Scenario: Audit Salary Change
```
  Employee  
    1. RowEvent Employee.audit_by_event()   
  
```
**Logic Log** in Scenario: Audit Salary Change
```
Logic Phase:		ROW LOGIC(session=0x7f3e84d50fa0) (sqlalchemy before_flush)			 - 2022-03-31 23:24:47,223 - logic_logger - INF
..Employee[5] {Update - client} Id: 5, LastName: Buchanan, FirstName: Steven, Title: Sales Manager, TitleOfCourtesy: Mr., BirthDate: 1987-03-04, HireDate: 2025-10-17, Address: 14 Garrett Hill, City: London, Region: British Isles, PostalCode: SW1 8JR, Country: UK, HomePhone: (71) 555-4848, Extension: 3453, Photo: None, Notes: Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses 'Successful Telemarketing' and 'International Sales Management.'  He is fluent in French., ReportsTo: 2, PhotoPath: http://accweb/emmployees/buchanan.bmp, IsCommissioned: 0, Salary:  [95000.0000000000-->] 200000, WorksForDepartmentId: 3, OnLoanDepartmentId: None  row: 0x7f3e84d30910  session: 0x7f3e84d50fa0 - 2022-03-31 23:24:47,225 - logic_logger - INF
..Employee[5] {BEGIN Copy to: EmployeeAudit} Id: 5, LastName: Buchanan, FirstName: Steven, Title: Sales Manager, TitleOfCourtesy: Mr., BirthDate: 1987-03-04, HireDate: 2025-10-17, Address: 14 Garrett Hill, City: London, Region: British Isles, PostalCode: SW1 8JR, Country: UK, HomePhone: (71) 555-4848, Extension: 3453, Photo: None, Notes: Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses 'Successful Telemarketing' and 'International Sales Management.'  He is fluent in French., ReportsTo: 2, PhotoPath: http://accweb/emmployees/buchanan.bmp, IsCommissioned: 0, Salary:  [95000.0000000000-->] 200000, WorksForDepartmentId: 3, OnLoanDepartmentId: None  row: 0x7f3e84d30910  session: 0x7f3e84d50fa0 - 2022-03-31 23:24:47,229 - logic_logger - INF
....EmployeeAudit[None] {Insert - Copy EmployeeAudit} Id: None, Title: Sales Manager, Salary: 200000, LastName: Buchanan, FirstName: Steven, EmployeeId: None, CreatedOn: None  row: 0x7f3e85621d90  session: 0x7f3e84d50fa0 - 2022-03-31 23:24:47,230 - logic_logger - INF
....EmployeeAudit[None] {early_row_event_all_classes - handle_all sets 'Created_on} Id: None, Title: Sales Manager, Salary: 200000, LastName: Buchanan, FirstName: Steven, EmployeeId: None, CreatedOn: 2022-03-31 23:24:47.231610  row: 0x7f3e85621d90  session: 0x7f3e84d50fa0 - 2022-03-31 23:24:47,232 - logic_logger - INF
Logic Phase:		COMMIT(session=0x7f3e84d50fa0)   										 - 2022-03-31 23:24:47,233 - logic_logger - INF
..Employee[5] {Commit Event} Id: 5, LastName: Buchanan, FirstName: Steven, Title: Sales Manager, TitleOfCourtesy: Mr., BirthDate: 1987-03-04, HireDate: 2025-10-17, Address: 14 Garrett Hill, City: London, Region: British Isles, PostalCode: SW1 8JR, Country: UK, HomePhone: (71) 555-4848, Extension: 3453, Photo: None, Notes: Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses 'Successful Telemarketing' and 'International Sales Management.'  He is fluent in French., ReportsTo: 2, PhotoPath: http://accweb/emmployees/buchanan.bmp, IsCommissioned: 0, Salary:  [95000.0000000000-->] 200000, WorksForDepartmentId: 3, OnLoanDepartmentId: None  row: 0x7f3e84d30910  session: 0x7f3e84d50fa0 - 2022-03-31 23:24:47,234 - logic_logger - INF

```
</details>
  
&nbsp;
&nbsp;
### Scenario: Raise Must be Meaningful
&emsp;  Scenario: Raise Must be Meaningful  
&emsp;&emsp;    Given Employee 5 (Buchanan) - Salary 95k  
&emsp;&emsp;    When Patch Salary to 96k  
&emsp;&emsp;    Then Reject - Raise too small  
<details>
<summary>Tests - and their logic - are transparent.. click to see Logic</summary>


&nbsp;
&nbsp;


**Logic Doc** for scenario: Raise Must be Meaningful
   
Observe the use of `old_row
`
> **Key Takeaway:** State Transsition Logic enabled per `old_row`



&nbsp;
&nbsp;


**Rules Used** in Scenario: Raise Must be Meaningful
```
  Employee  
    1. Constraint Function: <function declare_logic.<locals>.raise_over_20_percent at 0x7f3e85bf74c0>   
  
```
**Logic Log** in Scenario: Raise Must be Meaningful
```
Logic Phase:		ROW LOGIC(session=0x7f3e84bec100) (sqlalchemy before_flush)			 - 2022-03-31 23:24:47,526 - logic_logger - INF
..Employee[5] {Update - client} Id: 5, LastName: Buchanan, FirstName: Steven, Title: Sales Manager, TitleOfCourtesy: Mr., BirthDate: 1987-03-04, HireDate: 2025-10-17, Address: 14 Garrett Hill, City: London, Region: British Isles, PostalCode: SW1 8JR, Country: UK, HomePhone: (71) 555-4848, Extension: 3453, Photo: None, Notes: Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses 'Successful Telemarketing' and 'International Sales Management.'  He is fluent in French., ReportsTo: 2, PhotoPath: http://accweb/emmployees/buchanan.bmp, IsCommissioned: 0, Salary:  [95000.0000000000-->] 96000, WorksForDepartmentId: 3, OnLoanDepartmentId: None  row: 0x7f3e84bec730  session: 0x7f3e84bec100 - 2022-03-31 23:24:47,527 - logic_logger - INF
..Employee[5] {Constraint Failure: Buchanan needs a more meaningful raise} Id: 5, LastName: Buchanan, FirstName: Steven, Title: Sales Manager, TitleOfCourtesy: Mr., BirthDate: 1987-03-04, HireDate: 2025-10-17, Address: 14 Garrett Hill, City: London, Region: British Isles, PostalCode: SW1 8JR, Country: UK, HomePhone: (71) 555-4848, Extension: 3453, Photo: None, Notes: Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses 'Successful Telemarketing' and 'International Sales Management.'  He is fluent in French., ReportsTo: 2, PhotoPath: http://accweb/emmployees/buchanan.bmp, IsCommissioned: 0, Salary:  [95000.0000000000-->] 96000, WorksForDepartmentId: 3, OnLoanDepartmentId: None  row: 0x7f3e84bec730  session: 0x7f3e84bec100 - 2022-03-31 23:24:47,529 - logic_logger - INF

```
</details>
  