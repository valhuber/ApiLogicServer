# API Logic Server - Sample Tutorial

You've already completed the `create` step below.  In this tutorial, we will explore:

* **run** - we will first run the Web App and the JSON:API

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them

This tutorial presumes are are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for `.devcontainer` and `launch configurations`, so these instructions are oriented around VS Code.  You will need to configure container and launch configurations for PyCharm - [see here]() for more information.

Here is a video going through the same basic steps:

[![Using VS Code](https://github.com/valhuber/ApiLogicServer/blob/main/images/creates-and-runs-video-vsc.png?raw=true?raw=true)](https://youtu.be/-C5O453Q-Mc "Using VS Code with the ApiLogicServer container")

# Project Information

| About | Info  |
|:--------------|:--------------|
| Created | creation-date |
| API Logic Server Version | api_logic_server_version |
| Cloned From | api_logic_server_template  |

# Run

Created projects are instantly executable.  Let's explore the Basic Web App and the API.

### Basic Web App
To run the Web App:

1. Select the `Basic Web App` Launch Configuration
2. Press the green run button
   * The app should start, and VS Code will suggest opening a Browser.  Do so, and run the app with user **admin**, password **p**.
3. Explore the app
4. Stop the server

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/basic-web-app.png"></figure>


### JSON:API (Swagger)
The creation process builds not only the API, but swagger so you can explore it, like this:
1. Select the `ApiLogicServer` Launch Configuration
2. Press the green run button
   * The app should start, and VS Code will suggest opening a Browser.
3. Explore the swagger
4. Don't stop the server; we'll use it for debugging...


# Customize and Debug

That's quite a good start on a project.  But we've all seen generators that get close, but fail because the results cannot be extended, debugged, or managed with tools such as git and diff.

Let's examine the API Logic Server projects can be customized for both APIs and logic.  We'll first have a quick look at the created project structure, then some typical customizations.

> The API and web app you just reviewed were ***not*** customized - they were created completely from the model.  For the sample project, we've injected some API and logic customizations so you can explore them in this tutorial.


### Project Structure
This project was created with the following directory structure:

| Directory | Usage | Key Customization File | Typical Customization  |
|:-------------- |:--------|:--------------|:--------------|
| ```api``` | JSON:API | ```api/customize_api.py``` | Add new end points / services |
| ```database``` | SQLAlchemy Data Model Classes | ```database/customize_models.py``` | Add derived attributes, and relationships missing in the schema |
| ```logic``` | Transactional Logic | ```logic/declare_logic.py``` | Declare multi-table derivations, constraints, and events such as send mail / messages  |
| ```ui``` | Basic Web App  | ```ui/basic_web_app/app/view.py``` | Control field display, and add interfaces like graphs and charts |

### Key Customization File - Typical Customization

In the table above, the _Key Customization Files_ are created as stubs, intended for you to add customizations that extend
the created API, Logic and Web App.  Since they are separate files, the project can be
recreated (e.g., synchronized with a revised schema), and these files can be easily copied
into the new project, without line-by-line merges.

Let's now explore some examples.

### API Customization

While a standards-based API is a great start, sometimes you need custom endpoint tailored exactly to your business requirement.  You can create these as shown below in `api/customize_api.py`, where we create an additional endpoint for add_order.  To see it in action:

1. Set the breakpoint as shown
2. Use the swagger to access the endpoint, and **Try it out**, then **execute**

You can examine the variables, step, etc.

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>


### Logic
We've all seen excellent technology that can create great User Interfaces. But for transactional systems, their approach to logic is basically "your code goes here".

> That's a problem - for transaction systems, the backend constraint and derivation logic is often *half* the system.
 
The *logic* portion of API *Logic* server is a declarative approach - you declare spreadsheet-like rules for constraints and derivations.

> Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.

Logic is rules **plus** conventional Python code.  Explore the `logic/declare_logic.py` file, and:
1. Set a breakpoint
2. Using swagger, re-execute the add_order endpoint
3. When you hit the breakpoint, expand the `row` variable

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>

# Appendix 1 - Key Technologies

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

Use Logic Bank to govern SQLAlchemy update transaction logic - 
multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

Logic Bank is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.
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


# Installation and Execution
If not using Docker, install your projects' virtual environment:
```
cd <your project>
virtualenv venv
source venv/bin/activate  # windows venv\Scripts\activate
pip install -r requirements.txt
```

Then, start the API, either by IDE launch configurations (for Docker), or by command line:
```
python api_logic_server_run.py
```
* **Open API (Swagger) -** [localhost:5000/api](localhost:5000/api)


Or, start the web app:
```
python ui/basic_web_app/run.py
```

* **Basic Web App -** [localhost:8080](/localhost:8080)

