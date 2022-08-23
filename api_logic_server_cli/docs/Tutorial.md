## About this Tutorial

This Tutorial is designed for these scenarios:

* You have executed the `ApiLogicServer create` step, have opened the created [default project](https://valhuber.github.io/ApiLogicServer/Sample-Database/) in your IDE, and want to explore a typical project

   * Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.

* You are reviewing the docs, and want to get a sense of the software

In this tutorial, we will explore:

* **create** - we will briefly review what actually happened during the create process

* **run** - we will first run the Admin App and the JSON:API.  These will illustrate how automation creates an app and API from a data model.  You can then infer what you'd get for one of your databases.

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them.

&nbsp;&nbsp;

---

## Key Underlying Concepts
This tutorial illustrates some key concepts:

### _Declarative Models_, not code
Observe that the files for the Admin App and API are models that describe _what, not how_.  This makes it much easier to understand than large amounts of generated code.

### Preserve Customizations
The system is designed to enable `rebuild`, so you can iterate the data model - _without losing your customizations._  In general, such customizations are kept in separate files from the model files.  So, the model files can be rebuilt without affecting customization files.

### Logic Automation
A unique feature of API Logic Server is provision for spreadsheet-like rules for multi-table derivations and constraints, extensible with Python.

&nbsp;&nbsp;

---

## Create

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images//creates-and-runs-video.jpg?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container - click for video")

The diagram above summarizes the create / run / customize process.  When you issue the `ApiLogicServer create` CLI command, the system reads your schema and creates a customizable API Logic Project.

> It's a video - click to view.

&nbsp;

## Create and establish Python Environment

After creation, you must establish your Python environment:

* This is already complete for Codespace users
* Other users - please  see [Quick Start > Express Install](https://valhuber.github.io/ApiLogicServer/IDE-Execute/), which explains how to:

   1. Install API Logic Server
   2. Create the sample Tutorial API Logic Server Project
   3. Open it in your IDE
   4. Prepare the projects' Python environment
   5. Start the Server, and open the Admin App in the Browser


&nbsp;&nbsp;

---

## Run

With the server started and the Admin App open in your Browser, we are ready to explore the Admin App and the API.

&nbsp;

### Admin App: Multi-Page, Multi-Table, Automatic Joins

After starting the server and browser, explore the Admin App in your browser:

1. Navigate to `Customer`
      * Depending on your screen size, you may need to hit the "hamburger menu" (top left) to see the left menu<br/><br/>
2. Click the Customer row  to see Customer Details
3. Observe the `Placed Order List` tab at the bottom
4. Click the first Order row
5. Observe the `Order Detail List` tab at the bottom
6. Observe the elements shown in the diagram

      * Multi-Page - 2 pages for each table (list, with search, and display)
      * Multi-Table - database relationships (typically from foreign keys) used to build master/detail pages
      * Automatic Joins - the Order Detail table contains `ProductId`, but the system has joined in the `Product Name`.  You can edit the `admin.yaml` file to control such behavior.

7. __Leave the server and browser running__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/run-admin-app.png?raw=true"></figure>

&nbsp;&nbsp;

  > :bulb: **Key Take-away:** instant multi-page / multi-table admin apps, suitable for **back office, and instant agile collaboration.**

&nbsp;

### JSON:API - Related Data, Filtering, Sorting, Pagination, Swagger
Your API is instantly ready to support ui and integration
development, available in swagger, as shown below.  JSON:APIs are interesting because they
are client configurable to **reduce network traffic** and **minimize organizational dependencies.**

The creation process builds not only the API, but also swagger so you can explore it.  The Admin App Home page provides a link to the swagger.  In the browser:

1. Click __Home__ to open the Home Page
2. Click "2. API with __oas/Swagger__" to see the swagger
3. (Leave the swagger and server running)

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/swagger.png?raw=true"></figure>
&nbsp;&nbsp;&nbsp;

  > :bulb: **Key Take-away:** instant *rich* APIs, with filtering, sorting, pagination and swagger.  **Custom App Dev is unblocked.**

&nbsp;&nbsp;

---

## Customize and Debug

That's quite a good start on a project.  But we've all seen generators that get close, but fail because the results cannot be extended, debugged, or managed with tools such as git and diff.

Let's examine how API Logic Server projects can be customized for both APIs and logic.  We'll first have a quick look at the created project structure, then some typical customizations.

> The API and admin app you just reviewed above were ***not*** customized - they were created completely from the database structure.  For the sample project, we've injected some API and logic customizations, so you can explore them in this tutorial, as described below.

&nbsp;

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
3. Load the updated configuration: in the running Admin App, click __Configuration > Reset__ and __Apply__
4. Revisit **Customer > Order** to observe the new label

&nbsp;&nbsp;&nbsp;

  > :bulb: **Key Take-away:** you can alter labels, which fields are displayed and their order, etc -- via a simple model.  No need to learn a new framework, or deal with low-level code or html.


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

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/tutorial/customize-api.png?raw=true"></figure>

&nbsp;

### Logic
API and UI automation are impressive answers to _familiar_ challenges.  Logic automation is a _unique_ answer to a significant and unaddressed problem:

> :exclamation: For transaction systems, backend constraint and derivation logic is often nearly *half* the system.  This is not addressed by conventional approaches of "your code goes here".
 
The *logic* portion of API *Logic* server is a declarative approach - you declare spreadsheet-like rules for multi-table constraints and derivations.  The 5 rules shown below represent the same logic as 200 lines of Python - a remarkable **40X.**

> :bulb: Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.  Like a spreadsheet, rules __watch__ for changes, __react__ by automatically executing relevant rules, which can __chain__ to activate other rules; you can [visualize the process here](https://valhuber.github.io/ApiLogicServer/Logic-Operation/#watch-react-chain).

[Logic](https://valhuber.github.io/ApiLogicServer/Logic-Why/) consists of rules **and** conventional Python code.  Explore it like this:

1. Open **Explorer > logic/declare_logic.py**:
   * Observe the 5 rules highlighted in the diagram below.  These are built with code completion.
2. Set a breakpoint as shown
   * This event illustrates that logic is mainly _rules,_ extensible with standard _Python code_
3. Using swagger, re-execute the `add_order` endpoint
4. When you hit the breakpoint, expand `row` VARIABLES list (top left)

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/tutorial/debug-logic.png?raw=true"></figure>

Internally, rules execute by listening to SQLAlchemy `before_flush` events, as [described here](https://valhuber.github.io/ApiLogicServer/Logic-Operation/#how-usage-and-operation-overview).

> This rule architecture ensures that rules are always re-used across all client applications and integrations.  This avoids common "fat client" approaches that embed logic in user interface controllers, which leads to replication and inconsistency.

&nbsp;&nbsp;

---

## Test

You can test using standard api and ui test tools.  We recommend exploring the [Behave framework](https://valhuber.github.io/ApiLogicServer/Behave/).  This can be used as part of an overall agile approach as described in the [Logic Tutorial](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/).

TL;DR - features and test scripts are predefined in the sample; to run them (with the server running):

1. Run Launch Configuration `Run Behave Logic` 
2. Run Launch Configuration ``Behave Logic Report`` 
3. Open `test/api_logic_server_behave/reports/Behave Logic Report.md`

&nbsp;&nbsp;

   > The sample Scenarios below were chosen to illustrate the basic patterns of using rules. Open the disclosure box ("Tests - and their logic...") to see the implementation and notes.   

For more information, see [Testing with Behave](https://valhuber.github.io/ApiLogicServer/Behave/).

&nbsp;&nbsp;

---

## Wrap up
Let's recap what you've seen:

* **ApiLogicProject Creation and Execution** - a database API and an Admin App - created automatically from a database, in moments instead of weeks or months


* **Customizable** - the UI, API and Logic - using Visual Studio code, for both editing and debugging


### Next Steps

Explore the [Logic Tutorial](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/).


### Docker cleanup
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. It will look something like `vsc-ApiLogicProject...`.

&nbsp;&nbsp;&nbsp;