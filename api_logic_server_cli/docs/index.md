---
title:
---

[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

[![API Logic Server Intro](https://github.com/valhuber/apilogicserver/wiki/images/hero-banner.png?raw=true)](https://valhuber.github.io/ApiLogicServer/ "Single command creates executable, customizable projects")

## Key Features

1. [**Admin Web App**](Admin-Tour) [(running here on PythonAnywhere)](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home){:target="_blank" rel="noopener"} - multi-page, multi-table, automatic joins
2. [**API**](API) - endpoint for each table, with filtering, sorting, pagination, related data.  And [Swagger](http://apilogicserver.pythonanywhere.com/api#){:target="_blank" rel="noopener"}.
3. [**Unique Backend Logic**](Logic-Why) - _multi-table_ derivations and constraints, using spreadsheet-like rules, extensible with Python.

    * 40X more concise than code
    * Unique to API Logic Server &nbsp; :trophy:

This programmer-friendly low-code microservice creation approach is distinguished by

* leveraging [___your IDE___](IDE-Customize){:target="_blank" rel="noopener"}, and
* extending low-code to address frontend ___and backend___ logic.

---

## Instant -- Single Command

Create the sample API and Admin App project with a single command, using either Docker or a local install.

### Create With Docker

Execute the following commands (Windows, use Powershell):

```bash title="Run API Logic Server in Docker"
# Start the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/localhost/ApiLogicProject --db_url=
```

### Or, Create With Local Install
Presuming Python 3.7+ [is installed](Install){:target="_blank" rel="noopener"}, it's typically:

```bash title="Run API Logic Server from a local pip install"
python -m venv venv        # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
venv\Scripts\activate      # mac/linux: source venv/bin/activate
python -m pip install ApiLogicServer

ApiLogicServer create      # create, or create-and-run; accept defaults
```

### Then, Execute, Open in IDE

Your system is running - explore the data and api at [localhost:5656](http://localhost:5656).  Using the defaults provided above, you have started the [Tutorial](Tutorial/){:target="_blank" rel="noopener"}, the recommended quick start for API Logic Server.

VSCode and PyCharm users can execute within their IDE with [these steps](IDE-Execute){:target="_blank" rel="noopener"}.

&nbsp;

## Overview Video

Project creation is based on database schema introspection as shown below: identify a database, and the ```ApiLogicServer create``` commands creates an executable, customomizable project.

Click for a video tutorial, showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container"){:target="_blank" rel="noopener"}

&nbsp;

## Getting Started

### Install and run Tutorial
[Install](https://valhuber.github.io/ApiLogicServer/Install-Express/), and explore the [tutorial](https://valhuber.github.io/ApiLogicServer/Tutorial/).  You'll create a complete project using the pre-installed sample database, explore its features, and support for customization and debugging. 

### Dockerized Test Databases
Then, you might like to try out some of our [dockerized test databases](https://valhuber.github.io/ApiLogicServer/Database-Connectivity/).

### Your Database

Finally, try your own database.

&nbsp;

## Feature Summary

| Feature                                                               | Providing                                                                                                                                       | Why it Matters                                   | Learn More                                                                                 |
|:----------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------------------------------------------------|
| 1. [**Admin App**](Admin-Tour){:target="_blank" rel="noopener"} | Instant **multi-page, multi-table** app  [(running here on PythonAnywhere)](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home){:target="_blank" rel="noopener"}              | Engage Business Users<br>Back-office Admin       | [safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin){:target="_blank" rel="noopener"}                         |
| 2. [JSON:**API** and Swagger](API){:target="_blank" rel="noopener"}                     | Endpoint for each table, with... <br>Filtering, pagination, related data                                                                        | Unblock custom App Dev<br>Application Integration                           | [SAFRS](https://github.com/thomaxxl/safrs/wiki){:target="_blank" rel="noopener"}                                            |
| 3. [Transactional **Logic**](Logic-Rules-plus-Python){:target="_blank" rel="noopener"}  &nbsp; :trophy:      | *Spreadsheet-like Rules* <br> **40X more concise** - compare [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code){:target="_blank" rel="noopener"} | Unique backend automation <br> ... nearly half the system                       | [Logic Bank](Logic-Tutorial){:target="_blank" rel="noopener"}     |
| 4. [**Customizable Project**](Project-Structure){:target="_blank" rel="noopener"}                   | Custom Data Model, Endpoints, Logic <br>Use Python and yourIDE                                                                                                            | Customize and run <br>Re-creation *not* required | [VS Code](https://github.com/valhuber/ApiLogicServer/wiki#using-your-ide){:target="_blank" rel="noopener"} <br> PyCharm ... |
| 5. Model Creation                                                     | Classes for Python-friendly ORM                                                                                                                             | Custom Data Access<br>Used by API                | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html)                          |
| 6. [Behave **Test Framework**](Behave)         | Test Suite Automation<br/>Behave Logic Report<br/>Drive Automation with Agile                                                                                                                           | Optimize Automation to get it fast<br/>Agile Collaboration to get it right                | [Logic Tutorial](../Logic:-Tutorial)                          |

The [tutorial](Tutorial) is a good way to explore API Logic Server.

&nbsp;

## Making Contributions
This is an open source project.  We are open to suggestions.  Some of our ideas include:

| Component           | Provides         | Consider Adding                                                                |
|:---------------------------|:-----------------|:-------------------------------------------------------------------------------|
| [1. safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin){:target="_blank" rel="noopener"}      | Admin App        | [Hide/Show, Cascade Add](https://github.com/thomaxxl/safrs-react-admin/issues) |
| 2. [JSON:**API** and Swagger](#jsonapi---related-data-filtering-sorting-pagination-swagger){:target="_blank" rel="noopener"} | API Execution    | Security, Serverless, Kubernetes                                                                       | 
| 3. [Transactional **Logic**](#logic){:target="_blank" rel="noopener"}   | Rule Enforcement | New rule types        |
| 4. This project | API Logic Project Creation | Support for features described above |


To get started, please see  the [Architecture.](Internals)

&nbsp;

## Project Information

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:

* [Tutorial](Tutorial) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server


### Status

We have tested several databases - see [status here.](Database-Connectivity)

We are tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues){:target="_blank" rel="noopener"}.

We have introduced several renames to clarify operation.
These do not affect existing projects.  However, we've not updated all the docs to reflect these changes:

* `logic/declare_logic.py` replaces `logic_bank.py`
* `api/customize_api.py` replaces `expose_services.py`
* `database/customize_models.py` replaces `models_ext.py`

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

### Change Log

07/15/2022 - 05.03.17: Add swagger_host for create & run, Docker env

07/04/2022 - 05.03.10: Docs using mkdocs-material (vs. wiki)

06/27/2022 - 05.03.06: nw-, with perform_customizations docker

06/22/2022 - 05.03.00: Docker support to load/run project (env or sh), create ApiLogicProject image

06/16/2022 - 05.02.23: Support nw- (sample, no customization) for evaluation

06/12/2022 - 05.02.22: No pyodbc by default, model customizations simplified, better logging

05/30/2022 - 05.02.16: Python 3.10, Dockerfile include, start info

05/25/2022 - 05.02.12: Verified for Python 3.10, improved support for configuring `venv`

05/04/2022 - 05.02.03: alembic for database migrations, admin-merge.yaml

04/24/2022 - 05.01.01: copy_children, with support for nesting (children and grandchildren, etc.)

03/27/2022 - 05.00.06: Introducing [Behave test framework](../Logic:-Tutorial), LogicBank bugfix

02/18/2022 - 04.02.03: SqlServer fixes, rebuild creates '-created' versions for data model repair

01/18/2022 - 04.01.01: fix [startup failure](https://github.com/valhuber/ApiLogicServer/issues/32) on created app (windows pip-install version only)

01/14/2022 - 04.01.00: add info_disp/show, attribute info, performance, date fix

12/26/2021 - 04.00.05: Introducing the Admin app, with Readme Tutorial

11/13/2021 - 03.50.00: rebuild-from-database/model, improved relationship support 

11/04/2021 - 03.40.01: Per macOS Monterey, default ports to 5001, 5002

10/18/2021 - 03.20.11: Readme Tutorial for IDE users

10/16/2021 - 03.20.07: dev-network no longer required (see Releases)

10/03/2021 - 03.10.17: default db_url

10/02/2021 - 03.01.16: bugfix improper run arg for VSCode launch configuration

09/29/2021 - 03.01.15: run (now just runs without create), added create-and-run

09/25/2021 - 03.01.10: enable run command for Docker execution, pyodbc, fab create-by-copy

09/15/2021 - 03.00.09: auto-create .devcontainer for vscode, configure network, python & debug

09/10/2021 - 03.00.02: rename logic_bank to declare_logic, improved logging

[^1]:
    See the [FAQ for Low Code](FAQ-Low-Code)