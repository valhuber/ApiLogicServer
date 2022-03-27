# Behave Creates Executable Test Suite, Documentation

You can optionally use the Behave test framework to:

1. **Create and Run an Executable Test Suite:** in your IDE, create test definitions (similar to what is shown above), and Python code to execute tests.  You can then execute the tests with 1 command.

2. **Requirements and Test Documentation:** as shown above, Test Suite Exeuction creates a wiki report that documents your requirements, and the tests (**Scenarios**) that confirm their proper operation

3. **Logic Documentation:** the report integrates your logic, including a logic report showing your logic (rules and Python), and a Logic Log that shows exactly how the rules executed.  Logic Doc can further contribute to Agile Collaboration.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/behave-summary.png?raw=true"></figure>

# Appendices

## Behave
Behave...

## TDD
TDD...

# Process
This project illustrates how [API Logic Server](https://github.com/valhuber/ApiLogicServer/blob/main/README.md) Extensible Automation, coupled with an Agile (TDD) Process, can dramatically improve Time to Market and Reduce Risk:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/introduction.png?raw=true"></figure>
  
1. **Instant App:** API Logic Server creates an Admin App (and underlying API) with a single command.

1. **Customer Collaboration:** the app (Working Software, _Now_) drives collaboration, resulting in *Features* (Stories), *Scenarios* (tests), and *Design Specifications* that define how data is computed, validated, and processed (e.g., issues email or messages, auditing, etc.).

1. **Iteration:** the Design Specifications often translate directly into ***Executable* Rules,** automated in API Logic Server.  These can be easily altered as further collaboration uncovers clarifications (no archaeology).

2. **Transparency:** the [**TDD** (Test Driven Development) Report](#tdd-report) documents the functionality of the system as Features (Stories) and Scenarios (tests) that confirm its operation.  The report includes the underlying Rules, extending transparency to the implementation level.

&nbsp;&nbsp;

>  **Key Takeaway:** automation drives Time to Market, and provides working software rapidly; it also drives TDD collaboration to define systems that meet actual needs, reducing requirements risk.

&nbsp;&nbsp;

# Sample Project

This is the sample project from API Logic Server, based on the Northwind database (sqlite database located in the `database` folder - no installation required):

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/nw.png"></figure>

&nbsp;&nbsp;

## Verify Installation

You can confirm its working by installing and running [as described here](https://github.com/valhuber/TDD/wiki/Setup).

&nbsp;&nbsp;

# Process Overview

The created project provides the User Interface and API described below, and implements the transactional logic described in the [TDD Report](#tdd-report).  It was created, customized and tested as described in the subsections below.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/TDD-process.png?raw=true"></figure>

&nbsp;&nbsp;

## 1. Create Api Logic Project

API Logic Server is used once you have a preliminary database design.  Use your existing procedures for database design.  Include at least minimal test data.

Then (presuming API Logic Server [is installed](https://github.com/valhuber/ApiLogicServer/blob/main/README.md)), create the project with this command, using `venv` based installs:

```
ApiLogicServer create  --db_url= --project_name=TDD
```

or, like this, using docker-based installs:
```
ApiLogicServer create --db_url= --project_name=/localhost/TDD
```

&nbsp;&nbsp;

#### 1a. Creates **Admin App**

The Agile objective of collaboration is typically best-served with _running_ screens.  The problem is, it takes quite a long time to create the API and screens to reach this point.  And this work can be wasted if there were misunderstandings.

Ideally, User Interface creation would be automatic.

So, the API Logic Server `create` command above builds first-cut screens, automatically from the data model.  

The app shown below [(more detail here)](https://github.com/valhuber/ApiLogicServer#admin-app-multi-page-multi-table-automatic-joins) is suitable for initial _business user collaboration_ (further discussed below), and basic _back office_ data maintenance.

You can [customize it](https://github.com/valhuber/ApiLogicServer#admin-app-customization) by editing a simple `yaml`file (e.g, field captions, ordering etc.)

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/ui-admin/run-admin-app.png?raw=true"></figure>

&nbsp;&nbsp;

>  **Key Takeaway:** Admin App Automation enables collaboration, instantly.

&nbsp;&nbsp;

#### 1b. Also creates **API**

It is not difficult to create a single endpoint API.  The problem is that it's quite a bit more work to create an endpoint for each table, with support for related data, pagination, filtering and sorting.

Ideally, API creation would be automatic.

So, the API Logic Server `create` command above builds such an API instantly, suitable for _application integration_, and creating _custom User Interfaces_.  The API enforces the business logic described below.

The [created project is customizable,](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#customize-and-debug) using a standard IDE.

&nbsp;&nbsp;

>  **Key Takeaway:** automatic API creation, with support for related data, pagination, filtering and sorting.

&nbsp;&nbsp;

## 2. Collaborate using **Admin App**

As noted above, running screens are an excellent way to engage business user collaboration and ensure the system meets actual user needs.  Such collaboration typically leads in two important directions, as described below.

&nbsp;&nbsp;

#### 2a. Iterate Data Model

You may discover that the data model is incorrect (_"Wait!  Customers have multiple addresses!!"_).  

In a conventional system, this would mean revising the API and App.  However, since these are created instantly through automation, such iterations are trivial.  Just rebuild.

&nbsp;&nbsp;

#### 2b. Define Behave Scenarios

User Interfaces also spark insight about the Features ("Place Order") and Scenarios ("Check Credit"): _"When the customer places an order, we need to reject it if it exceeds the credit limit"._  Capture these as described below.

TDD is designed for business user collaboration by making Features and Scenarios transparent.  So, the start of Behave is to define one or more `.feature` files.

For example, see the `place_order.feature`, as tested by the `Bad Order: Custom Service` Scenario, below.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/scenario.png?raw=true"></figure>

For more on TDD, [see here](https://github.com/valhuber/TDD/wiki/Stories-And-Behaviors).

&nbsp;&nbsp;

##### Add Custom Service

While the automatically-created API is a great start, you may uncover a need for a custom service.  This is easy to add - it's only about 10 lines of Python (`api/customize_api.py`), since the logic (discussed below) is enforced in the underlying data access.  For details, [see here](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-customization).

&nbsp;&nbsp;

#### 2c. Logic Specification

We now choose a scenario (e.g, `Bad Order`), and engage business users for a clear understanding of _check credit_.  This follows a familiar step-wise definition of terms, which we capture in text as shown below.

Note this "cocktail napkin spec" is short, yet clear.  That's because instead of diving unto unecessary technical detail of _how_ (such as pseudocode), it focuses on ***what***.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/logic-spec.png?raw=true"></figure>
  

&nbsp;&nbsp;

## 3a. Declare Logic (from spec)

Business Logic is the heart of the system, enforcing our business policies.  These consist of multi-table constraints and derivations, and actions such as sending email and messages.  A core TDD objective is to define and test such behavior.

It's generally accepted that such domain-specific logic _must_ require domain-specific code.  The problem is that this is:
* **slow** (it's often nearly half the system)
* **opaque** to business users
* **painful to maintain** - it's no secret that developers hate maintenance, since it's less coding than _"archaeology":_ read the existing code to understand where to insert the new logic

Ideally, our _logic specification is executable._  

So, API Logic Server provides Logic Automation, where logic is implemented as:

* [Spreadsheet-like ***rules***](https://github.com/valhuber/LogicBank/wiki/Examples) for multi-table derivations and constraints, and

* Python, to implement logic not addressed in rules such as sending email or messages

So, [instead of several hundred lines of code](https://github.com/valhuber/LogicBank/wiki/by-code), we declared 5 rules [(more details here)](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#logic).  

Rules are entered in Python, with code completion.  5 key rules are shown below.  Oserve how they exactly correspond to our specification, and are executable by the API Logic Server rules engine:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/declare-logic.png?raw=true"></figure>

Unlike manual code, logic is ***declarative:***
* **automatically reused** - it is enforced as part of the API, so automatically shared across *all* screens and services.
* **automatically ordered** - maintenance is simply altering the rules; the system computes their execution order by automatically discovering their dependencies.  No more archaeology.
* **transparent** - business users can read the spreadsheet-like rules.  We'll exploit this in the TDD Report, described below.


&nbsp;&nbsp;

>  **Key Takeaway:** spreadsheet-like rules can dramatically reduce the effort for backend logic, and make it transparent

&nbsp;&nbsp;

>  **Key Takeaway:** keep your Logic Specification high level (_what_ not _how_ -- think spreadsheet), and your specification will often map directly to executable rules. 

&nbsp;&nbsp;

## 3b. Code/Run TDD Scenarios

Implement the actual scenarios (tests) in Python (`place_order.py`), using annotations (`@when`) to match scenarios and implementations.  In this project, the implementation is basically calling APIs to get old data, run transactions, and check results.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/behave/TDD-ide.png?raw=true"></figure>

Execute the tests using the pre-supplied Launch Configurations (shown at the bottom):

1. Run Launch Configuration `API Logic Server` 
1. Run Launch Configuration `Debug Behave Logic` 

The rules fire as transactions are run, and produce files later used in Report Behave Logic (described below): 
1. `test/api_logic_server_behave/behave.log` - summarizes test success / failure
2. `api_logic_server_behave/scenario_logic_logs/Bad_Order_Custom_Service.log` - [Logic Log output](https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python#debugging).
   * The code on line 121 signals the name of Logic Log
   * Note the Logic Log actually consists of 2 sections:
      * The first shows each rule firing, including complete old/new row values, with indentation for `multi-table chaining`
      * The "Rules Fired" summarizes which rules actually fired, representing a _confirmation of our Logic Specification_

>  You can use the debugger to stop in a test and verify results

&nbsp;&nbsp;

## 4. **Create TDD/Logic Report**

This is pretty interesting: a record of all our Features and Scenarios, including transparent underlying logic.  The problem is that it's buried in some text files inside our project.

Ideally, publishing this in a transparent manner (e.g., a wiki accessible via the Browser) would be a great asset to the team.

So, this project provides `report_behave_logic.py` to create a TDD Report - _including logic_ - as a wiki file.

To run it, use Launch Configuration `Report Behave Logic`:

1. Reads your current `readme.md` file (text like you are reading now), and
2. Appends the [TDD Report:](#tdd-report) by processing the files created in step 3c
   1. Reading the `behave.log`, and
   2. Injecting the `scenario_logic_logs` files
3. Creates the output report as a wiki file named `report_behave_logic.md`

&nbsp;&nbsp;

>  **Key Takeaway:** TDD makes *requirements and tests* transparent; rules make your *logic* transparent; combine them both into the [**TDD Report.**](#tdd-report)

&nbsp;
&nbsp;
