[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/hero-banner.png?raw=true)](https://valhuber.github.io/ApiLogicServer/ "Click for docs")

&nbsp;
[Docs here](https://valhuber.github.io/ApiLogicServer/)

---

&nbsp;

## Key Features

The `ApiLogicServer create-and-run` command creates a _executable, customizable_ project that provides:


1. [**Admin App**](https://valhuber.github.io/ApiLogicServer/Admin-Tour/) [(running here on PythonAnywhere)](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home) - multi-page, multi-table, automatic joins


2. [**API**](https://valhuber.github.io/ApiLogicServer/API/), and [Swagger](http://apilogicserver.pythonanywhere.com/api) - endpoint for each table, with filtering, pagination, related data


3. [**Business Logic**](https://valhuber.github.io/ApiLogicServer/Logic-Why/#rules-executable-design), using rules for multi-table derivations and constraints, extensible with Python
   * Declare rules as in a spreadsheet - 40X more concise than code
   * Unique to API Logic Server &nbsp; :trophy:

This programmer-friendly low-code microservice creation approach is distinguished by

* leveraging [___your IDE___](https://valhuber.github.io/ApiLogicServer/IDE-Customize/), and
* extending low-code to address frontend ___and backend___ logic.

---

&nbsp;

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
Presuming Python 3.7+ [is installed](Install), it's typically:

```bash title="Run API Logic Server from a local pip install"
python -m venv venv        # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
python -m pip install ApiLogicServer

ApiLogicServer create      # create, or create-and-run; accept defaults
```

### Then, Execute, Open in IDE

Your system is running - explore the data and api at [localhost:5656](http://localhost:5656).

VSCode and PyCharm users can execute within their IDE with [these steps](Execute).


&nbsp;

## Overview Video

Project creation is based on database schema introspection as shown below: identify a database, and the ```ApiLogicServer create``` commands creates an executable, customomizable project.

Click for a video tutorial, showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container")

&nbsp;

## Getting Started

### Install and run Tutorial
Install, and explore the tutorial (created from [this database](https://valhuber.github.io/ApiLogicServer/Sample-Database/)).

### Test databases
Then, you might like to try out some of our [dockerized test databases](https://valhuber.github.io/ApiLogicServer/Database-Connectivity/).

### Your database

Finally, try your own database.


&nbsp;

# Feature Summary

| Feature                                                               | Providing                                                                                                                                       | Why it Matters                                   | Learn More                                                                                 |
|:----------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------------------------------------------------|
| 1. [**Admin App**](https://valhuber.github.io/ApiLogicServer/Admin-Tour/) | Instant **multi-page, multi-table** app                                                                                                         | Engage Business Users<br>Back-office Admin       | [safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin)                         |
| 2. [JSON:**API** and Swagger](https://valhuber.github.io/ApiLogicServer/API/)                     | Endpoint for each table, with... <br>Filtering, pagination, related data                                                                        | Unblock custom App Dev<br>Application Integration                           | [SAFRS](https://github.com/thomaxxl/safrs/wiki)                                            |
| 3. [Transactional **Logic**](https://valhuber.github.io/ApiLogicServer/Logic-Rules-plus-Python/)           | *Spreadsheet-like Rules* <br> **40X more concise** - compare [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code) | Unique backend automation <br> ... nearly half the system                       | [Logic Bank](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python)     |
| 4. [**Customizable Project**](https://valhuber.github.io/ApiLogicServer/Project-Structure/)                   | Custom Data Model, Endpoints, Logic <br>Use Python and yourIDE                                                                                                            | Customize and run <br>Re-creation *not* required | VS Code <br> PyCharm ... |
| 5. Model Creation                                                     | Classes for Python-friendly ORM                                                                                                                             | Custom Data Access<br>Used by API                | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html)                          |
| 6. [Behave **Test Framework**](https://valhuber.github.io/ApiLogicServer/Behave/)    | Test Suite Automation<br/>Behave Logic Report<br/>Drive Automation with Agile                                                                                                                           | Optimize Automation to get it fast<br/>Agile Collaboration to get it right                | [Logic Tutorial](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/)                          |

The following tutorial is a good way to explore API Logic Server.

&nbsp;

# Installation

[Install instructions](https://valhuber.github.io/ApiLogicServer/Install/) are provided in the documentation.

&nbsp;

# Sample Tutorial - API Logic Server

The [Tutorial](https://valhuber.github.io/ApiLogicServer/Tutorial/) contains a complete walk-through of creating, running and customizing a project.  You can follow along just by reading the doc, but for the best experience, run the Tutorial.  It's included in the default sample project -- no databases to install.

&nbsp; 

# Contributions
This is an open source project, and we encourage contributions to the components noted below:

| Component           | Provides         | Consider Adding                                                                |
|:---------------------------|:-----------------|:-------------------------------------------------------------------------------|
| [1. safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin)      | Admin App        | [Hide/Show, Cascade Add](https://github.com/thomaxxl/safrs-react-admin/issues) |
| 2. [JSON:**API** and Swagger](#jsonapi---related-data-filtering-sorting-pagination-swagger) | API Execution    | Security, Serverless, Kubernetes                                                                       | 
| 3. [Transactional **Logic**](#logic)   | Rule Enforcement | New rule types        |
| 4. This project | API Logic Project Creation | Support for features described above |


To get started, please see [API Logic Server Development](https://valhuber.github.io/ApiLogicServer/Internals/).

&nbsp;

# Project Information

### Resources
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:
* [Tutorial](#api-logic-server---sample-tutorial) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server


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
There are a few articles that provide some orientation to Logic Bank and Flask App Builder.
These technologies are automatically created when you use ApiLogicServer:
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

### Change Log

07/24/2022 - 05.03.26: api_logic_server_run refactor, codespaces support

07/15/2022 - 05.03.17: Add swagger_host for create & run, Docker env

07/10/2022 - 05.03.11: Product links to new gh-pages doc site

06/27/2022 - 05.03.06: nw-, with perform_customizations docker

06/22/2022 - 05.03.00: Docker support to load/run project (env or sh), create ApiLogicProject image

06/16/2022 - 05.02.23: Support nw- (sample, no customization) for evaluation

06/12/2022 - 05.02.22: No pyodbc by default, model customizations simplified, better logging

05/30/2022 - 05.02.16: Python 3.10, Dockerfile include, start info

05/25/2022 - 05.02.12: Verified for Python 3.10, improved support for configuring `venv`

05/04/2022 - 05.02.03: alembic for database migrations, admin-merge.yaml

04/24/2022 - 05.01.01: copy_children, with support for nesting (children and grandchildren, etc.)

03/27/2022 - 05.00.06: Introducing [Behave test framework](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/), LogicBank bugfix

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
