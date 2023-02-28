# 1. Basic App: Flask / SQLAlchemy -- manually coded app

This is a manually coded server providing a few APIs for [this database]().

It is the smallest example of a typical project for a modern database API server.

&nbsp;

## Background - Key Tools

Creating an API Server requires 2 basic tools: a Framework, and database access.

&nbsp;

### Framework - Flask

A framework is a "your code goes here" library, provding backend functions to handle api calls, html calls, etc.  The framework provides key basic functions such as:

* listening for incoming calls, and **invoking your code** (your 'handler')

* providing **access to url parameters and request data**

* enabling you to **return a response** in a designated format, such as html or json

A popular framework in Python is ***Flask***, illustrated in this application.

&nbsp;

### Data Access - SQLAlchemy ORM

In your handler, you may need to read or write database data.  You can use raw SQL, or an ORM (Object Relational Manager) such as SQLAlchemy.  ORMs can facilitate database access:

* **use Objects** (instead of dictionaries), which provide IDE services such as code completion to simplify coding and reduce errors

* simplified **access to related data** (e.g., a simple way to get the OrderDetails for an Order)

* other services, such as support for type hierarchies

There are 2 common aspects for using an ORM:

* provide **data model classes** - these are used to read/write data, and can also be used to create / update the database structure (add tables and columns)

* use **data access** - verbs to read/write data

---

&nbsp;

## Exploring the App

&nbsp;

### App Structure

Long before you use the Flask/SQLAlchemy tools, you need to create project structure.  You can explore [```1. Basic_App```](../1.%20Basic_App/):

* `api` - a directory for api code

* `database` - a directory for SQLAlchemy artifacts

There are also important devops artifacts:

* `.devcontainer/` - files here enable your project to be run in docker images, and to package your application as an image

* `config.py` - use this to set up key configuration parameters, including code to override them with environment variables

&nbsp;

### Server

See [```flask_basic.py```](../1.%20Basic_App/flask_basic.py) to see how to establish a Flask server.  It's this program you ran to start the server.

&nbsp;

### API

Explore [```api/end_points.py```](../1.%20Basic_App/api/end_points.py) for examples of handling api calls.  See `def order():`.

&nbsp;

### Data Access

There are 2 aspects to explore for SQLAlchemy:

* See [```database/models.py```](../1.%20Basic_App/database/models.py) for examples of defining objects (models) for database rows.  These correspond to the tables in your database.

* See [```api/end_points.py```](../1.%20Basic_App/api/end_points.py) for examples of SQLAlchemy calls.  See `def order():`.

&nbsp;

## Appendix

&nbsp;

### API

An API is a set of endpoints, accessible via the web, that clients (e.g, mobile apps) can invoke by providing:

* **a command:** such as GET, POST or PATCH

* **a URL:** this identifies the server, the endpoint (e.g, Order), and the arguments (e.g. the OrderNumber)

* **a payload:** data being sent to the server (e.g, to be saved), typically in `json` format (not provided for GET commands)

* **a header:** typically identifying the authenticated user

&nbsp;

### API Server

A server that implements an API.  In the context of this tutorial, it's a Flask server, using SQLAlchemy for data access.
