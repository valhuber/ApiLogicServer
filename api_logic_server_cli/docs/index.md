---
title:
---

[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

[![API Logic Server Intro](https://github.com/valhuber/apilogicserver/wiki/images/hero-banner.png?raw=true)](https://valhuber.github.io/ApiLogicServer/ "Single command creates executable, customizable projects")

&nbsp;

# Welcome to API Logic Server

Use API Logic Server to create customizable database web app projects _instantly_ from your database schema, providing:

* __API__ - an endpoint for each table, with filtering, sorting, pagination and related data access

* __Admin UI__ - multi-page / multi-table apps, with page navigations and automatic joins

* __Logic Automation__ - using unique rules, extensible with Python

Created projects are customizable with your IDE, such as VSCode.

&nbsp;

# Background
A brief look at why we built it, and our approach.<br><br>

### Motivation - not instant, propietary IDE, no logic automation

We looked at approaches for building database systems:   

* __Frameworks:__ Frameworks like Flask or Django enable you to build a single endpoint or _Hello World_ page, but a __multi-endpoint__ API and __multi-page__ application would take __weeks__ or more.

* __Low Code Tools:__ these are great for building great UIs, but

    * Want a multi-page app, _instantly_ -- __no layout required each screen__
    * Want to __preserve dev tools__ - VSCode, PyCharm, git, etc
    * Need an answer for __backend logic__ (it's nearly half the effort)<br><br>


### Our Approach: Instant, Customizable, Logic Automation

API Logic Server is an open source Python project, consisting of:

* a set of runtimes (SAFRS API, Flask, SQLAlchemy ORM, rule engine) for project execution, plus 

* a CLI (Command Language Interface) to create executable projects, which can be customized in an IDE such as VSCode or PyCharm

It runs as a standard pip install, or under Docker. After installation, you use the CLI create a project like this:

```
ApiLogicServer create --project_name=ApiLogicProject db_url=
```

!!! pied-piper "Key Takeaway"

    :bulb: API Logic Server reads your schema, and creates an executable, customizable project providing the features listed below.

&nbsp;

# Feature Summary

|   | Feature    | Providing   | Why it Matters   |
:-------|:-----------|:------------|:-----------------|
| __Instant__ | 1. [**Admin App**](Admin-Tour){:target="_blank" rel="noopener"} | Instant **multi-page, multi-table** app  [(running here on PythonAnywhere)](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home){:target="_blank" rel="noopener"}              | Engage Business Users<br>Back-office Admin       |
| | 2. [JSON:**API** and Swagger](API){:target="_blank" rel="noopener"}                     | Endpoint for each table, with... <br>Filtering, pagination, related data                                                                        | Unblock custom App Dev<br>Application Integration                           |
| | 3. Data Model Class Creation                                                     | Classes for Python-friendly ORM                                                                                                                             | Custom Data Access<br>Used by API                |
| __Customizable__ | 4. [**Customizable Project**](Project-Structure){:target="_blank" rel="noopener"}                   | Custom Endpoints, Logic <br>Use Python and your IDE  |Customize and run <br>Re-creation *not* required |                                                                                      
| __Unique Logic__ | 5. [Spreadsheet-like Business Rules](Logic-Rules-plus-Python){:target="_blank" rel="noopener"}  &nbsp; :trophy:      | **40X more concise** - compare [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code){:target="_blank" rel="noopener"} | Unique backend automation <br> ... nearly half the system  |
|  | Extensible with Python      | Familiar Event Model | Eg., Send messages, email  |
| Testing | 6. [Behave **Test Framework**](Behave)         | Test Suite Automation<br/>Behave Logic Report<br/>Drive Automation with Agile                                                                                                                           | Optimize Automation to get it fast<br/>Agile Collaboration to get it right                |

&nbsp;

# Instant -- Single Command

Use the CLI to create the sample API and Admin App project, with a single command.

&nbsp;

### Create With Docker

Execute the following commands (Windows, use Windows Terminal or Powershell):

```bash title="Run API Logic Server in Docker"
# Start the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/localhost/ApiLogicProject --db_url=
```
&nbsp;

### Or, Create With Local Install
Presuming Python 3.7+ [is installed](Install){:target="_blank" rel="noopener"}, it's typically:

```bash title="Run API Logic Server from a local pip install"
python -m venv venv        # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
venv\Scripts\activate      # mac/linux: source venv/bin/activate
python -m pip install ApiLogicServer

ApiLogicServer create --project_name=ApiLogicProject --db_url=  # or, create-and-run
python ApiLogicProject/api_logic_server_run.py                  # run the server
```
&nbsp;

## Execute

Your system is running - explore the data and api at [localhost:5656](http://localhost:5656).  Using the defaults provided above, you have started the [Tutorial](Tutorial/){:target="_blank" rel="noopener"}, the recommended quick start for API Logic Server.

&nbsp;

# Customize in IDE

VSCode and PyCharm users can customize and run/debug within their IDE with [these steps](IDE-Execute){:target="_blank" rel="noopener"}.  Created projects include Launch and Docker configurations.  

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png?raw=true"></figure>

[Rebuild services](https://valhuber.github.io/ApiLogicServer/Project-Rebuild/){:target="_blank" rel="noopener"} are provided to accomodate changes to database structure or ORM classes.

&nbsp;

# Overview Video

Project creation is based on database schema introspection as shown below: identify a database, and the ```ApiLogicServer create``` commands creates an executable, customomizable project.

Click for a video tutorial, showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/creates-and-runs-video.jpg?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container"){:target="_blank" rel="noopener"}

&nbsp;

# Getting Started

API Logic Server is designed to make it easy to get started:

* **Install and run Tutorial** - 
[install](https://valhuber.github.io/ApiLogicServer/Install-Express/), and explore the [tutorial](https://valhuber.github.io/ApiLogicServer/Tutorial/).  You'll create a complete project using the pre-installed sample database, explore its features, and support for customization and debugging. 

* **Dockerized Test Databases** - 
then, you might like to try out some of our [dockerized test databases](https://valhuber.github.io/ApiLogicServer/Database-Connectivity/).

* **Your Database** - 
finally, try your own database.

&nbsp;

# Project Information

### Making Contributions
This is an open source project.  We are open to suggestions.  Some of our ideas include:

| Component           | Provides         | Consider Adding                                                                |
|:---------------------------|:-----------------|:-------------------------------------------------------------------------------|
| [1. safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin){:target="_blank" rel="noopener"}      | Admin App        | [Hide/Show, Cascade Add](https://github.com/thomaxxl/safrs-react-admin/issues) |
| 2. [JSON:**API** and Swagger](#jsonapi---related-data-filtering-sorting-pagination-swagger){:target="_blank" rel="noopener"} | API Execution    | Security, Serverless, Kubernetes                                                                       | 
| 3. [Transactional **Logic**](#logic){:target="_blank" rel="noopener"}   | Rule Enforcement | New rule types        |
| 4. This project | API Logic Project Creation | Support for features described above |


To get started, please see  the [Architecture.](Internals)

&nbsp;

### Status

We have tested several databases - see [status here.](Database-Connectivity)

We are tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues){:target="_blank" rel="noopener"}.

We have introduced several renames to clarify operation.
These do not affect existing projects.  However, we've not updated all the docs to reflect these changes:

* `logic/declare_logic.py` replaces `logic_bank.py`
* `api/customize_api.py` replaces `expose_services.py`
* `database/customize_models.py` replaces `models_ext.py`

 &nbsp;

### Acknowledgements

Many thanks to

- [Thomas Pollet](https://www.linkedin.com/in/pollet/), for SAFRS, SAFRS-react-admin, and invaluable design partnership
- [Marelab](https://marmelab.com/en/), for [react-admin](https://marmelab.com/react-admin/)
- Armin Ronacher, for Flask
- Mike Bayer, for SQLAlchemy
- Alex Grönholm, for Sqlacodegen
- [Meera Datey](https://www.linkedin.com/in/meeradatey/), for React Admin prototyping
- Denny McKinney, for Tutorial review
- Achim Götz, for design collaboration and testing
- Max Tardiveau, for testing and help with Docker
- Michael Holleran, for design collaboration and testing
- Nishanth Shyamsundar, for review and testing
- Thomas Peters, for review and testing
- Daniel Gaspar, for Flask AppBuilder
- Gloria Huber and Denny McKinney, for doc review

&nbsp;

### Articles

There are a few articles that provide some orientation to API Logic Server:

* [How Automation Activates Agile](https://modeling-languages.com/logic-model-automation/){:target="_blank" rel="noopener"}
* [How Automation Activates Agile](https://dzone.com/articles/automation-activates-agile){:target="_blank" rel="noopener"} - providing working software rapidly drives agile collaboration to define systems that meet actual needs, reducing requirements risk
* [How to create application systems in moments](https://dzone.com/articles/create-customizable-database-app-systems-with-1-command){:target="_blank" rel="noopener"}
* [Stop coding database backends…Declare them with one command.](https://medium.com/@valjhuber/stop-coding-database-backends-declare-them-with-one-command-938cbd877f6d){:target="_blank" rel="noopener"}
* [Instant Database Backends](https://dzone.com/articles/instant-api-backends){:target="_blank" rel="noopener"}
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even){:target="_blank" rel="noopener"} - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr){:target="_blank" rel="noopener"} - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank){:target="_blank" rel="noopener"} - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence){:target="_blank" rel="noopener"} - focuses on automation, design flexibility and agile iterations
* [Instant Web Apps](https://dzone.com/articles/instant-db-web-apps){:target="_blank" rel="noopener"} 



[^1]:
    See the [FAQ for Low Code](FAQ-Low-Code)