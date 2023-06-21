# 1. Learn APIs using Flask / SQLAlchemy

This is a manually coded server providing a few APIs for [this database](https://apilogicserver.github.io/Docs/Sample-Database/).

It is the smallest example of a typical project for a modern database API server.

&nbsp;

# APIs

Here's a brief overview of APIs.

&nbsp;

## Requirement: Networked Database Access

Most database applications require networked database access.  You simply cannot call database access libraries (e.g., ODBC, JDBC) from a mobile app or a remote computer for B2B or application integration.

&nbsp;

## RESTful APIs: Leverage HTTP, JSON

REST has emerged as a loose standard for APIs, by leveraging 2 key technology elements:

* **HTTP protocol:**  Web Browsers utilize this, invoking `Get` commands to obtain `html` responses, but HTTP is far more extensive as shown in the table below.

* **JSON:** JavaScript Object Notation is supported by virtually all language, providing readable formatting for objects/properties, including lists and sub-objects.

&nbsp;

## Example: retrieve some data

HTTP is invoked with a URL, as shown in the following cURL command, identifies a verb, a server/port, an endpoint (`order`) and arguments:

```
curl -X GET "http://localhost:8080/order?Id=10643"
```

&nbsp;

## Key Elements

| HTTP Component |  Designates   | Notes | Example |
|:----|:--------|:--------|:--------|
| **Verb** | `Post`, `Get`, `Patch`, `Delete`  | Maps well to ***crud*** | `Get` |
| Server:port | Identifies server | | http://localhost:8080 | 
| **Endpoint** | Can be series of nodes | Analogous to **table/view** name | `Order` |
| **Arguments** | Key/values Start with `?`, separate by `&` | E.g., **filter/sort**.  Caution: special characters | `?Id=10643` |
| Return Code | Success/failure | a number | 200 means success |
| **Response** | The requested data | JSON format | See below |
| **Request** | Data for insert, update | JSON format | Not used for `Get` |
| *Header* | **Authentication** | typically a token | Commonly JWT (Java Web Token) |

&nbsp;

<details markdown>

<br>

<summary>Response Example</summary>


```json
{
  "AmountTotal": "1086.00",
  "City": "None",
  "CloneFromOrder": "None",
  "Country": "None",
  "CustomerId": "ALFKI",
  "Customer_Name": "Alfreds Futterkiste",
  "EmployeeId": "6",
  "Freight": "29.4600000000",
  "Id": "10643",
  "OrderDate": "2013-08-25",
  "OrderDetailCount": "3",
  "OrderDetailListAsDicts": [
    {
      "Amount": "684.0000000000",
      "Discount": "0.25",
      "Id": "1040",
      "OrderId": "10643",
      "ProductId": "28",
      "ProductName": "R\u00f6ssle Sauerkraut",
      "Quantity": "15",
      "ShippedDate": "None",
      "UnitPrice": "45.6000000000"
    },
    {
      "Amount": "378.0000000000",
      "Discount": "0.25",
      "Id": "1041",
      "OrderId": "10643",
      "ProductId": "39",
      "ProductName": "Chartreuse verte",
      "Quantity": "21",
      "ShippedDate": "None",
      "UnitPrice": "18.0000000000"
    },
    {
      "Amount": "24.0000000000",
      "Discount": "0.25",
      "Id": "1042",
      "OrderId": "10643",
      "ProductId": "46",
      "ProductName": "Spegesild",
      "Quantity": "2",
      "ShippedDate": "None",
      "UnitPrice": "12.0000000000"
    }
  ],
  "Ready": "True",
  "RequiredDate": "2013-09-22",
  "ShipAddress": "Obere Str. 57",
  "ShipCity": "Berlin",
  "ShipCountry": "Germany",
  "ShipName": "Alfreds Futterkiste",
  "ShipZip": "12209",
  "ShipRegion": "Western Europe",
  "ShipVia": "1",
  "ShippedDate": "None"
}
```
</details>

&nbsp;

### Considerable Design Required

There is ***considerable*** variation with RESTful servers:

* how the arguments are specified
* how exactly are request/response objects structured, etc.

Resolving these is a substantial design task, requiring considerable time and experience.  Standards such as **JSON:API** can therefore save time and improve quality.


&nbsp;

# Python Frameworks

Creating an API Server requires 2 basic tools: a Framework, and database access.

There are several libraries for creating Web Servers in Python, including Django, Fast API, and Flask.  Here we will explore:

* Flask - a framework for receiving HTTP calls and returning responses
* SQLAlchemy - SQL Access


&nbsp;

## Framework - Flask

A framework is a "your code goes here" library, providing backend functions to handle api calls, html calls, etc.  The framework provides key basic functions such as:

* listening for incoming calls, and **invoking your code** (your 'handler')

* providing **access to url parameters and request data**

* enabling you to **return a response** in a designated format, such as html or json

A popular framework in Python is ***Flask***, illustrated in this application.  Basically:

```python
    @app.route('/order', methods=['GET'])  # Tell Flask: call this on order request
    def order():
        order_id = request.args.get('Id')  # Obtain URL argument from Flask
```

&nbsp;

## Data Access - SQLAlchemy ORM

In your handler, you may need to read or write database data.  You can use raw SQL, or an ORM (Object Relational Manager) such as SQLAlchemy.  ORMs can facilitate database access:

* **use Objects** (instead of dictionaries), which provide IDE services such as code completion to simplify coding and reduce errors

* simplified **access to related data** (e.g., a simple way to get the OrderDetails for an Order)

* **custom naming** - independent of database table/columns
    * See `Category.CategoryName`, `Order.ShipZip`<br><br>

* other services, such as support for type hierarchies

There are 2 basic elements for using an ORM:

* provide **data model classes** - these are used to read/write data, and can also be used to create / update the database structure (add tables and columns).  See `database/models.py`:


```python
class Customer(Base):
  __tablename__ = 'Customer'
  _s_collection_name = 'Customer'
  __bind_key__ = 'None'

  Id = Column(String(8000), primary_key=True)
  CompanyName = Column(String(8000))

  OrderList = relationship('Order', cascade_backrefs=False, backref='Customer')
```


* use **data access** - verbs to read/write data.  See `api/end_points.py`:

```python
  order = db.session.query(models.Order).filter(models.Order.Id == order_id).one()
  for each_order_detail in order.OrderDetailList:  # SQLAlchemy related data access
```

---

&nbsp;

# Exploring the App

&nbsp;

## App Structure

Long before you use the Flask/SQLAlchemy tools, you need to create project structure.  You can explore [```1. Learn APIs using Flask SqlAlchemy```](../1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/):

* `api` - a directory for api code

* `database` - a directory for SQLAlchemy artifacts

There are also important devops artifacts:

* `.devcontainer/` - files here enable your project to be run in docker images (including Codespaces), and to package your application as an image for production deployment

* `config.py` - use this to set up key configuration parameters, including code to override them with environment variables

&nbsp;

## Server

See [```flask_basic.py```](/1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/flask_basic.py) to see how to establish a Flask server.  It's this program you ran to start the server.


&nbsp;

## API

Explore [```api/end_points.py```](/1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/api/end_points.py) for examples of handling api calls.  See `def order():`.

&nbsp;

## Data Access

There are 2 files to explore for SQLAlchemy:

* See [```database/models.py```](/1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/database/models.py) for examples of defining objects (models) for database rows.  These correspond to the tables in your database.

* See [```api/end_points.py```](/1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/api/end_points.py) for examples of SQLAlchemy calls.  See `def order():`.
