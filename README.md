[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

# API Logic Server

### TL;DR - Executable Software, *now*... Customizable

With 1 command, you get:
* Working Software, ***Now***
  * a **database API,** to unblock UI development
  * a **multi-page web app,** to engage Business Users - early in the project
  * Declarative logic using **unique spreadsheet-like rules** - 40X more concise than code, extensible with Python - for remarkable business agility.
* A **_Customizable_ Project,** using a standard language and tools, in an cleanly isolated, containerized environment that matches your deployment architecture.

To create the sample API and web-app project in a *minute or two --*  start Docker, and execute the following commands (Windows, use Powershell):

```
cd ~/Desktop                       # directory of API Logic Server projects on local host

# Start (install if required) the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/localhost/api_logic_server --db_url=  # Working Software, Now

```

Your API is running - explore it with [swagger](http://localhost:5000).

VSCode and PyCharm users can follow [these simplified steps](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs).

You can picture the process as follows, as shown by this short [**tutorial**](#api-logic-server---sample-tutorial) video showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/ApiLogicServer/blob/main/images/creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/Zo0dUIgRYFg "Using VS Code with the ApiLogicServer container")

After you've explored the tutorial, try out our [dockerized test databases](https://github.com/valhuber/ApiLogicServer/wiki/Testing#docker-databases), and then try your own database.

> Already installed?  Upgrade to the latest (3.20.09): ```docker pull apilogicserver/api_logic_server``` (you may need to [rebuild your container](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs#apilogicserver-container-upgrades)).


# Feature Summary

| Feature | Providing  | Why it Matters | Learn More
| :-------------- |:--------------| :------|  :------|
| 1. [JSON:**API** and Swagger](#jsonapi---swagger) | Endpoint for each table, with... <br>Filtering, pagination, related data | Unblock Client App Dev | [SAFRS](https://github.com/thomaxxl/safrs/wiki) |
| 2. [Transactional **Logic**](#logic)| *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code)  | Strategic Business Agility | [Logic Bank](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) |
| 3. [Basic **Web App**](#basic-web-app) | Instant **multi-page, multi-table** web app | Engage Business Users<br>Back-office Admin | [Flask App Builder](https://flask-appbuilder.readthedocs.io/en/latest/), <br>[fab-quickstart](https://github.com/valhuber/fab-quick-start/wiki) |
| 4. [**Customizable Project**](#customize-and-debug) | Custom Data Model, Endpoints, Logic | Customize and run <br>Re-creation *not* required | [VS Code](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs) <br> PyCharm ... |
| 5. Model Creation | Python-friendly ORM | Custom Data Access<br>Used by API and Basic Web App | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html) |

The following tutorial is a good way to explore API Logic Server.

&nbsp;&nbsp;

# API Logic Server - Sample Tutorial

API Logic Server includes [this sample database,](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)  used for this Tutorial.  We'll install as described above, but use VS Code to run, customize and debug.

<details>
  <summary>Also works with PyCharm</summary>
This tutorial presumes you are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.  You will need to configure container and launch configurations for PyCharm - [see here](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-IDEs) for more information.

</details>

## Install and Create
Pre-reqs:
1. Docker installed and running
2. VS Code (1.61+)

```
cd ~/Desktop                       # directory of API Logic Server projects on local host

# Start API Logic Server container
docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create --project_name=/localhost/api_logic_server --db_url=  # RETURN for sample database

# start VS Code, and open ~/Desktop/api_logic_server
#   1. install the remote-container extension if asked
#   2. re-open in container when asked

```
To begin:
1. Execute the steps above to install API Logic Server and create the sample project
2. Start VS Code, and open the created project (e.g. `~/Desktop/api_logic_server`)

In this tutorial, we will explore:

* **run** - we will first run the Web App and the JSON:API
* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them


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

##### Preparing Flask AppBuilder
Before you run the basic web app on your own database, you must create admin data,
and address certain restrictions (not required for this tutorial).  For more information, see
[Working with Flask AppBuilder](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Flask-AppBuilder).

### JSON:API - Swagger
Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

The creation process builds not only the API, but swagger so you can explore it, like this:
1. Select the `ApiLogicServer` Launch Configuration
2. Press the green run button
   * The app should start, and VS Code will suggest opening a Browser.
3. Explore the swagger
   * For each table, you will find `get` (with filtering, pagination, related data), `patch, post and delete`
4. **Don't stop** the server; we'll use it for debugging...

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/api.png"></figure>

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

#### Customize model code

<details>
  <summary>Customizing Model Code</summary>

The created project is extremely small, since the created code defines _declarative models,_ rather than low level _procedural code._  Not only does this make it small, it makes it very easy to customize the behavior.

For example, the API is defined (`api/expose_api_models.py` - upper left code pane) with statements as shown below. It's instantly obvious how to alter this code, e.g., to not expose a given table as an endpoint.

```Python
api.expose_object(models.Category)
api.expose_object(models.Customer)
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
</details>

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
 
The *logic* portion of API *Logic* server is a declarative approach - you declare spreadsheet-like rules for multi-table constraints and derivations.  The 5 rules shaded below represent the same logic as 200 lines of Python - a remarkable **40X.**

> Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.

[Logic](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) consists of rules **and** conventional Python code.  Explore it like this:
1. Explore the `logic/declare_logic.py` file
   * Observe the 5 rules highlighted in the diagram below.  These are built with code completion.
2. Set a breakpoint as shown
   * This event illustrates that logic is mainly _rules,_ extensible with standard _Python code_
3. Using swagger, re-execute the `add_order` endpoint
4. When you hit the breakpoint, expand `row` (VARIABLES list, top left)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/declare-logic.png"></figure>


&nbsp;&nbsp;&nbsp;

## Tutorial Wrap up
Let's recap what you've seen:

* **Working software now** - a database API and a Web App - created automatically from a database, in moments instead of weeks or months.


* **Customization** - for both the API and Logic - using Visual Studio code, for both editing and debugging

### Docker cleanup
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. it will look something like `vsc-api_logic_server...`.

&nbsp;&nbsp;&nbsp;


### React-Admin Creation
ApiLogicServer 2.3.4 can also create react-admin client applications.
This element is for technology exploration - it is _not_ production ready.

[See here](https://github.com/meera/apilogicserver-react-admin-genned#readme)
for more information.


# Architectural Overview
<details>
  <summary>Docker Containers</summary>
As shown below, there are typically 2-3 "machines" in operation:
* Your **local host** (in grey), where the Customizable Project files (`api_logic_server`) are stored, 
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

Your docker container looks like this:

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
</details>

# Command Language Details


<details>
  <summary>Click to see Docker run argument descriptions, and how to inspect Docker environment</summary>

### Install - `docker run`
Once you've [installed Docker](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker) itself, the `docker run` command above installs the ApiLogicServer docker (if it's not already there), and starts it, opening a terminal window on the Docker container.  Notes:
* the `v ${PWD}:/localhost` argument is what enables the ApiLogicServer to create / access the project on your local host
   * Windows - Powershell must be used (due to the `$(PWD)` syntax)
   * if you use Command Prompt, specify the local directory completely 
   
The **arguments** mean:
* **-it** - launch a terminal window for the Docker container
* **--name api_logic_server** - the name of the image on your local host
* **-rm** - remove the container once it stops (your project files are not lost - they are on your local host)
* **-p 5000:5000** - maps local (host) part to Docker port 
* **-v ${PWD}:/localhost** - maps a local directory to a mount name for Docker.  This is where a directory will be created for your new project.  
   * `${PWD}` is your current folder.  
      * You could also provide a specific folder, e.g., `~/dev/servers` (Unix), or `C:\Users\val\dev\servers` (windows)
   * `/localhost`is the mounted volume reference from inside the Docker container
* **`apilogicserver/api_logic_server`** - the name of the image to pull from Docker Hub.  
   * This will fetch the image first time, and will run it locally on subsequent runs
   * The image is not automatically refreshed -- install ApiLogicServer updates as described below

You may also wish to add a parameter for networking:
* **--net my-network** - attaches to my-network

On your Docker container, you can **inspect** your environment:
```
python py.py
```

Open a new terminal window on your **local host**, and find your docker IP address:

```
docker inspect api_logic_server  # you will find the ip, e.g., 172.17.0.2
```

</details>
    

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
As of release 3.00.00, you can install using Docker (recommended), or standard
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


### Heads up - Certificate Issues
We sometimes see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```


# Project Information

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:
* [Tutorial](https://github.com/valhuber/ApiLogicServer/wiki/Tutorial) walks you through the steps of creating a server
* [Video](https://www.youtube.com/watch?v=gVTdu6c0iSI) shows the steps of creating a server


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

10/24/2021 - 03.20.11: Preliminary admin_app yaml generation (internal, experimental)

10/18/2021 - 03.20.09: Readme Tutorial for IDE users

10/16/2021 - 03.20.07: dev-network no longer required (see Releases)

10/14/2021 - 03.20.06: create in current working directory

10/03/2021 - 03.10.17: default db_url

10/02/2021 - 03.01.16: bugfix improper run arg for VSCode launch configuration

09/29/2021 - 03.01.15: run (now just runs without create), added create-and-run

09/24/2021 - 03.01.04: enable run command for Docker execution, pyodbc, fab create-by-copy

09/15/2021 - 03.00.10: auto-create .devcontainer for vscode, configure network, python & debug

09/06/2021 - 02.04.19: Docker foundation, improved Python path / log handling, .vscode, auto copy

08/29/2021 - 02.04.08: Docker foundation, improved Python path handling, IDE files

08/25/2021 - 02.04.00: Docker foundation (work in progress)

08/23/2021 - 02.03.06: Create react-admin app (tech exploration), cmdline debug fix (Issue 17)

