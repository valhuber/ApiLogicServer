[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

# API Logic Server

### TL;DR - Executable Software, *now*

**ApiLogicServer** creates customizable database api projects with a single command.

Create the sample project in a *minute or two*, using Docker:

```
cd ~/dev/servers                   # directory of api_logic_server projects on local machine
docker network create dev-network  # only required once (ignore errors if network already exists)

docker run -it --name api_logic_server --rm --net dev-network -p 5000:5000 -p 8080:8080 -v ${PWD}:/local/servers apilogicserver/api_logic_server

ApiLogicServer run --project_name=/local/servers/docker_project  # Create and run project on local host machine

```

After you've explored the sample (e.g., Swagger at [localhost:5000](http://localhost:5000)), try different databases: [connect to a Dockerized Databases](#connect-to-dockerized-databases), and then try your own database as [described below](#next-steps).

### Feature Summary

| Feature | Providing  | Why it Matters | Using
| :-------------- |:--------------| :------|  :------|
| 1. [JSON:**API** and Swagger](#api-safrs-jsonapi-and-swagger) | Endpoint for each table, with... <br>Filtering, pagination, related data | Unblock Client App Dev | [SAFRS](https://github.com/thomaxxl/safrs/wiki) |
| 2. [Transactional **Logic**](#logic)| *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code)  | Strategic Business Agility | [Logic Bank](https://github.com/valhuber/logicbank#readme) |
| 3. [Basic **Web App**](#basic-web-app---flask-appbuilder) | Instant **multi-page, multi-table** web app | Engage Business Users<br>Back-office Admin | [Flask App Builder](https://flask-appbuilder.readthedocs.io/en/latest/), <br>[fab-quickstart](https://github.com/valhuber/fab-quick-start/wiki) |
| 4. [**Customizable**](#created-project---customizable-re-runnable) | Custom Data Model, Endpoints, Logic | Customize and run <br>Re-creation *not* required | PyCharm <br> VS Code ... |
| 5. Model Creation | Python-friendly ORM | Custom Data Access<br>Used by API and Basic Web App | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html) |

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:
* [Tutorial](https://github.com/valhuber/ApiLogicServer/wiki/Tutorial) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server
* [Cloud Demo](https://github.com/valhuber/ApiLogicServerTutorial) enables you to run the demo using a cloud-based (MyBinder) install
   * Note: swagger and the Basic Web App are not available using this approach

### Background

There is widespread agreement that APIs are strategic
to the business, required for mobile apps and internal
/ external systems integration.

The problem is that they are time-consuming and costly to develop.
This reduces strategic business agility.

API Logic Server provides exceptional strategic business agility,
by creating an executable server for a database, instantly.
Working Software, now.
 
This **declarative approach** is based on standard Python tooling,
and can be [installed](#Installation) and customized with standard approaches as described below.


# Architectural Overview
The ApiLogicServer docker image contains:
1. The **CLI** (Command Language Interface) to create projects
2. The various **runtimes** (API, Logic, Flask App Builder to execute projects
3. A **Python** environment to support execution, and your IDE

### ApiLogicServer CLI
With a single command, create and run a
[logic](#logic)-enabled
[JSON:API](#api-safrs-jsonapi-and-swagger) and
[web app](#basic-web-app---flask-appbuilder) for your database:

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/creates-and-runs.png"></figure>

As illustrated above, you run the ApiLogicServer CLI to create and optionally run a project:
```
ApiLogicServer run        # see console log, below
```

The CLI provides a number of options you can discover with ```ApiLogicServer --help```.
In particular:
1. The ```-db_url``` parameter defaults to a supplied [sample database](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database).

   * Specify a [SQLAlchemy url](https://docs.sqlalchemy.org/en/14/core/engines.html)
to use your own database.
   

2. By default, the project name (directory) is ```api_logic_server```- override it with the
```-project_name``` option.


3. Discover other options with ```ApiLogicServer run --help```

Use the `run` command to create and run your project, or the `create` command to just create it.


### Created Project - Customizable, Re-runnable

You can execute the project *(without recreating it)* with the **Docker** terminal window:

```
python api_logic_server_run.py  # run the API Server - test with cURL, Swagger
python ui/basic_web_app/run.py  # run the Basic Web App (help for command args)
```

> **Key Takeaway:** you do **not** need to repeat the `ApiLogicServer run` command to start the server.


You will probably prefer to open it with your IDE.  The created Docker project is a standard Python project, fully customizable using your existing IDE and other development tools (e.g., git).  Open the created project folder (it's on your local machine, not the Docker machine), configure as described in [Working with IDEs](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs), and use your IDE.

* Significantly, you can utilize the Python environment from the Docker machine, _eliminating the need to install and configure Python_

* It's pre-configured to use this Python as a [Remote Container](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs#create-the-project) including *launch configurations* for the server and basid wep app, so you basically open the project and proceed

> Tip: install the [`shell` extension](https://stackoverflow.com/questions/30065227/run-open-vscode-from-mac-terminal) into VSCode, so it's basically `code docker_project`, from your **local** terminal window

The sample database provides an excellent opportunity to study one of *key differentiators* of ApiLogicServer - ***declarative logic***:
* The customizable project is open in VSCode, editing `declare_logic.py`, which illustrates how [5 rules can replace 200 lines of code](https://github.com/valhuber/LogicBank/wiki/by-code)
* Create logic, using IDE services such as code completion
* Use IDE services to breakpoints and inspect variables and the log as shown below:

<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/docker/VSCode/logic-debug.png"></figure>

Typical [customizations](https://github.com/valhuber/ApiLogicServer/wiki/ApiLogicServer-Guide) include
(explore the default sample database to see examples):

* **Customize API:** edit ```api/expose_services.py``` to define your own endpoints,
  complementing those created from the model
  

* **Customize Model:** edit ```models_ext.py```, for example
    * to define [relationships perhaps not defined in your schema](https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design), critical for multi-table logic, APIs, and web apps
    * to describe derived attributes, so that your API, logic and apps are not limited to the physical data model


* **Customize Logic:** edit ```models/logic_bank.py``` (initially empty) to declare logic
    * The default sample database project contains some simple rules you can review;
  learn more about rules in the [Logic Bank](https://github.com/valhuber/LogicBank)


After customization, your ```api_logic_server``` project can be re-executed as described above.


# Features

### API: SAFRS JSON:API and Swagger

Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/swagger.png"></figure>

> Customize your API by editing ```api/expose_services.py```, and see [Customizing](https://github.com/valhuber/ApiLogicServer/wiki/ApiLogicServer-Guide#customizing-apilogicprojects)

### Logic

Transactional business logic - multi-table derivations and
constraints - is a significant portion of database systems,
often nearly half.  Procedural coding is time-consuming
to develop and maintain, reducing business agility.

ApiLogicServer integrates Logic Bank, spreadsheet-like rules
that reduce transaction logic by 40X.
Logic is declared in Python (example below), and is:

- **Extensible:** logic consists of rules (see below), plus standard Python code

- **Multi-table:** rules like ``sum`` automate multi-table transactions

- **Scalable:** rules are pruned and optimized; for example, sums are processed as *1 row adjustment updates,* rather than expensive SQL aggregate queries

- **Manageable:** develop and debug your rules in IDEs, manage it in SCS systems (such as `git`) using existing procedures

The following 5 rules represent the
[same logic](https://github.com/valhuber/LogicBank/wiki/by-code)
as 200 lines of Python:
<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/example.png"></figure>

> Declare your logic by editing: **```logic/logic_bank.py```**


### Basic Web App - Flask Appbuilder

UI development takes time.  That's a problem since
* Such effort may not be warranted for admin "back office" screens,
and
  
* [Agile approaches](https://agilemanifesto.org) depend on getting _working
software_ soon, to drive _collaboration and iteration_.

ApiLogicServer CLI therefore creates working software _now:_
multi-page, multi-table applications as shown below:

1. **Multi-page:** apps include 1 page per table

2. **Multi-table:** pages include ``related_views`` for each related child table, and join in parent data

3. **Favorite fields first:** first-displayed field is "name", or `contains` "name" (configurable)

4. **Predictive joins:** favorite field of each parent is shown (product *name* - not product *id*)

5. **Ids last:** such boring fields are not shown on lists, and at the end on other pages

<figure><img src="https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png"></figure>

> Customize your app by editing: **```ui/basic_web_app/app/views.py```**

> Before running, [some setup is required](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Flask-AppBuilder) for Flask App Builder (except for Northwind, which is pre-created).

### React-Admin Creation
ApiLogicServer 2.3.4 can also create react-admin client applications.
This element is for technology exploration - it is _not_ production ready.

[See here](https://github.com/meera/apilogicserver-react-admin-genned#readme)
for more information.

# Installation
As of release 3.00.00, you can install using Docker, or standard
`pip` install.

## Docker Installation
[Docker installation](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker)
enables you to bypass sometimes-tricky Python installs by using Docker.

Docker support provides not only ApiLogicServer, but a Python environment
you can use with your IDE.

```
cd ~/dev/servers                   # directory of api_logic_server projects on local machine
docker network create dev-network  # only required once (ignore errors if network already exists)

# Step 1 - install and start ApiLogicServer
docker run -it --name api_logic_server --rm --net dev-network -p 5000:5000 -p 8080:8080 -v ${PWD}:/local/servers apilogicserver/api_logic_server

# Step 2 - create project on local host machine
ApiLogicServer create --project_name=/local/servers/docker_project

# Step 3 - run the created ApiLogicServer project
python /local/servers/docker_project/api_logic_server_run.py

```

See the link above for more information on install and execution.

## Local Installation
Caution: Python install is rather more than running an installer.
Use this page to [Verify / Install Python](https://github.com/valhuber/ApiLogicServer/wiki/Python-Verify-and-Install).

Then, install the ApiLogicServer CLI in the usual manner:

```
virtualenv venv            # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
pip install ApiLogicServer # you may need to use pip3, or restart your terminal session
```

### Important News - Certificate Issues
We are starting to see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```

# Next Steps
Create the sample project, and take the [tutorial](https://github.com/valhuber/ApiLogicServer/wiki/Tutorial) to explore locally installed ApiLogicServer:

```
ApiLogicServer run
```
>  Note: use ```ApiLogicServer run --help``` for options, e.g., to use a port other than 5000.

(You can also try it with no install on the Cloud, use [this version of the Tutorial](https://github.com/valhuber/ApiLogicServerTutorial#readme).  Note: swagger and the Basic Web App are not available using this approach).  

After creating / exploring the sample project and Tutorial, try it with your own database:

```
ApiLogicServer run --db_url=mysql+pymysql://root:p@localhost/classicmodels
```

The run command provides several useful examples of how to specify `db_url`, a SQLAlchemy uri.


# Project Information

### Status

We have tested several databases - see [status here.](https://github.com/valhuber/ApiLogicServer/wiki/Testing)

We are tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues).

### Acknowledgements

Many thanks to

- Armin Ronacher, for Flask
- Mike Bayer, for SQLAlchemy
- [Thomas Pollet](https://www.linkedin.com/in/pollet/), for SAFRS, and invaluable design assistance
- Daniel Gaspar, for Flask AppBuilder
- Alex Grönholm, for Sqlacodegen
- [Meera Datey](https://www.linkedin.com/in/meeradatey/), for creating React Admin user interface
- Denny McKinney, for Tutorial review
- Achim Götz, for design collaboration and testing
- Max Tardiveau, for testing
- Michael Holleran, for design collaboration and testing
- Nishanth Shyamsundar, for review and testing
- Thomas Peters, for review and testing
- Gloria Huber and Denny McKinney, for doc review

### Articles
There are a few articles that provide some orientation to Logic Bank and Flask App Builder.
These technologies are automatically created when you use ApiLogicServer:
* [Stop coding database backends…Declare them with one command.](https://medium.com/@valjhuber/stop-coding-database-backends-declare-them-with-one-command-938cbd877f6d)
* [Instant Database Backends](https://dzone.com/articles/instant-api-backends)
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even) - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr) - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank) - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence) - focuses on automation, design flexibility and agile iterations
* [Instant Web Apps](https://dzone.com/articles/instant-db-web-apps) 

### Change Log

09/15/2021 - 03.00.10: auto-create .devcontainer for vscode, configure network, python & debug

09/06/2021 - 02.04.19: Docker foundation, improved Python path / log handling, .vscode, auto copy

08/29/2021 - 02.04.08: Docker foundation, improved Python path handling, IDE files

08/25/2021 - 02.04.00: Docker foundation (work in progress)

08/23/2021 - 02.03.06: Create react-admin app (tech exploration), cmdline debug fix (Issue 17)

07/22/2021 - 02.02.29: help command arg for starting APILogicServer / Basic Web App; SAFRS 2.11.5

05/27/2021 - 02.02.28: Flask AppBuilder 3.3.0

05/26/2021 - 02.02.27: Clearer logicbank multi-table chain log - show attribute names

05/23/2021 - 02.02.18: TVF multi-row fix; ApiLogicServer Summary - Console Startup Banner

05/21/2021 - 02.02.17: SAFRS Patch Error Fix, model gen for Posting w/o autoIncr, Startup Tests

05/10/2021 - 02.02.09: Extended Builder fix - no-arg TVFs

05/08/2021 - 02.02.08: Server Startup Option

05/03/2021 - 02.01.05: --extended_builder - bypass Scalar Value Functions

04/30/2021 - 02.01.04: --extended_builder - multiple Table Value Functions example running

04/26/2021 - 02.01.00: Improved Services, option --extended_builder (e.g., restify Table Value Functions)

04/23/2021 - 02.00.15: bug fix - SQLAlchemy version, server port

04/20/2021 - 02.00.12: pythonanywhere - port option, wsgi creation

04/13/2021 - 02.00.10: Improved model error recovery; fix sql/server char type (issues # 13)

04/11/2021 - 02.00.06: Minor - additional CLI info

04/09/2021 - 02.00.05: Bug Fix - View names with spaces

03/30/2021 - 02.00.02: Create Services table to avoid startup issues

03/23/2021 - 02.00.01: Minor doc changes, CLI argument simplification for default db_url

03/17/2021 - 02.00.00: Create create_admin.sh, copy sqlite3 DBs locally, model_ext

03/10/2021 - 01.04.10: Fix issues in creating Basic Web App

03/03/2021 - 01.04.09: Services, cleanup main api_run

02/23/2021 - 01.04.08: Minor - proper log level for APIs

02/20/2021 - 01.04.07: Tutorial, Logic Bank 0.9.4 (bad warning message)

02/08/2021 - 01.04.05: add employee audit foreign key in nw.sqlite

02/07/2021 - 01.04.04: fix default project name

02/07/2021 - 01.04.03: db_url default (for Jupyter)

02/07/2021 - 01.04.02: Internal Renaming

02/06/2021 - 01.04.00: Fix constraint reporting, get related (issues 7,8)

01/31/2021 - 01.03.00: Resolve n:m relationships (revised models.py)

01/29/2021 - 01.02.04: Minor cleanup

01/29/2021 - 01.02.03: Flask AppBuilder fixes - Admin setup, class vs table names (wip)

01/28/2021 - 01.02.02: Command line cleanup

01/27/2021 - 01.02.00: Many
* Host option
* --from_git defaults to local directory
* hello world example
* nw rules pre-created

01/25/2021 - 01.01.01: MySQL fixes
