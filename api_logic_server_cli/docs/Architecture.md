
# Architectural Overview

### Docker Containers
As shown below, there are typically 2-3 "machines" in operation:
* Your **local host** (in grey), where the Customizable Project files (`ApiLogicProject`) are stored, 
and your Dev Tools (IDE etc) operate


* The ApiLogicServer Docker **container** (blue), which contains:
  * The **ApiLogicServer**, with CLI (Command Language Interface) commands:
     * **`create`** to create projects on your local host
     * **`run`** to execute projects, utilizing the various runtimes (Flask, SQLAlchemy, SAFRS API, Logic, Flask App Builder)
  * A **Python** environment to support execution, and development using your IDE
  * Neither API nor logic execution creates / uses additional files or database data; your database access is via standard SQLAlchemy models
     * The exception to this is Flask App Builder, which creates additional database tables for security authorization


* The **database** (purple) can run as a separate Docker container, in your local host, or (for the demo) within the ApiLogicServer docker container


<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/docker-arch-create-run.png"></figure>


### Pip Install - ApiLogicServer in local Python environment

<details>

  <summary>Alternative option: pip install</summary>

You can also run ApiLogicServer without Docker.  The familiar `pip install ApiLogicServer` creates the ApiLogicServer in your `venv` instead of the Docker container.  The contents are identical - the ApiLogicServer `create` and `run` components.

We recommend, however, that you take a good look at Docker:
* It avoids a sometimes-tricky Python install
* It isolates your projects into containers
* It is quite likely the eventual deployment architecture, so you're already in step with that
</details>

### ApiLogicServer Key Components


