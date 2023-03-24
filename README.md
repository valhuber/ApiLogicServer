---
title:
---

[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

[![API Logic Server Intro](https://github.com/valhuber/apilogicserver/wiki/images/hero-banner.png?raw=true)](https://apilogicserver.github.io/Docs/ "Single command creates executable, customizable projects")

&nbsp;
---

Find the [documentation here](https://apilogicserver.github.io/Docs/).  To explore **(no download, no install),** click...

* here for an [*App Fiddle*](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=594296622) for learning Flask, SQLAlchemy and API Logic Server 

* here for an [Instant Eval](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=593459232)

&nbsp;

# Welcome to API Logic Server

API Logic Server creates __customizable database web app projects:__

* __Creation is Instant:__ create projects with a single command

* __Projects are Highly Functional:__

    * __API:__ an endpoint for each table, with filtering, sorting, pagination and related data access

    * __Admin UI:__ multi-page / multi-table apps, with page navigations and automatic joins

* __Projects are Customizable, using _your IDE_:__ such as VSCode, PyCharm, etc, for familiar edit/debug services

* __Business Logic Automation:__ using unique rules, extensible with Python


&nbsp;

# Background
A brief look at why we built it, and what it is.<br><br>

### Motivation - not instant, propietary IDE, no logic automation

We looked at approaches for building database systems:   

* __Frameworks:__ Frameworks like Flask or Django enable you to build a single endpoint or _Hello World_ page, but a __multi-endpoint__ API and __multi-page__ application would take __weeks__ or more.

* __Low Code Tools:__ these are great for building great UIs, but

    * Want a multi-page app -- __no screen painting__
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

> API Logic Server reads your schema, and creates an executable, customizable project providing the features listed below.  Check it out - __zero install__ - [here, in Codespaces](https://github.com/ApiLogicServer/ApiLogicProject#readme).

&nbsp;

# Feature Summary

|   | Feature    | Providing   | Why it Matters   |
:-------|:-----------|:------------|:-----------------|
| __Instant__ | 1. [**Admin App**](https://apilogicserver.github.io/Docs/Admin-Tour/) | Instant **multi-page, multi-table** app  [(running here on PythonAnywhere)](https://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home)              | Engage Business Users<br>Back-office Admin       |
| | 2. [JSON:**API** and Swagger](https://apilogicserver.github.io/Docs/API/)                     | Endpoint for each table, with... <br>Filtering, pagination, related data                                                                        | Unblock custom App Dev<br>Application Integration                           |
| | 3. Data Model Class Creation                                                     | Classes for Python-friendly ORM                                                                                                                             | Custom Data Access<br>Used by API                |
| __Customizable__ | 4. [**Customizable Project**](https://apilogicserver.github.io/Docs/Project-Structure/)                   | Custom Endpoints, Logic <br>Use Python and your IDE  |Customize and run <br>Re-creation *not* required |                                                                                      
| __Unique Logic__ | 5. [Spreadsheet-like Business Rules](https://apilogicserver.github.io/Docs/Logic-Why/)  &nbsp; :trophy:      | **40X more concise** - compare [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code) | Unique backend automation <br> ... nearly half the system  |
|  | Extensible with Python      | Familiar Event Model | Eg., Send messages, email  |
| Testing | 6. [Behave **Test Framework**](https://apilogicserver.github.io/Docs/Behave/)         | Test Suite Automation<br/>Behave Logic Report<br/>Drive Automation with Agile                                                                                                                           | Optimize Automation to get it fast<br/>Agile Collaboration to get it right                |

&nbsp;

# Instant -- Single Command

Use the CLI to create the sample API and Admin App project, with a single command.

&nbsp;

### Create With Docker

Execute the following commands (Windows, use Powershell):

```bash title="Run API Logic Server in Docker"
# Start the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/localhost/ApiLogicProject --db_url=
```
&nbsp;

### Or, Create With Local Install
Presuming Python 3.7+ [is installed](https://apilogicserver.github.io/Docs/Install/), it's typically:

```bash title="Run API Logic Server from a local pip install"
python -m venv venv                  # may require python3 -m venv venv
source venv/bin/activate             # windows venv\Scripts\activate
venv\Scripts\activate                # mac/linux: source venv/bin/activate
python -m pip install ApiLogicServer

ApiLogicServer create-and-run        # create, or create-and-run; accept defaults
```
&nbsp;

## Execute

Your server is running - explore the data and api at [localhost:5656](http://localhost:5656).  Using the defaults provided above, you have started the [Tutorial](https://apilogicserver.github.io/Docs/Tutorial), the recommended quick start for API Logic Server.

&nbsp;

# Customize in IDE

VSCode and PyCharm users can customize and run/debug within their IDE with [these steps](https://apilogicserver.github.io/Docs/IDE-Execute/).  Created projects include Launch and Docker configurations.  

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png?raw=true"></figure>

[Rebuild services](https://apilogicserver.github.io/Docs/Project-Rebuild/) are provided to accomodate changes to database structure or ORM classes.

&nbsp;

# Overview Video

Project creation is based on database schema introspection as shown below: identify a database, and the ```ApiLogicServer create``` commands creates an executable, customomizable project.

Click for a video tutorial, showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container")

&nbsp;

# Getting Started

### Quick Evaluation - _no install_

You can avoid install hassles by exploring the [Sample Project in Codespaces](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=593459232).  This will enable you to use VSCode - _in your Browser, zero install_ - to:

* see the created project
* use the Tutorial to run, customize and debug it 

We think you'll find Codespaces pretty amazing - check it out!

### Local Install

API Logic Server is designed to make it easy to get started:

* **Install and run Tutorial** - 
[install](https://apilogicserver.github.io/Docs/Install-Express/), and explore the [tutorial](https://apilogicserver.github.io/Docs/Tutorial/).  You'll create a complete project using the pre-installed sample database, explore its features, and support for customization and debugging. 

* **Dockerized Test Databases** - 
then, you might like to try out some of our [dockerized test databases](https://apilogicserver.github.io/Docs/Database-Connectivity/).

* **Your Database** - 
finally, try your own database.

&nbsp;

# Project Information

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:

* [Tutorial](https://apilogicserver.github.io/Docs/Tutorial/) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server

&nbsp;

### Making Contributions
This is an open source project.  We are open to suggestions.  Some of our ideas include:

| Component           | Provides         | Consider Adding                                                                |
|:---------------------------|:-----------------|:-------------------------------------------------------------------------------|
| 1. [JSON:**API** and Swagger](#jsonapi---related-data-filtering-sorting-pagination-swagger) | API Execution    | Serverless, Kubernetes                                                                       | 
| 2. [Transactional **Logic**](#logic)   | Rule Enforcement | New rule types        |
| 3. This project | API Logic Project Creation | Support for features described above |


To get started, please see  the [Architecture.](https://apilogicserver.github.io/Docs/Architecture-Internals/)

&nbsp;

### Status

We have tested several databases - see [status here.](https://apilogicserver.github.io/Docs/Database-Connectivity/)

We are tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues).

 &nbsp;

### Acknowledgements

Many thanks to

- [Thomas Pollet](https://www.linkedin.com/in/pollet/), for SAFRS, SAFRS-react-admin, and invaluable design partnership
- [Marelab](https://marmelab.com/en/), for [react-admin](https://marmelab.com/react-admin/)
- Armin Ronacher, for Flask
- Mike Bayer, for SQLAlchemy
- Alex Grönholm, for Sqlacodegen
- Thomas Peters, for review and testing
- [Meera Datey](https://www.linkedin.com/in/meeradatey/), for React Admin prototyping
- Denny McKinney, for Tutorial review
- Achim Götz, for design collaboration and testing
- Max Tardiveau, for testing and help with Docker
- Michael Holleran, for design collaboration and testing
- Nishanth Shyamsundar, for review and testing
- Gloria Huber and Denny McKinney, for doc review

&nbsp;

### Articles

There are a few articles that provide some orientation to API Logic Server:

* [How Automation Activates Agile](https://modeling-languages.com/logic-model-automation/)
* [How Automation Activates Agile](https://dzone.com/articles/automation-activates-agile) - providing working software rapidly drives agile collaboration to define systems that meet actual needs, reducing requirements risk
* [How to create application systems in moments](https://dzone.com/articles/create-customizable-database-app-systems-with-1-command)
* [Stop coding database backends…Declare them with one command.](https://medium.com/@valjhuber/stop-coding-database-backends-declare-them-with-one-command-938cbd877f6d)
* [Instant Database Backends](https://dzone.com/articles/instant-api-backends)
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even) - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr) - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank) - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence) - focuses on automation, design flexibility and agile iterations
* [Instant Web Apps](https://dzone.com/articles/instant-db-web-apps) 



[^1]:
    See the [FAQ for Low Code](FAQ-Low-Code)

### Change Log

03/23/2023 - 08.01.15: table filters, cloud debug additions, issue 59, 62-4 

03/05/2023 - 08.01.04: python 3.11.2, Werkzeug==2.2.3, mypy initial, logicbank 1.8.3

02/15/2023 - 08.00.01: Declarative Authorization and Authentication

01/05/2023 - 07.00.00: Multi-db, sqlite test dbs, tests run, security prototype, env config

12/21/2022 - 06.05.00: devops, env db uri, api endpoint names, git-push-new-project

12/08/2022 - 06.04.05: Clarify creating docker repo, IP info, logic comments, nested result example

11/22/2022 - 06.03.06: Image, Chkbox, Dialects, run.sh, SQL/Server url change, stop endpoint, Chinook Sqlite

10/02/2022 - 06.02.00: Option infer_primary_key, Oct1 SRA (issue 49), cleanup db/api setup, restore postgres dvr

09/15/2022 - 06.01.00: Multi-app Projects

08/28/2022 - 06.00.01: Admin App show_when, cascade add. Simplify Codespaces swagger url & use default config

06/12/2022 - 05.02.22: No pyodbc by default, model customizations simplified, better logging

05/30/2022 - 05.02.16: Python 3.10, Dockerfile include, start info

05/04/2022 - 05.02.03: alembic for database migrations, admin-merge.yaml

04/27/2022 - 05.01.02: copy_children, with support for nesting (children and grandchildren, etc.)

03/27/2022 - 05.00.06: Introducing [Behave test framework](https://apilogicserver.github.io/Docs/Logic-Tutorial/), LogicBank bugfix

12/26/2021 - 04.00.05: Introducing the Admin app, with Readme Tutorial

11/13/2021 - 03.50.01: rebuild-from-database/model, improved relationship support 

09/15/2021 - 03.00.09: auto-create .devcontainer for vscode, configure network, python & debug
