[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

# API Logic Server

### TL;DR - Executable Software, *now*

With 1 command, create a **database API,** to unblock UI development.  Also, a **multi-page web app,** to engage Business Users - early in the project.  Declare logic with **spreadsheet-like rules** - 40X more concise than code, extensible with Python - for remarkable business agility.

Create the sample project in a *minute or two*, using Docker.  With Docker started (Windows, use Powershell):

```
cd ~/dev/servers                   # directory of API Logic Server projects on local host
docker network create dev-network  # only required once (ignore errors if network already exists)

# Start (install if required) the API Logic Server docker container
docker run -it --name api_logic_server --rm --net dev-network -p 5000:5000 -p 8080:8080 -v ${PWD}:/local/servers apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/local/servers/docker_project  # Create and run project using API Logic Server

```


> Already installed?  Upgrade to the latest (3.10.15): ```docker pull apilogicserver/api_logic_server```


After you've explored the [sample](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database) (e.g., find Swagger at [localhost:5000](http://localhost:5000)), try different databases: [try our dockerized test databases](https://github.com/valhuber/ApiLogicServer/wiki/Testing#docker-databases), and then try your own database.

You can picture the process like this:

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/creates-and-runs.png"></figure>

### Feature Summary

| Feature | Providing  | Why it Matters | Using
| :-------------- |:--------------| :------|  :------|
| 1. [JSON:**API** and Swagger](#api-safrs-jsonapi-and-swagger) | Endpoint for each table, with... <br>Filtering, pagination, related data | Unblock Client App Dev | [SAFRS](https://github.com/thomaxxl/safrs/wiki) |
| 2. [Transactional **Logic**](#logic)| *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code)  | Strategic Business Agility | [Logic Bank](https://github.com/valhuber/logicbank#readme) |
| 3. [Basic **Web App**](#basic-web-app---flask-appbuilder) | Instant **multi-page, multi-table** web app | Engage Business Users<br>Back-office Admin | [Flask App Builder](https://flask-appbuilder.readthedocs.io/en/latest/), <br>[fab-quickstart](https://github.com/valhuber/fab-quick-start/wiki) |
| 4. [**Customizable Project**](#3-customize) | Custom Data Model, Endpoints, Logic | Customize and run <br>Re-creation *not* required | PyCharm <br> VS Code ... |
| 5. Model Creation | Python-friendly ORM | Custom Data Access<br>Used by API and Basic Web App | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html) |

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:
* [Tutorial](https://github.com/valhuber/ApiLogicServer/wiki/Tutorial) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server


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

As shown below, there are typically 2-3 "machines" in operation:
* Your **local host** (in grey), where the Customizable Project files (`docker_project`) are stored, 
and your Dev Tools (IDE etc) operate


* The ApiLogicServer Docker **container** (blue), which contains:
  * The **ApiLogicServer**, with CLI (Command Language Interface) commands:
     * **`create`** to create projects on your local host
     * **`run`** to execute projects, utilizing the various runtimes (Flask, SQLAlchemy, SAFRS API, Logic, Flask App Builder)
  * A **Python** environment to support execution, and development using your IDE


* The **database** (purple) can run as a separate Docker container, in your local host, or (for the demo) within the ApiLogicServer docker container
<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/docker/docker-arch-create-run.png"></figure>

<details>
  <summary>Directory Contents</summary>

When you have created your project, you will find the following project directory in `~/dev/servers` on your (grey) local host   (here opened in VS Code):
<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/generated-project.png"></figure>

Your docker container (blue) files include Python, Python libraries, and API Logic Server.  The Python project above utilizes IDE `remote-container` support (visible at the lower left in the preceding diagram), which utilizes the docker container (not local host) version of Python.

You docker container looks like this:

<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/docker/docker-files.png"></figure>

</details>

<details>
  <summary>Alternative option: pip install</summary>

You can also run ApiLogicServer without Docker.  The familiar `pip install ApiLogicServer` creates the ApiLogicServer in your `venv` instead of the Docker container.

We recommend, however, that you take a good look at Docker:
* It avoids a sometimes-tricky Python install
* It isolates your projects into containers
* It is quite likely the eventual deployment architecture, so you're already in step with that
</details>

# Usage Overview

Let's review the steps shown above:
1. Create
2. Run
3. Customize

### Install - `docker run`
Once you've [installed Docker](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker) itself, the `docker run` command above installs the ApiLogicServer docker (if it's not already there), and starts it, opening a terminal window on the Docker container.  Notes:
* the `v ${PWD}:/local/servers` argument is what enables the ApiLogicServer to create / access the project on your local host
   * Windows - Powershell must be used (due to the `$(PWD)` syntax)
   * if you use Command Prompt, specify the local directory completely 

<details>
  <summary>Click to see Docker run argument descriptions, and how to inspect Docker environment</summary>


The **arguments** mean:
* **-it** - launch a terminal window for the Docker container
* **--name api_logic_server** - the name of the image on your local host
* **-rm** - remove the container once it stops (your project files are not lost - they are on your local host)
* **--net dev-network** - attaches to dev-network (see _docker database networking_, below)
* **-p 5000:5000** - maps local (host) part to Docker port 
* **-v ${PWD}:/local/servers** - maps a local directory to a mount name for Docker.  This is where a directory will be created for your new project.  
   * `${PWD}` is your current folder.  
      * You could also provide a specific folder, e.g., `~/dev/servers` (Unix), or `C:\Users\val\dev\servers` (windows)
   * `/local/servers`is the mounted volume reference from inside the Docker container
* **`apilogicserver/api_logic_server`** - the name of the image to pull from Docker Hub.  
   * This will fetch the image first time, and will run it locally on subsequent runs
   * The image is not automatically refreshed -- install ApiLogicServer updates as described below

On your Docker container, you can **inspect** your environment:
```
python py.py
```

Open a new terminal window on your **local host**, and find your docker IP address:

```
docker inspect api_logic_server  # you will find the ip, e.g., 172.17.0.2
```

</details>

### Create
In this step, you are using the ApiLogicServer CLI to create and optionally run your project.  There are 2 alternatives.

##### Create and Run: `ApiLogicServer create-and-run`
The ```ApiLogicServer create-and-run``` command creates your project, and runs the server (verify with swagger):
```
ApiLogicServer create-and-run --project_name=/local/servers/docker_project  # Create and run project using API Logic Server
```

It accepts these arguments:

1. The ```-db_url``` argument defaults to a pre-supplied [sample database](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)

   * Specify a [SQLAlchemy url](https://docs.sqlalchemy.org/en/14/core/engines.html) to use your own database
   

2. the```--project_name``` argument defines the project name (directory); it defaults to ```api_logic_server```


3. Discover other arguments with ```ApiLogicServer run --help```


##### Create only: `ApiLogicServer create`

You can also just create the project with `ApiLogicServer create`.  It accepts the same arguments.

### Run

Run directly from the **Docker** Terminal window:
```
ApiLogicServer run --project_name=/local/servers/docker_project
```
Or, equivalently:
```
python /local/servers/docker_project/api_logic_server_run.py  # run the API Server - test with cURL, Swagger
```
Run the basic web app like this:
```
python /local/servers/docker_project/ui/basic_web_app/run.py  # run the Basic Web App (help for command args)
```

Notes:
* Note you run from the **Docker** (not local) terminal, so that you have the proper Python environment.

* **Key Takeaway:** you do **not** need to repeat the `ApiLogicServer create` command to restart the server.

You can also run using your IDE, as discussed below -- see **Debug, using your IDE**.


### Customize, Extend and Debug with your IDE

The created project is a standard Python project, fully customizable using your existing IDE and other development tools (e.g., `git`).  Open the created project folder (issue this command your **local host**, not the Docker container), configure as described in [Working with IDEs](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs), and use your IDE:
```
code ~/dev/servers/api_logic_server  # local host!  Launch VS Code; use charm for PyCharm
```

* __Important:__ you may need to install the [`shell` extension](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line) into VS Code, so starting it becomes as simple as `code docker_project` (from your **local** terminal window)


* The created project is pre-configured for VS Code to use a [Remote Container](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs#create-the-project)

  * This means it uses Python in the ApiLogicServer docker (not your local host), which _eliminates the need to install and configure Python_


Here is the created project, opened in VS Code:

<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/generated-project.png"></figure>

#### Customize model code

The created project is extremely small, since the created code defines _declarative models,_ rather than low level _procedural code._  Not only does this make it small, it makes it very easy to customize the behavior.

For example, the API is defined (`api/expose_api_models.py` - upper left code pane) with statements as shown below. It's instantly obvious how to alter this code, e.g., to not expose a given table as an endpoint.

```Python
api.expose_object(models.Category)
api.expose_object(mod<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/generated-project.png"></figure>
els.Customer)
api.expose_object(models.CustomerDemographic)
```

The same applies to `ui/basic_web_app/app/view.py` - it's clear how to control what fields are displayed (including joins), and in what order:

```python
class OrderDetailModelView(ModelView):
datamodel = SQLAInterface(OrderDetail)
list_columns = [
"Id", "Order.ShipName", "Product.ProductName", "UnitPrice", "Quantity"]
show_columns = [
"Id", "Order.ShipName", "Product.ProductName", "UnitPrice", "Quantity", "Discount", "Amount", "ShippedDate", "ProductId", "OrderId"]
edit_columns = [
"Id", "UnitPrice", "Quantity", "Discount", "Amount", "ShippedDate", "ProductId", "OrderId"]
add_columns = [
"Id", "UnitPrice", "Quantity", "Discount", "Amount", "ShippedDate", "ProductId", "OrderId"]
related_views = []
```

#### Extend with Python

Typical [customizations](https://github.com/valhuber/ApiLogicServer/wiki/ApiLogicServer-Guide) include
(explore the default sample database to see examples):

* **Customize API:** edit ```api/customize_services.py``` to define your own endpoints, complementing those created from the model
  

* **Customize Model:** edit ```customize_models.py```, for example
    * to define [relationships perhaps not defined in your schema](https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design), critical for multi-table logic, APIs, and web apps
    * to describe derived attributes, so that your API, logic and apps are not limited to the physical data model


* **Customize Logic:** edit ```models/declare_logic.py``` (initially empty) to declare logic
    * As shown above, the default sample database project contains some simple rules you can explore;
  learn more about rules in the [Logic Bank](https://github.com/valhuber/LogicBank)
    

#### Debug, using your IDE
Since the project is standard, you can use your existing IDE services 
such as code completion and debugging.  

For VS Code, the created project has pre-built launch configurations 
for `ApiLogicServer` and the `Basic Web App`.  You can set breakpoints, examine variables, step through code, etc:

<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/docker/VSCode/logic-debug.png"></figure>

# Features
Let's take a closer look at what the created project provides.

### API: SAFRS JSON:API and Swagger

Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/swagger.png"></figure>

> Customize your API by editing ```api/customize_api.py```, and see [Customizing](https://github.com/valhuber/ApiLogicServer/wiki/ApiLogicServer-Guide#customizing-apilogicprojects)

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
<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/logic-declare-5-rules.png"></figure>

> Declare your logic by editing: **```logic/declare_logic.py```**


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

6. **Logic enforcement:** logic is enforced on all updates.  For example, try to alter the `Credit Limit` of the first customer to 20, and observe the error.

    * This is due to the constraint rule in `logic/declare_logic.py` on Customer, containing: `row.Balance <= row.CreditLimit`

If you are using Docker, you can run it like this for the created sample:
```
python /local/servers/docker_project/ui/basic_web_app/run.py  # using the docker terminal window
```

<figure><img src="https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png"></figure>

> Customize your app by editing: **```ui/basic_web_app/app/views.py```**

> Before running, [some setup is required](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Flask-AppBuilder) for Flask App Builder (except for Northwind, which is pre-created).

### React-Admin Creation
ApiLogicServer 2.3.4 can also create react-admin client applications.
This element is for technology exploration - it is _not_ production ready.

[See here](https://github.com/meera/apilogicserver-react-admin-genned#readme)
for more information.

# Internals - How It Works
<details>
  <summary>How It Works</summary>

The ApiLogicServer CLI `create` (or `run`) command creates the project structure shown below.

The executables are shown in blue, corresponding to Run, above.  Your customizations are done to the files noted in green.

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/how-it-works.png"></figure>

### API Execution: `api_logic_server_run.py`

`api_logic_server_run.py` sets up a Flask app, the database, logic and api:

* **Database Setup:** It imports`api/expose_api_models` which imports `database/models.py`, which then imports `database/customize_models.py` for your model extensions.  `api_logic_server_run.py` then sets up flask, and opens the  database with `db = safrs.DB`


* **Logic Setup:** It then calls `LogicBank.activate`, passing `declare_logic` which loads your declared rules. On subsequent updates, logic operates by handling SQLAlchemy `before_flush` events, enforcing the declared logic.  This is non-trivial, using the engine in `LogicBank` (no relation to retail!).


* **API Setup:** It next invokes `api/expose_api_models`.  This calls safrs to create the end points and the swagger information, based on the created `database/models.py` (the models used by the SQLAlchemy ORM).   It finally calls `api/customize.py` where you can add your own services.  The sample includes a trivial Hello World, as well as `add_order`.


### Basic Web App Execution: `ui/basic_web_app/run.py`
run.py executes `from app import app` which
loads the module `ui/basic_web_app/app/__init__.py'; this
loads the models and activates logic.

It then instantiates the class `AppBuilder`, which interprets the `views.py` file that describes your pages and transitions.  You can edit this file to tune what data is displayed, introduce graphs and charts, etc.

</details>


# Installation
As of release 3.00.00, you can install using Docker, or standard
`pip` install.

## Docker Installation
[Docker installation](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker)
enables you to bypass sometimes-tricky Python installs by using Docker.

Docker support provides not only ApiLogicServer, but a Python environment
you can use with your IDE.  It is described above.

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

#### Cloud (reduced functionality)
The cloud demo is less recommended, since you don't get to use Swagger or the Basic Web App.
But you just want to take a quick look the the API, [run the demo using a cloud-based (MyBinder) install](https://github.com/valhuber/ApiLogicServerTutorial).

For your own projects, follow normal procedures to deploy them to the cloud.


### Important News - Certificate Issues
We are starting to see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```


# Project Information

### Status

We have tested several databases - see [status here.](https://github.com/valhuber/ApiLogicServer/wiki/Testing)

We are tracking [issues in git](https://github.com/valhuber/ApiLogicServer/issues).

We have introduced several renames to clarify operation.
These do not affect existing projects.  However, we've not updated all the docs to reflect these changes:
* `logic/declare_logic.py` replaces `logic_bank.py`
* `api/customize_api.py` replaces `expose_services.py`
* `database/customize_models.py` replaces `models_ext.py`

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
- Max Tardiveau, for testing and help with Docker
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

10/02/2021 - 03.01.16: bugfix improper run arg for VSCode launch configuration

09/29/2021 - 03.01.15: run (now just runs without create), added create-and-run

09/24/2021 - 03.01.04: enable run command for Docker execution, pyodbc, fab create-by-copy

09/15/2021 - 03.00.10: auto-create .devcontainer for vscode, configure network, python & debug

09/06/2021 - 02.04.19: Docker foundation, improved Python path / log handling, .vscode, auto copy

08/29/2021 - 02.04.08: Docker foundation, improved Python path handling, IDE files

08/25/2021 - 02.04.00: Docker foundation (work in progress)

08/23/2021 - 02.03.06: Create react-admin app (tech exploration), cmdline debug fix (Issue 17)