| Component                                                                              | Provides                                                                                                              |
|:---------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| [SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html)                      | Python-friendly ORM (analogous to Hiberate, JPA)                                                                      |
| [Logic Bank](../Logic:-Rules-plus-Python) | Multi-Table Derivation and Constraint Rules<br>Python Events (e.g., send mail, message)<br>Extensible with Python<br> |
| [SAFRS](https://github.com/thomaxxl/safrs/wiki)                                        | JSON:API and swagger, based on SQLAlchemy                                                                             |
| [SAFRS-React-Admin](https://github.com/thomaxxl/safrs-react-admin)                     | Executable React Admin UI, using SAFRS                                                                                |


### Project Structure
When you have created your project, you will find the following project directory in `~/dev/servers` on your (grey) local host   (here opened in VS Code):
<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png"></figure>

Your docker container (blue) files include Python, Python libraries, and API Logic Server.  The Python project above utilizes IDE `remote-container` support (visible at the lower left in the preceding diagram), which utilizes the docker container (not local host) version of Python.

Your docker container looks like this:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/docker-files.png"></figure>

#### IDE Friendly

The project structure above can be loaded into any IDE for code editing, deubgging, etc.  For more information on using IDEs, [see here](https://github.com/valhuber/ApiLogicServer/wiki#using-your-ide).

#### Tool-friendly - file-based

All project elements are files - no database or binary objects.  So, you can store objects in source control systems like git, diff/merge them, etc.



# Internals - How It Works

The ApiLogicServer CLI `create` (or `run`) command creates the project structure shown below - for more information, [see here](../Internals).

* Execution begins in `api_logic_server_run.py`.
* Your customizations are done to the files noted in the callouts below.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png"></figure>

### API Execution: `api_logic_server_run.py`

`api_logic_server_run.py` (a file created in your ApiLogicProject) sets up a Flask app, the database, logic and api:

1. **Database Setup:** It imports`api/expose_api_models` which imports `database/models.py`, which then imports `database/customize_models.py` for your model extensions.  `api_logic_server_run.py` then sets up flask, and opens the  database with `db = safrs.DB`


2. **Logic Setup:** It then calls `LogicBank.activate`, passing `declare_logic` which loads your declared rules into Logic Bank.


3. **API Setup:** It next invokes `api/expose_api_models`.  This calls safrs to create the end points and the swagger information, based on the created `database/models.py` (the models used by the SQLAlchemy ORM).   It finally calls `api/customize.py` where you can add your own services.  The sample includes a trivial Hello World, as well as `add_order`.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/logic/logic-exec-arch.png"></figure>

### Logic Execution
SAFRS API listens for API calls, e.g., from the Admin App.  When updates are issued:

4. **Invokes SQLAlchemy updates:** SAFRS calls SQLAlchemy, passing a set of rows comprising a database transaction


5. **`before_flush`:** SQLAlchemy provides a `before_flush` event, where all the update rows are assembled and passed to `Logic Bank`  (no relation to retail!).


6. **Logic Execution:** Logic Bank reviews the rows, and based on what has change, prunes rules for unchanged data, and executes / optimizes relevant logic in an appropriate order.  

#### Declarative Logic is critical

Logic addresses multi-table derivations, constraints, and actions such as sending messages or emails.  These can constitute nearly half the effort in transactional systems.


### Admin App Execution: `ui/admin/admin.yaml`
[http://localhost:5656/](http://localhost:5656/) redirects to `ui/admin/index.html` which loads the react-admin single-page app into your browser.

It then loads your `ui/admin/admin.yaml`, and responds to the various clicks by invoking the API (and hence the update logic), or the swagger at [http://localhost:5656/api](http://localhost:5656/api).


## Key Observations: Extensible Declarative Automation

While the most striking element of ApiLogicServer is automation - a running UI and API from a database - there are some important aspects, described below.

### _Customizable, Declarative_ Models

Observe that the key files for defining API, UI and Logic are not procedural code.  They are _declarative:_ specifications of _what_ you want to happen, not _how_ it's implemented:

* Logic looks more like a specification than code

* UI looks like a list of Objects and Attributes to display

* API looks like a list of Objects

This is important because they are orders of magnitude shorter, and therefore far easier to understand, and to customize.

For example, consider the UI, defined by `ui/admin/admin.yaml`.  This is in lieu of hundreds of lines of very complex HTML and JavaScript.

### Extensible

ApiLogicServer makes provisions for you to add standard Python code for aspects of your project that are automated - custom end points, extensions to the data model, logic (rules _plus Python_).  

And, of course, the API means you are unblocked for creating custom UIs and integrations.

### Includes Logic

As noted above, multi-table constraints and derivations can constitute nearly half the effort in transactional systems.

Unlike most systems that address such logic with "your code goes here", ApiLogicServer provides _**declarative** spreadsheet-like rules,_ extensible with Python, as [described here](../Logic:-Rules-plus-Python).  Rules are 40X more concise than code.  

Rule execution is via a _transaction logic_ engine, a complementary technology to traditional RETE engines.  The [transaction logic engine](https://github.com/valhuber/LogicBank/wiki/Rules-Engines) is specifically designed to optimize integrity and performance for transactional logic, which is not possible in RETE engines. See [here](https://github.com/valhuber/LogicBank/wiki/Logic-Walkthrough) for more information on their operation.

## Technology Adoption Considerations

### Standards-based

Development and runtime architectures are what programmers expect:
* As noted above, the [Key Project Components](#key-project-components) are standard Python packages for APIs, data access.
* Projects developed in standard IDEs, and deployed in standard containers.

### Near-Zero Learning Curve - no frameworks, etc

ApiLogicServer has a near-zero learning curve.  You do not need to know Python, SQLAlchemy, React, or JSONapi_logic_serverPIs to get started.  You have a running project in moments, customizable without requiring deep understanding of any of these frameworks.  Making extensions, of course, begins to require more technical background.

#### Allow a few days for learning logic

Logic represents the starkest different between procedural code and declarative rules.  It requires a few days to get the hang of it.  We recommend you [explore this documentation](https://github.com/valhuber/LogicBank#next-steps).

### Business Agility

ApiLogicServer automation creates a running project nearly instantly, but it also is designed to help you adapt to business changes more rapidly:

* [Rebuild](https://github.com/valhuber/ApiLogicServer/wiki#rebuilding) support to update existing projects from database or data model changes
* Logic provides automatic [reordering and reoptimization](../Logic:-Rules-plus-Python#ordering-automatic-for-derivations-with-control-for-actions-and-constraints) as logic is altered

### Technology Agility - an Application Virtual Machine

Models are, somewhat by their very nature, rather technology independent.  Instead of React, the UI specification could be implemented on Angular.  Instead of interpreted, the logic could be code-generated onto any language.  And so forth.

You can think of the [Key Project Components](#key-project-components) as an Application Virtual Machine that executes ApiLogicProjects.  As new underlying technology becomes available, new AVMs could be developed that migrate the declarative elements of your UI, API and Logic - ***without coding change***.  Because, they are models, not code.

   > This provides an unprecedented preservation of your application investment over underlying technology change. 

### Automation Reduces Risk

Automation not only gets results fast and simplifies adapting to change, it also reduces risk.

#### Coding Risk

The most troublesome bugs are silent failures - no stacktrace, but the wrong answer.

Automation address this by designing out whole classes of error:

* the UI and API just work
* logic is [automatically re-used](../Logic:-Rules-plus-Python#spreadsheet-like-automatic-reuse) over all Use Cases

#### Architectural Risk

Technology complexity makes it get hard to get projects that even work, much less work right.  Projects commonly suffer from a wide variety of architectural flaws:

* business logic is not shared, but repeated in each UI controller... and each integration
* pagination may not be provided for all screens

And so forth.  These cause project failures, far too often.

But automation can help - since your declarative models only stipulate _what_, the _system_ bears the responsibility for the _how -- and getting it right_.  Each of the architectural items above are automated by the system.

#### Requirements Risk

Requirements risk can represent an even greater challenge.  The reality that users may only realize the real requirements when they actually use running screens with real data.  The problem, of course, is that these are often available after considerable time and effort.

That's why _working software **now**_ is so important - users get screens right away.  These can identify data model errors (_"hey... customers have more than one address"_) or business logic requirements (_"hey.... we need to check the credit limit"_).


