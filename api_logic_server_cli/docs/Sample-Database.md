The sample application [(run it here)](http://apilogicserver.pythonanywhere.com/admin-app/index.html) is created from the database shown below [(tutorial here)](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-logic-server---sample-tutorial).  It is an extension to Northwind that includes additional relationships:
* multiple relationships between Department / Employee
* multi-field relationships between Order / Location
* self-relationships in Department

The integrity of this database is enforced with [this logic](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#logic).

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/nw.png"></figure>


## Standard Northwind
Specify your database as `nw-` to use the standard Northwind:

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/nw.png"></figure>

It includes a few fields to illustrate rules.  For example, `Customer.Balance`.  
It also includes the admin security tables for the basic web app, as described [here.](../Working-with-Flask-AppBuilder)

The sample project also has some pre-loaded code to illustrate [customizations](https://github.com/valhuber/ApiLogicServer/wiki) for logic, APIs and the data model.
