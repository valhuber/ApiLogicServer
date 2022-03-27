[![Downloads](https://pepy.tech/badge/apilogicserver)](https://pepy.tech/project/apilogicserver)
[![Latest Version](https://img.shields.io/pypi/v/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/apilogicserver.svg)](https://pypi.python.org/pypi/apilogicserver/)

# Alert

Recent updates to included libs have broken previous versions of API Logic Server.  After installing, you can repair your existing install like this (your venv should be active):

```
pip install MarkupSafe==1.1.1
pip install Jinja2==2.11.2
```

A new version (5.00.06) is now available, and recommended.

&nbsp;&nbsp;

# API Logic Server

### TL;DR - creates customizable, model-driven database systems - instantly - from your [database](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)

The `ApiLogicServer create-and-run` command creates a _executable, customizable_ project providing:

1. **Automatic Admin App** [(running here on PythonAnywhere)](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home)

   * For instant collaboration and Back Office data maintenance
   * Rich functionality: multi-page, multi-table, automatic joins
   * [Explore](https://github.com/valhuber/ApiLogicServer/wiki/Admin-Tour/) this Admin App, and how to [customize it](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App)


2. **API,** with [Swagger](http://localhost:5656/api)

   * For custom app dev, integration
   * Rich functionality: endpoint for each table, with filtering, pagination, related data
   * [Customizable:](https://github.com/valhuber/ApiLogicServer/wiki#customize-the-api-with-expose_servicespy-add-rpcs-services) add your own endpoints


3. **Business Logic,** for backend processing

   * Spreadsheet-like rules for multi-table derivations and constraints
   * Extensible with Python events for email, messages, etc
   * [Explore](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) how logic can meaningfully improve [conciseness](https://github.com/valhuber/LogicBank/wiki/by-code) and quality

To create the sample API and app project in a *minute or two --*  start Docker, and execute the following commands (Windows, use Powershell):

```
cd ~/Desktop                       # directory of API Logic Server projects on local host

# Start (install if required) the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create-and-run --project_name=/localhost/ApiLogicProject --db_url=  # Working Software, Now

```

Your system is running - explore the data and api 
[locally](localhost:5656),
or [on this deployed systems](http://apilogicserver.pythonanywhere.com/admin-app/index.html#/Home).

VSCode and PyCharm users can execute within their IDE with [these steps](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start).

In addition to Docker, you can [install](#installation) locally, or on the cloud.

You can picture the process as shown in the diagram below; click it for a video tutorial, showing complete project creation, execution, customization and debugging.

[![Using VS Code](https://github.com/valhuber/ApiLogicServer/wiki/images/creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container")

After you've explored the tutorial, try out our [dockerized test databases](https://github.com/valhuber/ApiLogicServer/wiki/Testing#docker-databases), and then try your own database.

> Already installed?  Upgrade to the latest (5.00.06): ```docker pull apilogicserver/api_logic_server``` (you may need to [rebuild your container](https://github.com/valhuber/ApiLogicServer/wiki#apilogicserver-container-upgrades)).


# Feature Summary

| Feature                                                               | Providing                                                                                                                                       | Why it Matters                                   | Learn More                                                                                 |
|:----------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:-------------------------------------------------------------------------------------------|
| 1. [**Admin App**](#admin-app-multi-page-multi-table-automatic-joins) | Instant **multi-page, multi-table** app                                                                                                         | Engage Business Users<br>Back-office Admin       | [safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin)                         |
| 2. [JSON:**API** and Swagger](#jsonapi---swagger)                     | Endpoint for each table, with... <br>Filtering, pagination, related data                                                                        | Unblock custom App Dev                           | [SAFRS](https://github.com/thomaxxl/safrs/wiki)                                            |
| 3. [Transactional **Logic**](#logic)                                  | *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code) | Unique backend automation - nearly half the system                       | [Logic Bank](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python)     |
| 4. [**Customizable Project**](#customize-and-debug)                   | Custom Data Model, Endpoints, Logic                                                                                                             | Customize and run <br>Re-creation *not* required | [VS Code](https://github.com/valhuber/ApiLogicServer/wiki#using-your-ide) <br> PyCharm ... |
| 5. Model Creation                                                     | Python-friendly ORM                                                                                                                             | Custom Data Access<br>Used by API                | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html)                          |

The following tutorial is a good way to explore API Logic Server.

&nbsp;&nbsp;

# API Logic Server - Sample Tutorial

After completing the `Create` step below, you can view the readme in the created ApiLogicProject.  It contains the sample tutorial, created from [this database.](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)  

In this tutorial, we will explore:

* **run** - we will first run the Admin App and the JSON:API

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them

This tutorial presumes you are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.  You will need to configure container and launch configurations for PyCharm - [see here](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start#project-execution) for more information.

The diagram above summarizes the create / run / customize process.  You can watch the tutorial in [this video.](https://youtu.be/-C5O453Q-Mc)


&nbsp;&nbsp;&nbsp;

## Run

Created ApiLogicProjects are instantly executable.  Let's explore the Admin App and the API.

### Admin App: Multi-Page, Multi-Table, Automatic Joins
To run the Admin App, follow these steps:

1. Click **Run and Debug**
   * *Note:* these steps are highlighted in the diagram below
2. Select the `ApiLogicServer` Launch Configuration
3. Press the green run button to start the server
   * If you are running Docker / VS Code, and VS Code will suggest opening a Browser (the _preview_ browser is shown below).  Do so, and you should see the Home screen in your Browser.
   * Otherwise, you can:
      * Open a browser at [localhost:5656](localhost:5656), or
      * Click __View > Command Palette__, select __Simple Browser__, and specify the same url
         * Note: be aware that we have seen some issue where the _simple browser_ fails to start; just use your normal browser  
4. Explore the app: multi-page, multi-table, automatic joins
   * Navigate to `Customer`
     * Depending on your screen size, you may need to hit the "hamburger menu" (top left) to see the left menu
   * Click the Customer row  to see Customer Details
   * Observe the `Placed Order List` tab at the bottom
   * Click the first Order row
   * Click the `Order Detail List` tab at the bottom
   * Click the first __Product Id__ to see its detail information
6. (Close the app (browser), but leave the server running)

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/ui-admin/run-admin-app.png?raw=true"></figure>

&nbsp;&nbsp;

  > **Key Take-away:** instant multi-page / multi-table admin apps, suitable for **back office, and instant agile collaboration.**

&nbsp;

### JSON:API - Related Data, Filtering, Sorting, Pagination, Swagger
Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

The creation process builds not only the API, but swagger so you can explore it.  The Admin App Home page provides a link to the swagger, but it doesn't work in VS Code's simple browser.  So, we'll launch a new Simple Browser, like this:
1. Click __View > Command__ to open the Command Palette
   * Enter command: `Simple Browser: Show`
   * Specify the URL: `http://localhost:5656/api`
2. Explore the swagger
   * Note: you can drag windows to arrange your viewing area
3. (Leave the swagger and server running)

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/ui-admin/swagger.png?raw=true"></figure>
&nbsp;&nbsp;&nbsp;

  > **Key Take-away:** instant *rich* APIs, with filtering, sorting, pagination and swagger.  **Custom App Dev is unblocked.**


&nbsp;&nbsp;&nbsp;

## Customize and Debug

That's quite a good start on a project.  But we've all seen generators that get close, but fail because the results cannot be extended, debugged, or managed with tools such as git and diff.

Let's examine how API Logic Server projects can be customized for both APIs and logic.  We'll first have a quick look at the created project structure, then some typical customizations.

> The API and admin app you just reviewed above were ***not*** customized - they were created completely from the database structure.  For the sample project, we've injected some API and logic customizations, so you can explore them in this tutorial, as described below.


### Project Structure
Use VS Code's **Project Explorer** to see the project structure:

| Directory | Usage                         | Key Customization File             | Typical Customization                                                                 |
|:-------------- |:------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|
| ```api``` | JSON:API                      | ```api/customize_api.py```         | Add new end points / services                                                         |
| ```database``` | SQLAlchemy Data Model Classes | ```database/customize_models.py``` | Add derived attributes, and relationships missing in the schema                       |
| ```logic``` | Transactional Logic           | ```logic/declare_logic.py```       | Declare multi-table derivations, constraints, and events such as send mail / messages |
| ```ui``` | Admin App                     | ```ui/admin/admin.yaml```          | Control field display, ordering, etc.                                                 |

<figure><img src="https://raw.githubusercontent.com/valhuber/ApiLogicServer/main/images/generated-project.png"></figure>

Let's now explore some examples.

### Admin App Customization
There is no code for the Admin app - it's behavior is declared in the `admin.yaml` model file.  Alter this file to control labels, hide fields, change display order, etc:

1. Open **Explorer > ui/admin/admin.yaml**
   * Find and alter the string `- label: 'Placed Order List*'` (e.g, make it plural)
   * Click Save
2. Launch the app: [http://localhost:5656](http://localhost:5656)
3. Load the updated configuration: click __Configuration > Reset__
4. Revisit **Customer > Order** to observe the new label

&nbsp;&nbsp;&nbsp;

  > **Key Take-away:** you can alter labels, which fields are displayed and their order, etc -- via a simple model.  No need to learn a new framework, or deal with low-level code or html.


&nbsp;&nbsp;&nbsp;


### API Customization

While a standards-based API is a great start, sometimes you need custom endpoints tailored exactly to your business requirement.  You can create these as shown below, where we create an additional endpoint for `add_order`.

To review the implementation: 

1. Open **Explorer > api/customize_api.py**:
3. Set the breakpoint as shown
4. Use the swagger to access the `ServicesEndPoint > add_order`, and
   1. **Try it out**, then 
   2. **execute**
5. Your breakpoint will be hit
   1. You can examine the variables, step, etc.
6. Click **Continue** on the floating debug menu (upper right in screen shot below)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>


### Logic
API and UI automation are impressive answers to familiar challenges.  Logic automation is a _unique_ answer to a significant and unaddressed problem:

> For transaction systems, backend constraint and derivation logic is often nearly *half* the system.  This is not addressed by conventional approaches of "your code goes here".
 
The *logic* portion of API *Logic* server is a declarative approach - you declare spreadsheet-like rules for multi-table constraints and derivations.  The 5 rules shown below represent the same logic as 200 lines of Python - a remarkable **40X.**

> Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.

[Logic](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python) consists of rules **and** conventional Python code.  Explore it like this:
1. Open **Explorer > logic/declare_logic.py**:
   * Observe the 5 rules highlighted in the diagram below.  These are built with code completion.
2. Set a breakpoint as shown
   * This event illustrates that logic is mainly _rules,_ extensible with standard _Python code_
3. Using swagger, re-execute the `add_order` endpoint
4. When you hit the breakpoint, expand `row` VARIABLES list (top left)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/declare-logic.png"></figure>

&nbsp;&nbsp;

## Test

You can test using standard api and ui test tools.  We recommend exploring the [Behave framework](https://github.com/valhuber/ApiLogicServer/wiki/Working-With-Behave).

&nbsp;&nbsp;&nbsp;

## Wrap up
Let's recap what you've seen:

* **ApiLogicProject Creation and Execution** - a database API and an Admin App - created automatically from a database, in moments instead of weeks or months


* **Customizable** - the UI, API and Logic - using Visual Studio code, for both editing and debugging


### Next Steps

Explore the [Logic Tutorial](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Tutorial).


### Docker cleanup
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. it will look something like `vsc-ApiLogicProject...`.

&nbsp;&nbsp;&nbsp;

# Project Operations
Please [see the wiki](https://github.com/valhuber/ApiLogicServer/wiki) for 
details on project operations.

# Architectural Overview
Please see [Architecture](https://github.com/valhuber/ApiLogicServer/wiki/Architecture).

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
* **-p 5656:5656** - maps local (host) part to Docker port 
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
Please see [Architecture - How It Works](https://github.com/valhuber/ApiLogicServer/wiki/Architecture#internals---how-it-works).

# Installation
As of release 3.00.00, you can install using Docker (recommended), standard
`pip` install, or PytonAnywhere.

## Installation Options

#### Docker Installation
[Docker installation](https://github.com/valhuber/ApiLogicServer/wiki/Install-Guide#docker-install)
enables you to bypass sometimes-tricky Python installs by using Docker.

Docker support provides not only ApiLogicServer, but a Python environment
you can use with your IDE.  It is described above.

See the link above for more information on install and execution.

#### Local Installation
Caution: Python install is rather more than running an installer.
Use this page to [Verify / Install Python](https://github.com/valhuber/ApiLogicServer/wiki/Install-Guide).

Then, install the ApiLogicServer CLI in the usual manner:

```
python3 -m venv venv       # may require python -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
apt install unixodbc-dev   # Linux only
pip install ApiLogicServer # you may need to use pip3, or restart your terminal session
```


#### Cloud Install - Pythonanwhere
API Logic Server runs well on [pythonanywhere](http://pythonanywhere.com/).  See [these instructions](https://github.com/valhuber/ApiLogicServer/wiki/Install-Guide#pythonanywhere).

Here is the [sample on PythonAnywhere.](http://apilogicserver.pythonanywhere.com/admin-app/index.html)

## Quick Start

Once installed, use the [Quick Start](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start) to create and load the sample project.


## Installation Notes

### Heads up - Certificate Issues
We sometimes see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](https://github.com/valhuber/ApiLogicServer/wiki/Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```


# Project Information

### Tutorials
There are a number of facilities that will quickly enable you to get familiar with API Logic Server:
* [Tutorial](#api-logic-server---sample-tutorial) walks you through the steps of creating a server
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
* [How to create application systems in moments](https://dzone.com/articles/create-customizable-database-app-systems-with-1-command)
* [Stop coding database backends…Declare them with one command.](https://medium.com/@valjhuber/stop-coding-database-backends-declare-them-with-one-command-938cbd877f6d)
* [Instant Database Backends](https://dzone.com/articles/instant-api-backends)
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even) - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr) - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank) - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence) - focuses on automation, design flexibility and agile iterations
* [Instant Web Apps](https://dzone.com/articles/instant-db-web-apps) 

### Change Log

03/27/2022 - 05.00.06: Introducing Behave test framework, LogicBank bugfix

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
