# API Logic Server

Created: creation-date

From Prototype: 1.0 (Jan 19, 2021)

Clone from: cloned-from


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

    Edit your logic in: logic/logic_bank.py

## Basic Web App - Flask App Builder

This generated project also contains a basic web app
* Multi-page - including page transitions to "drill down"
* Multi-table - master / details (with tab sheets)
* Intelligent layout - favorite fields first, predictive joins, etc

    Edit your pages in: ui/basic_web_app/app/view.py


## Check it out
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

## Source

>*Rules: [/logic/logic_bank.py](/logic/logic_bank.py)*  
*Enhanced Json Decoder: [api/json_encode.py](api/json_encode.py)*  
*SQLAlchemy Models: [/models](/database/models) (StoreModel: Custom endpoint)*  
*Custom Column Types: [models/types](database/models/types)*  
*Flask App: [/app](/app)*  
*Enhanced Flask-Admin View: [/admin/admin_view_ext.py](/admin/admin_view_ext.py) (Display Validation Errors/ LogicBank Constraints)*  
*Flask Admin Custom Types:[/admin/admin_model_converter_ext.py](/admin/admin_model_converter_ext.py)*  
*Rules Exception Handler: [/logic/_init_.py](/logic/__init__.py)*  


**User Email Validation:**

<pre>        if "@" not in value:  raise ValidationError("Email Validation Error {}".format(value))</pre>

**Rules:**

<pre>        Rule.constraint(validate=StoreModel,as_condition=lambda row: 'X' not in row.name,
                                                error_msg="Store Names({row.name}) should not  contain X")
        Rule.count(StoreModel.item_count, as_count_of=ItemModel)
        Rule.parent_check(validate=ItemModel, error_msg="no parent", enable=True)</pre>