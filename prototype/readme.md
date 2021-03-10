# API Logic Server

Created: creation-date

From Prototype: 1.1 (Mar 3, 2021)

Clone from: cloned-from

API Logic Server is based on the projects shown below.
Consult their documentation for important information.

## SARFS JSON:Api Server

[SAFRS: Python OpenAPI & JSON:API Framework](https://github.com/thomaxxl/safrs)

SAFRS is an acronym for SqlAlchemy Flask-Restful Swagger.
The purpose of this framework is to help python developers create
a self-documenting JSON API for sqlalchemy database objects and relationships.

These objects can be serialized to JSON and can be
created, retrieved, updated and deleted through the JSON API.
Optionally, custom resource object methods can be exposed and invoked using JSON.

Class and method descriptions and examples can be provided
in yaml syntax in the code comments.

The description is parsed and shown in the swagger web interface.
The result is an easy-to-use
swagger/OpenAPI and JSON:API compliant API implementation.

## LogicBank

[Transaction Rules for SQLAlchemy Object Models](https://github.com/valhuber/logicbank)

Use Logic Bank to govern SQLAlchemy update transaction logic - multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

Logic Bank is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.
Your logic therefore applies to any SQLAlchemy-based access - JSON:Api, Flask App Builder, etc.

    Declare your logic in: logic/logic_bank.py


## SQLAlchemy

[Object Relational Mapping for Python](https://docs.sqlalchemy.org/en/13/).

SQLAlchemy provides Python-friendly database access for Python.

It is used by JSON:Api, Logic Bank, and Flask App Builder.

SQLAlchemy processing is based on Python `model` classes,
created automatically by API Logic Server from your database,
and saved in the `database` directory.



## Basic Web App - Flask App Builder

This generated project also contains a basic web app
* Multi-page - including page transitions to "drill down"
* Multi-table - master / details (with tab sheets)
* Intelligent layout - favorite fields first, predictive joins, etc


    Edit your pages in: ui/basic_web_app/app/view.py

### Preparing Flask AppBuilder
Before you run your app, you must create admin data,
and address certain restrictions.  For more information, see
[Working with Flask AppBuilder](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Flask-AppBuilder).


# Check it out
Install your projects' environment:
```
cd <your project>
test> cd my_new_project
virtualenv venv
source venv/bin/activate  # windows venv\Scripts\activate
pip install -r requirements.txt
python api_logic_server_run.py
```
Then, run:
* **Open API (Swagger) -** [localhost:5000/api](localhost:5000/api)

* **Basic Web App -** [localhost:8080](/localhost:8080)

# Project Structure

>*Logic: [/logic/logic_bank.py](/logic/logic_bank.py)*  
*SQLAlchemy Models: [/database](/database/models.py)*  
*Services: [/api](/api/expose_services.py)*  
*Flask App: [/ui](/ui/basic_web_app/run.py)*  
