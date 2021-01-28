# API Logic Server

There is widespread agreement that APIs are strategic
to the business, required for mobile apps and internal
/ external systems integration.

The problem is that they are time-consuming and costly to develop.
This reduces strategic business agility.

API Logic Server provides strategic business agility,
by creating executable APIs from a database, instantly:

- **API:** [swagger/OpenAPI](https://swagger.io/)
  and [JSON:API](https://jsonapi.org) compliant.
  Uses [SAFRS](https://github.com/thomaxxl/safrs/wiki), a modern approach that enables client applications to configure their own API to reduce network traffic.


- **Logic:** spreadsheet-like rules for multi-table derivations and constraint
  that reduce transaction logic by 40X,
  using [Logic Bank](https://pypi.org/project/logicbank).


- **Web App:** a multi-page, multi-table web app;
  uses [fab-quickstart](https://pypi.org/project/fab-quick-start).
  
This declarative approach is based on standard Python tooling,
and can be customized with standard approaches as described below.

## Usage

### Install with ```pip```
Caution: Python install is rather more than running an installer.
Use this page to [Verify / Install Python](../../wiki/Python-Verify-and-Install).
Then:

```
cd ~/Desktop
mkdir server
cd server
virtualenv venv
source venv/bin/activate
# windows venv\Scripts\activate
pip install ApiLogicServer
```

### Quick Start - Create and Execute
This verifies proper install - it will
create and run a [*customizable* ApiLogicServer Project](../../wiki/ApiLogicServer-Guide):

```
ApiLogicServer run
```

The ``db_url`` parameter defaults to a supplied [sample database](../../wiki/Sample-Database).
Specify a [SQLAlchemy url](https://docs.sqlalchemy.org/en/14/core/engines.html)
to use your own database.


### Create (only)

You can also create the project, without execution.
As above, this verifies proper install:

```
ApiLogicServer create --project_name=my_api_logic_server
cd my_api_logic_server
virtualenv venv
source venv/bin/activate
# windows venv\Scripts\activate
pip install -r requirements.txt
```

You may also wish to include the ``open_with`` parameter,
to open an IDE or Editor on the created project.  For example,
PyCharm (``charm``) will open the project and create / initialize the ``venv``
automatically (some PyCharm configuration may be required):

```
ApiLogicServer create --project_name=my_api_logic_server db_url=sqlite:///nw.sqlite --open_with=charm
```

### Execution
With a proper [virtual environment](../../wiki/ApiLogicServer-Guide#environment):

```
python api_logic_server_run.py
python ui/basic_web_app/run.py
```


## Features


### API: SAFRS JSON:API and Swagger

Your API is instantly ready to support ui and integration
development, available in swagger:

<figure><img src="images/swagger.png"></figure>

> Customize your API: edit **```api_logic_server_run.py```**, and see [Customizing](../../wiki/ApiLogicServer-Guide#customizing-apilogicprojects)

### Logic

Transactional business logic - multi-table derivations and
constraints - are a significant portion of database systems,
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

ApiLogicServers therefore generate multi-page, multi-table
applications as shown below:

1. **Multi-page:** apps include 1 page per table

2. **Multi-table:** pages include ``related_views`` for each related child table, and join in parent data

3. **Favorite field first:** first-displayed field is "name", or `contains` "name" (configurable)

4. **Predictive joins:** favorite field of each parent is shown (product *name* - not product *id*)

5. **Ids last:** such boring fields are not shown on lists, and at the end on other pages

<figure><img src="https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png"></figure>

> Customize your app by editing: **```ui/basic_web_app/app/views.py```**

## Status
Pre-Alpha / Technology Preview - just entering test.

Initially released 1/19/2021, the project is beginning to stablize.  We have tested several sqlite databases, and several MySQL databases.  These are both successfully creating the API and the web app.

The [default Northwind project](../../wiki/Sample-Database) pre-creates logic, which is working with both the API and the web app.

We tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues).

## Acknowledgements

Many thanks to

- Thomas Pollet, for SAFRS
- Daniel Gaspar, for Flask AppBuilder
- Achim Götz, for design collaboration



### Articles
There a few articles that provide some orientation to Logic Bank and Flask App Builder.
These technologies are automatically created when you use ApiLogicServer:
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even) - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr) - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank) - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence) - focuses on automation, design flexibility and agile iterations
* [Instant Web Apps](https://dzone.com/articles/instant-db-web-apps) 

## Change Log

1.02.00 - Many:

1. Renamed logic/rules_bank to logic/logic_bank

1. Improved error handling on introspection failures

1. Building backrefs for relationships (with disambiguation)

1. Project creation defaults to copy (vs git clone)

1. Rules are pre-populated for the default (Northwind) database

1.01.02 - --host option, from_git supports local directory, hello world example

1.01.01 - Preliminary fixes for MySQL - acknowledgements (and thanks!) to Thomas Pollet

1.01.00 - ``use_model`` option, to use existing (manually repaired) model --
see [Troubleshooting](../../wiki/Troubleshooting)

1.0.9   - ``Run`` command

1.0.8   - Fix windows bug, options to specify clone-from and open-with

1.0.7   - Initial Version
