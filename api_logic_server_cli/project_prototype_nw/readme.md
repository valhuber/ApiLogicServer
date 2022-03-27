# API Logic Server - Sample Tutorial

You've already completed the `Create` step below, and are now viewing the readme in the created ApiLogicProject - the sample tutorial, created from [this database.](https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database)  

In this tutorial, we will explore:

* **run** - we will first run the Admin App and the JSON:API

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them

This tutorial presumes you are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.  

The diagram below summarizes the create / run / customize process:

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/creates-and-runs.png"></figure>

You can watch the tutorial in [this video.](https://youtu.be/-C5O453Q-Mc)


&nbsp;&nbsp;&nbsp;

## Establish your virtual environment
Install your projects' virtual environment
as described in the [Quick Start](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start).



## Run

Created ApiLogicProjects are instantly executable.  Let's explore the Admin App and the API.

### Admin App: Multi-Page, Multi-Table, Automatic Joins
To run the Admin App, follow these steps:

1. Click **Run and Debug**
   * *Note:* these steps are highlighted in the diagram below
2. Select the `ApiLogicProject` Launch Configuration
3. Press the green run button to start the server
   * If you are runnig Docker / VS Code, and VS Code will suggest opening a Browser (the _preview_ browser is shown below).  Do so, and you should see the Home screen in your Browser.
   * Otherwise, you can:
      * Open a browser at [localhost:5656](localhost_5656), or
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

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/ui-admin/swagger
.png?raw=true"></figure>
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
<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/generated-project.png"></figure>

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

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/docker/VSCode/nw-readme/customize-api.png"></figure>


### Logic
We've all seen excellent technology that can create great User Interfaces. But for transactional systems, their approach to logic is basically "your code goes here".

> That's a problem - for transaction systems, the backend constraint and derivation logic is often *half* the system.
 
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
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. it will look something like `vsc-api_logic_server...`.

&nbsp;&nbsp;&nbsp;


## Appendix - Key Technologies

API Logic Server is based on the projects shown below.
Consult their documentation for important information.

### SARFS JSON:API Server

[SAFRS: Python OpenAPI & JSON:API Framework](https://github.com/thomaxxl/safrs)

SAFRS is an acronym for SqlAlchemy Flask-Restful Swagger.
The purpose of this framework is to help python developers create
a self-documenting JSON API for sqlalchemy database objects and relationships.

These objects are serialized to JSON and 
created, retrieved, updated and deleted through the JSON API.
Optionally, custom resource object methods can be exposed and invoked using JSON.

Class and method descriptions and examples can be provided
in yaml syntax in the code comments.

The description is parsed and shown in the swagger web interface.
The result is an easy-to-use
swagger/OpenAPI and JSON:API compliant API implementation.

### LogicBank

[Transaction Logic for SQLAlchemy Object Models](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python)

Use Logic Bank (nothing to do with banking!) to govern SQLAlchemy update transaction logic - 
multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

Logic Bank is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.
Your logic therefore applies to any SQLAlchemy-based access - JSON:Api, Admin App, etc.


### SQLAlchemy

[Object Relational Mapping for Python](https://docs.sqlalchemy.org/en/13/).

SQLAlchemy provides Python-friendly database access for Python.

It is used by JSON:Api, Logic Bank, and the Admin App.

SQLAlchemy processing is based on Python `model` classes,
created automatically by API Logic Server from your database,
and saved in the `database` directory.


### Admin App

[safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin).

This generated project also contains a React Admin app:
* Multi-page - including page transitions to "drill down"
* Multi-table - master / details (with tab sheets)
* Intelligent layout - favorite fields first, predictive joins, etc
* Logic Aware - updates are monitored by business logic


# Project Structure
This project was created with the following directory structure:

| Directory | Usage                         | Key Customization File             | Typical Customization                                                                 |
|:-------------- |:------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|
| ```api``` | JSON:API                      | ```api/customize_api.py```         | Add new end points / services                                                         |
| ```database``` | SQLAlchemy Data Model Classes | ```database/customize_models.py``` | Add derived attributes, and relationships missing in the schema                       |
| ```logic``` | Transactional Logic           | ```logic/declare_logic.py```       | Declare multi-table derivations, constraints, and events such as send mail / messages |
| ```ui``` | Admin App                     | ```ui/admin/admin.yaml```          | Control field display - order, captions etc.                                          |

In the table above, the _Key Customization Files_ are created as stubs, intended for you to add customizations that extend
the created API, Logic and Admin App.  Since they are separate files, the project can be
recreated (e.g., synchronized with a revised schema), and these files can be easily copied
into the new project, without line-by-line merges.


| Feature                                                               | Providing  | Why it Matters                                          | Learn More                                                                              |
|:----------------------------------------------------------------------|:--------------|:--------------------------------------------------------|:----------------------------------------------------------------------------------------|
| 1. [JSON:**API** and Swagger](#jsonapi---swagger)                     | Endpoint for each table, with... <br>Filtering, pagination, related data | Unblock Client App Dev                                  | [SAFRS](https://github.com/thomaxxl/safrs/wiki)                                         |
| 2. [Transactional **Logic**](#logic)                                  | *Spreadsheet-like Rules* - **40X more concise** <br>Compare Check Credit with [legacy code](https://github.com/valhuber/LogicBank/wiki/by-code)  | Business Agility                                        | [Logic Bank](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python)  |                                                         |
| 3. [**Admin App**](#admin-app-multi-page-multi-table-automatic-joins) | Instant **multi-page, multi-table** web app | Engage Business Users<br>Back-office Admin              | [Admin App](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App) |
| 4. [**Customizable Project**](#customize-and-debug)                   | Custom Data Model, Endpoints, Logic | Customize, run and debug <br>Re-creation *not* required | PyCharm <br> VS Code ...                                                                |
| 5. Model Creation                                                     | Python-friendly ORM | Custom Data Access<br>Used by API and Admin App         | [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html)                       |

## Appendix 2 - Project Information


| About                    | Info                               |
|:-------------------------|:-----------------------------------|
| Created                  | creation-date                      |
| API Logic Server Version | api_logic_server_version           |
| Created in Directory     | api_logic_server_project_directory |
| API Name                 | api_logic_server_api_name          |



