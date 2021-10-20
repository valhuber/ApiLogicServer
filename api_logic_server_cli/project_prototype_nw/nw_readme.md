# API Logic Server - Sample Tutorial

You've already completed the `create` step below, and now viewing the readme in the created project - the sample tutorial, created from [this database.](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)  

In this tutorial, we will explore:

* **run** - we will first run the Web App and the JSON:API

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them

This tutorial presumes you are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.  You will need to configure container and launch configurations for PyCharm - [see here]() for more information.

The diagram below summarizes the create / run / customize process:

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/creates-and-runs.png"></figure>

You can watch the tutorial in [this video.](https://youtu.be/-C5O453Q-Mc)


&nbsp;&nbsp;&nbsp;

## Run

Created projects are instantly executable.  Let's explore the Basic Web App and the API.

### Basic Web App
To run the Web App, follow these steps:

1. Click **Run and Debug**
   * *Note:* these steps are highlighted in the diagram below
2. Select the `Basic Web App` Launch Configuration
3. Press the green run button
   * The app should start, and VS Code will suggest opening a Browser (the _preview_ browser is shown below).  Do so, and run the app with user **admin**, password **p**.
4. Explore the app - multi-page, multi-table, automatic joins
5. Stop the server

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/basic-web-app.png"></figure>


### JSON:API - Swagger
Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

The creation process builds not only the API, but swagger so you can explore it, like this:
1. Select the `ApiLogicServer` Launch Configuration
2. Press the green run button
   * The app should start, and VS Code will suggest opening a Browser.
3. Explore the swagger
4. **Don't stop** the server; we'll use it for debugging...

&nbsp;&nbsp;&nbsp;

## Customize and Debug

That's quite a good start on a project.  But we've all seen generators that get close, but fail because the results cannot be extended, debugged, or managed with tools such as git and diff.

Let's examine how API Logic Server projects can be customized for both APIs and logic.  We'll first have a quick look at the created project structure, then some typical customizations.

> The API and web app you just reviewed above were ***not*** customized - they were created completely from the database structure.  For the sample project, we've injected some API and logic customizations, so you can explore them in this tutorial, as described below.


### Project Structure
Use the Project Explorer to see the project structure:

| Directory | Usage | Key Customization File | Typical Customization  |
|:-------------- |:--------|:--------------|:--------------|
| ```api``` | JSON:API | ```api/customize_api.py``` | Add new end points / services |
| ```database``` | SQLAlchemy Data Model Classes | ```database/customize_models.py``` | Add derived attributes, and relationships missing in the schema |
| ```logic``` | Transactional Logic | ```logic/declare_logic.py``` | Declare multi-table derivations, constraints, and events such as send mail / messages  |
| ```ui``` | Basic Web App  | ```ui/basic_web_app/app/view.py``` | Control field display, and add interfaces like graphs and charts |

Let's now explore some examples.

### API Customization

While a standards-based API is a great start, sometimes you need custom endpoints tailored exactly to your business requirement.  You can create these as shown below, where we create an additional endpoint for `add_order`.

To review the implementation: 

1. Open **Explorer > `api/customize_api.py`:**
2. Set the breakpoint as shown
3. Use the swagger to access the `ServicesEndPoint > add_order`, and
   1. **Try it out**, then 
   2. **execute**

You can examine the variables, step, etc.

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>


### Logic
We've all seen excellent technology that can create great User Interfaces. But for transactional systems, their approach to logic is basically "your code goes here".

> That's a problem - for transaction systems, the backend constraint and derivation logic is often *half* the system.
 
The *logic* portion of API *Logic* server is a declarative approach - you declare spreadsheet-like rules for multi-table constraints and derivations.  The 5 rules shown below represent the same logic as 200 lines of Python - a remarkable **40X.**

> Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.

[Logic](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) consists of rules **and** conventional Python code.  Explore it like this:
1. Explore the `logic/declare_logic.py` file
   * Observe the 5 rules highlighted in the diagram below.  These are built with code completion.
2. Set a breakpoint as shown
   * This event illustrates that logic is mainly _rules,_ extensible with standard _Python code_
3. Using swagger, re-execute the `add_order` endpoint
4. When you hit the breakpoint, expand `row` VARIABLES list (top left)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/declare-logic.png"></figure>


&nbsp;&nbsp;&nbsp;

## Wrap up
Let's recap what you've seen:

* **Working software now** - a database API and a Web App - created automatically from a database, in moments instead of weeks or months.


* **Customization** - for both the API and Logic - using Visual Studio code, for both editing and debugging

### Docker cleanup
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. it will look something like `vsc-api_logic_server...`.

&nbsp;&nbsp;&nbsp;


## Appendix - Key Technologies

API Logic Server is based on the projects shown below.
Consult their documentation for important information.

### SARFS JSON:API Server

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

### LogicBank

[Transaction Rules for SQLAlchemy Object Models](https://github.com/valhuber/logicbank)

Use [Logic](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) to govern update transaction logic - 
multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

The Logic Engine is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.
Your logic therefore applies to any SQLAlchemy-based access - JSON:Api, Flask App Builder, etc.


### SQLAlchemy

[Object Relational Mapping for Python](https://docs.sqlalchemy.org/en/13/).

SQLAlchemy provides Python-friendly database access for Python.

It is used by JSON:Api, Logic Bank, and Flask App Builder.

SQLAlchemy processing is based on Python `model` classes,
created automatically by API Logic Server from your database,
and saved in the `database` directory.


### Basic Web App - Flask App Builder

This generated project also contains a basic web app
* Multi-page - including page transitions to "drill down"
* Multi-table - master / details (with tab sheets)
* Intelligent layout - favorite fields first, predictive joins, etc

#### Preparing Flask AppBuilder
Before you run your app, you must create admin data,
and address certain restrictions.  For more information, see
[Working with Flask AppBuilder](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Flask-AppBuilder).

## Appendix 1 - Features


| Feature | Providing  | Why it Matters | Learn More
| :-------------- |:--------------| :------|  :------|
| 1. [JSON:**API** and Swagger](#jsonapi---swagger) | Endpoint for each table, with... <br>Filtering, pagination, related data | Unblock Client App Dev | [SAFRS](https://github.com/thomaxxl/safrs/wiki) |
| 2. [Transactional **Logic**](#logic)| *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code)  | Strategic Business Agility | [Logic Bank](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) |
| 3. [Basic **Web App**](#basic-web-app) | Instant **multi-page, multi-table** web app | Engage Business Users<br>Back-office Admin | [Flask App Builder](https://flask-appbuilder.readthedocs.io/en/latest/), <br>[fab-quickstart](https://github.com/valhuber/fab-quick-start/wiki) |
| 4. [**Customizable Project**](#customize-and-debug) | Custom Data Model, Endpoints, Logic | Customize and run <br>Re-creation *not* required | PyCharm <br> VS Code ... |
| 5. Model Creation | Python-friendly ORM | Custom Data Access<br>Used by API and Basic Web App | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html) |

## Appendix 2 - Project Information

| About | Info  |
|:--------------|:--------------|
| Created | creation-date |
| API Logic Server Version | api_logic_server_version |
| Cloned From | api_logic_server_template  |



