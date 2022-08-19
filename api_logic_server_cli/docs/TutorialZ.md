After completing the `ApiLogicServer create` step, you can view the ```readme``` in the created API Logic Project.  The `readme` links to this sample tutorial, created from [this database.](https://valhuber.github.io/ApiLogicServer/Sample-Database/).  

In this tutorial, we will explore:

* **create** - creating the Tutorial project, and opening it your IDE

* **run** - we will first run the Admin App and the JSON:API

* **customize** - we will then explore some customizations already done for the API and logic, and how to debug them

This tutorial presumes you are running in an IDE - VS Code or PyCharm.  Projects are pre-configured for VS Code with `.devcontainer` and `launch configurations,` so these instructions are oriented around VS Code.

&nbsp;

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images//creates-and-runs-video.png?raw=true?raw=true)](https://youtu.be/tOojjEAct4M "Using VS Code with the ApiLogicServer container - click for video")

The diagram above summarizes the create / run / customize process.  It's a video - click to view.


&nbsp;&nbsp;

## Key Underlying Concepts
This tutorial illustrates some key concepts:

### _Declarative Models_, not code
Observe that the files for the Admin App and API are models that describe _what, not how_.  This makes it much easier to understand than generating large amounts of code.

### Preserve Customizations
The system is designed to enable `rebuild`, so you can iterate the data model - _without losing your customization._  In general, such customizations are kept in separate files than the model files.  So, model files can be rebuilt without affecting customzation files.

&nbsp;

## Create and establish Python Environment

Please  see [Quick Start > Express Install](https://valhuber.github.io/ApiLogicServer/IDE-Execute/), which explains how to:

1. Install API Logic Server
2. Create the sample Tutorial API Logic Server Project
3. Open it in your IDE
4. Prepare the projects' Python environment


&nbsp;

## Run

The prior step established your Python enviroment, so your project is ready to run.  We are now ready to explore the Admin App and the API.

### Admin App: Multi-Page, Multi-Table, Automatic Joins

To run the Admin App, follow these steps:

1. After completing the Create step, start the server as illustrated below:
      * Use the pre-built Launch Configuration to start the server and
      * Start the browser to see your Admin App
1. Navigate to `Customer`
      * Depending on your screen size, you may need to hit the "hamburger menu" (top left) to see the left menu
2. Click the Customer row  to see Customer Details
3. Observe the `Placed Order List` tab at the bottom
4. Click the first Order row
5. Observe the `Order Detail List` tab at the bottom
6. Observe the elements shown in the diagram

      * Multi-Page - 2 pages for each table (list, with search, and display)
      * Multi-Table - database relationships (typically from foreign keys) used to build master/detail pages
      * Automatic Joins - the Order Detail table contains `ProductId`, but the system has joined in the `Product Name`.  You can edit the `admin.yaml` file to control such behavior.

7. Close the app (browser), but __leave the server running__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/run-admin-app.png?raw=true"></figure>

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

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/swagger.png?raw=true"></figure>
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

> Since they automate all the re-use and dependency management, rules are [40X more concise](https://github.com/valhuber/LogicBank/wiki/by-code) than code.  Like a spreadsheet, rules __watch__ for changes, __react__ by automatically executing relevant rules, which can __chain__ to activate other rules; you can [visualize the process here](https://valhuber.github.io/ApiLogicServer/Logic-Operation/#watch-react-chain).

[Logic](https://valhuber.github.io/ApiLogicServer/Logic-Why/) consists of rules **and** conventional Python code.  Explore it like this:

1. Open **Explorer > logic/declare_logic.py**:
   * Observe the 5 rules highlighted in the diagram below.  These are built with code completion.
2. Set a breakpoint as shown
   * This event illustrates that logic is mainly _rules,_ extensible with standard _Python code_
3. Using swagger, re-execute the `add_order` endpoint
4. When you hit the breakpoint, expand `row` VARIABLES list (top left)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/declare-logic.png"></figure>

Internally, rules execute by listening to SQLAlchemy `before_flush` events, as [described here](https://valhuber.github.io/ApiLogicServer/Logic-Operation/#how-usage-and-operation-overview).

> This rule architecture ensures that rules are always re-used across all client applications and integrations.  This avoids common "fat client" approaches that embed logic in user interface controllers, which leads to replication and inconsistency.


&nbsp;&nbsp;

## Test

You can test using standard api and ui test tools.  We recommend exploring the [Behave framework](https://valhuber.github.io/ApiLogicServer/Behave/).  This can be used as part of an overall agile approach as described in the [Logic Tutorial](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/).

TL;DR - features and test scripts are predefined in the sample; to run them (with the server running):

1. Run Launch Configuration `Run Behave Logic` 
2. Run Launch Configuration ``Behave Logic Report`` 
3. Open `test/api_logic_server_behave/reports/Behave Logic Report.md`

&nbsp;&nbsp;

   > The sample Scenarios below were chosen to illustrate the basic patterns of using rules. Open the disclosure box ("Tests - and their logic...") to see the implementation and notes.   

For more information, see [Testing with Behave](https://valhuber.github.io/ApiLogicServer/Behave/).

&nbsp;&nbsp;&nbsp;

## Wrap up
Let's recap what you've seen:

* **ApiLogicProject Creation and Execution** - a database API and an Admin App - created automatically from a database, in moments instead of weeks or months


* **Customizable** - the UI, API and Logic - using Visual Studio code, for both editing and debugging


### Next Steps

Explore the [Logic Tutorial](https://valhuber.github.io/ApiLogicServer/Logic-Tutorial/).


### Docker cleanup
VS Code leaves the container and image definitions intact, so you can quickly resume your session.  You may wish to delete this. it will look something like `vsc-ApiLogicProject...`.

&nbsp;&nbsp;&nbsp;