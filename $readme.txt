FIXME design - search for these, which designate request for external review
TODO major - designates significant unimplemented

Major friction due to Python Path
    Pycharm sets it (thankyou), but cmd-line, vsc (etc) do not
    Run > Configurations, unset Source & Content Roots
    This should make debug runs == cmd-line, vsc
    Using LogicBankUtils to set path (to LogicBank) in each nw/tests

Significant bug fixes:
    See nw/trans_tests/upd_order_reuse, and logic_engine/exec_row_logic/logic_row#save_altered_parents


Various misc copy/paste:

update orderdetail set amount = unitPrice * quantity

update "Order" set AmountTotal =
(select sum(orderdetail.amount) from orderdetail where orderdetail.orderid = "Order".id);

select id, customerid, shippeddate, amounttotal from "Order" where id = 11011;

select ProductName, UnitsInStock, UnitsShipped from Product where id = 58;

select id, balance, creditlimit from customer where id="ALFKI";
    960

update Customer set Balance =
(select sum("Order".amounttotal) from "Order" where Customer.id = "Order".customerid
and "Order".shippeddate is null);

update Customer set UnpaidOrderCount =
(select count("Order".amounttotal) from "Order" where Customer.id = "Order".customerid
and "Order".shippeddate is null);

update Customer set Balance = 0 where balance is null;
update Customer set Balance = 960  where id="ALFKI";

update Customer set creditlimit = balance + 100;

830 orders, 21 not shipped
    11045 for BOTTM (22607.7 ==> 1309.5)
    ALFKI has balance=0


select id, amounttotal from "Order" where id=11011;

CREATE TABLE IF NOT EXISTS "OrderX"
(
  "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "CustomerId" VARCHAR(8000) NULL,
  "EmployeeId" INTEGER NOT NULL,
  "OrderDate" VARCHAR(8000) NULL,
  "RequiredDate" VARCHAR(8000) NULL,
  "ShippedDate" VARCHAR(8000) NULL,
  "ShipVia" INTEGER NULL,
  "Freight" DECIMAL NOT NULL,
  "ShipName" VARCHAR(8000) NULL,
  "ShipAddress" VARCHAR(8000) NULL,
  "ShipCity" VARCHAR(8000) NULL,
  "ShipRegion" VARCHAR(8000) NULL,
  "ShipPostalCode" VARCHAR(8000) NULL,
  "ShipCountry" VARCHAR(8000) NULL, AmountTotal Decimal(10,2),
  FOREIGN KEY (CustomerId) REFERENCES Customer(Id),
  FOREIGN KEY (EmployeeId) REFERENCES Employee(Id)
);

insert into Orderx select * from "Order";

SELECT Id, CustomerId FROM "Order"
WHERE NOT EXISTS (SELECT 1 FROM Customer WHERE Customer.Id = "Order".CustomerId);

OrderList fails on 10248 : 10272 (no orphans to Customer, Employee) - serving.py @ 314
ha!  Due to a null row - deleted it, runs fine now
[10248, 10249, 10250, 10251, 10252, 10253, 10254, 10255, 10256, 10257, 10258, 10259, 10260, 10261, 10262, 10263, 10264, 10265, 10266, 10267, 10268, 10269, 10270, 10271, 10272]

SELECT Id, EmployeeId FROM "Order"
WHERE NOT EXISTS (SELECT 1 FROM Employee WHERE Employee.Id = "Order".EmployeeId);

......Customer[ALFKI] {Update - Adjusting Customer} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance:  [1016.00-->] 1034.00, CreditLimit: 2000.00, OrderCount: 10, UnpaidOrderCount: 5, PaidOrderCount: 5  row@: 0x10b410430 - 2020-10-21 20:40:19,743 - logic_logger - DEBUG


notes regarding LogicRow.get_old_children()
