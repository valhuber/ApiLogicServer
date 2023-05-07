# Tutorial

<details markdown>

<br>

<summary>Welcome to this Tutorial</summary>

Use this Tutorial for a quick tour of API Logic Server 

- **Instant** project creation from a database
- **Fully customizable,** using both standard code (Flask/SQLAlchemy) in *your* IDE, and
- **Logic** -- multi-table derivation and constraint logic using unique spreadsheet-like rules

This contains several projects.  These projects use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/) (customers, orders, products).


| Project | What it is | Use it to... |
|:---- |:------|:-----------|
| 1. Instant_Creation | Northwind Database - Uncustomized | Explore **automated project creation** from Database |
| 2. Customized | Northwind Database - Customized | Explore **customizing** with code |
| 3. Logic | Northwind Database - Customized, with Logic | Explore **customizing** with code, and rule-based logic |
| Next Steps | Create other sample databases | More examples - initial project creation from Database |

&nbsp; 

> If you are running via `pip install` (not Docker or Codespaces), you need to [setup your virtual environment](https://apilogicserver.github.io/Docs/Project-Env/#shared-venv).

</details>

&nbsp;

<details markdown>

<br>

<summary>0. App_Fiddle: Manually Coded -- Learn Flask / SQLAlchemy - Fully customizable, but slow</summary>

This first app (_0. App_Fiddle_) illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.  Let's run/test it, then explore the code.

To run, use the Run Configuration, and test with `cURL`.  

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Show me how </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see *0. App Fiddle), and the green button to start the server

2. Copy the `cURL` text, and paste it into the `bash`/`zsh` window

3. When you have reviewed the result ([here's the readme](./1.%20App_Fiddle/readme.md)), **stop** the server

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app-tutorial.png?raw=true)


</details>


&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;--> Fully Customizable, but Faster Would Be Better</summary>

&nbsp;

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project **does not provide:**

<img align="right" width="150" height="150" src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/vscode/app-fiddle/horse-feathers.jpg?raw=true" alt="Horse Feathers">

* an API endpoint for each table

    * We saw above it's straightforward to provide a *single endpoint.*  It's quite another matter -- ***weeks to months*** -- to provide endpoints for **all** the tables, with pagination, filtering, and related data access.  That's a horse of an entirely different feather.<br><br>

* a User Interface

* any security, or business logic (multi-table derivations and constraints).

Instead of frameworks, we might consider a Low Code approach.  Low Code tools provide excellent custom user interfaces.  However, these often require extensive screen painting, and typically require a proprietary IDE.

And neither frameworks nor Low-Code address multi-table derivation and constraint logic. This is typically nearly half the effort.

The next section introduces an approach that is as flexible as a framework, but faster than Low Code for APIs and Admin Apps.

</details>

</details>

&nbsp;

<details markdown>

<summary>1. Instant Creation -- Flexible as a Framework, Faster than Low Code</summary>

<br>

The *1. Instant_Creation* app illustrates an alternative, creating an entire project by reading your schema.  This automated approach is:

* **Instant:** faster than Low Code screen painting, with instant APIs and Admin User Interfaces:

  * **Admin UI:** multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show.  No HTML or JavaScript required.  Ready for Agile collaboration.

      * Custom UIs can be built using your tool of choice (React, Angular, etc), using the API<br><br>

  * **API:** an endpoint for each table, with filtering, sorting, pagination and related data access.  Swagger is automatic.  Ready for custom app dev.

* **Fully Customizable:** with **standard dev tools**.  Use *your IDE*, Python, and Flask/SQLAlchemy to create new services.  We'll see several examples below. 

* **Open Source:** install with pip or docker.

To execute (see *Show me how*, below, for details): **start the server** with **Run and Debug >> *1. Instant Creation***, and then start the Browser at localhost:5656 **(url in the console log)**

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Show me how </summary>

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/2-apilogicproject-tutorial.png?raw=true)

&nbsp;

</details>

&nbsp;

This application was *not coded* - **it was created** using the API Logic Server CLI (Command Language Interface), with 1 command (not necessary to do now - it's already been done):

```bash
cd tutorial
ApiLogicServer create --db_url=sqlite:///sample_db.sqlite --project_name=nw
```

If you *do* want to execute: **stop** the server, restart with **Run and Debug >> nw**, and then start the Browser at localhost:5656 (url in the console log).

&nbsp;

> Key Takeway: you will achieve this level automation for your projects: provide a database, get an instant API and Admin App.  Ready for agile collaboration, custom app dev.  Then, customize in your IDE. 

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;What is API Logic Server </summary>

&nbsp;

**What is Installed**

API Logic server installs with `pip`, in a docker container, or in codespaces.  As shown below, it consists of a:

* **CLI:** the `ApiLogicServer create` command you saw above
* **Runtime Packages:** for API, UI and Logic execution<br>


![](https://apilogicserver.github.io/Docs/images/Architecture-What-Is.png)

&nbsp;

**Development Architecture**

It operates as shown below:

* A) Create your database as usual

* B) Use the CLI to generate an executable project

  * The system reads your database to create an executable API Logic Project

* C) Customize and debug it in VSCode, PyCharm, etc.


![](https://apilogicserver.github.io/Docs/images/creates-and-runs.png)

&nbsp;

**Standard, Scalable Modern Architecture**

* A modern 3-tiered architecture, accessed by **APIs**
* Logic is **automatically reused**, factored out of web apps and custom services
* **Containerized** for scalable cloud deployment - the project includes a dockerfile to containerize it to DockerHub.


![API Logic Server Intro](https://apilogicserver.github.io/Docs/images/Architecture.png)

</details>


&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;--> Instant, But Customization Required</summary>

&nbsp;

An instant Admin App and API are a great start, but there are some significant short-comings:

* **Limited endpoints -** we may require additional endpoints beyond those automatically created

* **No security -** no login authentication

* **No logic -** multi-table derivations and constraints for save logic

    * For example, open **Customer** (left nav menu), **click `ALFKI`**, and **EDIT > DELETE the first Order**.  Re-click Customer from the left nav menu - it should have reduced the customer's balance from 2102, but it's unchanged.   That's because there is *no logic...*

    * Backend update logic can be as much as half the effort, so we really haven't achieved "Low Code" until this are addressed.

Let's see how these are addressed, in the next sections.

</details>

</details>

&nbsp;

<details markdown>

<summary>2. Customized -- Admin App, New Endpoint... Standard Dev Tools</summary>

<br>

Customizations are addressed using your IDE, using **Standard use Flask and SQLAlchemy**, exactly as you normally do.

Customizations are illustrated in the project [`2. Customized`](2.%20Customized/).  To see the effect of the changes, run the app like this:

1. **Stop the server** using the red "stop" button.
2. **Restart the server** with the same procedure as Step 1, above, but choose Run Configuration ***2. Customized***.<br>

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Remind me how</summary>

&nbsp;

1. Restart the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **3. API Logic Project: Logic**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656, using the **url shown in the console log**

![](https://apilogicserver.github.io/Docs/images/tutorial/2-apilogicproject-tutorial.png)

</details>

&nbsp;

This project is the customized version of _1. Instant_Creation_, above.  The table below lists some of the key customizations you can explore.

&nbsp;

<p align="center">
  <h2 align="center">Explore Key Customizations</h2>
</p>
<p align="center">
  Explore customizations in project: <i>2. Customized</i><br>
  Click Explore Code to see the code.<br>
  <b>TL;DR - scan code marked by <--</b>
</p>

| Customization Area           | Try It                                                                                                                                                                                            | Click to Explore Code                                                                                  | Notes                |
|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------|:---------------------|
| **New API endpoint <--**         | Use Swagger for endpoint: *CategoriesEndPoint/get_cats* | [```api/customize_api.py```](2.%20Customized/api/customize_api.py)                 | Standard Flask/SQLAlchemy  |
| **Admin App <--**  | Observe **help text** describes features    |   [```ui/admin/admin.yaml```](2.%20Customized/ui/admin/admin.yaml)                  | Not complex JS, HTML                     |

&nbsp;

</details>

&nbsp;

<details markdown>

<summary>3. Logic -- Unique Spreadsheet-like Rules (40X more concise), Plus Python</summary>

<br>

In addition to standard Flask/SQLAlchemy use, you can declare rules for multi-table derivations and constraints.  Declare rules using Python as a DSL, leveraging IDE support for type-checking, code completion, logging and debugging.

Rules are extensible using standard Python.  This enables you to address non-database oriented logic such as sending mail or messages.<br><br>

**Rules operate like a spreadsheet**

Rules plug into SQLAlchemy events, and execute as follows:

| Logic Phase | Why It Matters |
|:-----------------------------|:---------------------|
| **Watch** for changes at the attribute level | Performance - Automatic Attribute-level Pruning |
| **React** if referenced data is changed | Ensures Reuse - Invocation is automatic<br>Derivations are optimized (e.g. *adjustment updates* - not aggregate queries) |
| **Chain** to other referencing data | Simplifies Maintenance - ordering is automatic |

&nbsp;

Customizations are illustrated in the project [`3. Logic`](3.%20Logic/).  To see the effect of the changes, run the app like this:

1. **Stop the server** using the red "stop" button.
2. **Restart the server** with the same procedure as Step 2, above, but choose Run Configuration ***3. Logic***.<br>

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Remind me how</summary>

&nbsp;

1. Restart the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **3. API Logic Project: Logic**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656, using the **url shown in the console log**

![](https://apilogicserver.github.io/Docs/images/tutorial/2-apilogicproject-tutorial.png)

</details>

&nbsp;

This project further customizes _2. Customized_, above.  The table below lists some of the key customizations you can explore.

&nbsp;

<p align="center">
  <h2 align="center">Explore Key Customizations</h2>
</p>
<p align="center">
  Explore customizations in project: <i>3. ApiLogicProject_Logic</i><br>
  Click Explore Code to see the code.<br>
  <b>TL;DR - scan code marked by <--</b>
</p>

| Customization Area           | Try It                                                                                                                                                                                            | Click to Explore Code                                                                                  | Notes                |
|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------|:---------------------|
| **New API endpoint <--**         | Use Swagger for endpoint: *CategoriesEndPoint/get_cats*<br><br>See [docs](https://apilogicserver.github.io/Docs/Security-Swagger/) - authenticate as **u1**  | [```api/customize_api.py```](3.%20Logic/api/customize_api.py)                 | Standard Flask/SQLAlchemy  |
| **Multi-table Update Logic <--** | Delete Order now adjusts the customer balance                                                                                                                                                    | [```logic/declare_logic.py```](3.%20Logic/logic/declare_logic.py)             |  Spreadsheet-like rules                    |                                                                
| **Admin App <--**  | Observe **help text** describes features                                                                                                                                                 | [```ui/admin/admin.yaml```](3.%20Logic/ui/admin/admin.yaml)                  | Not complex JS, HTML                     |
| **Login Authentication**     | Click Category - observe you need to **login** now (user u1, password p)                                                                                                                                  | [```config.py```](3.%20Logic/config.py)                                       | See SECURITY_ENABLED |
| **Role-Based Authorization** | Observe categories has **fewer rows**                                                                                                                                                                         | [```security/declare_security.py```](3.%20Logic/security/declare_security.py) |                      |

&nbsp;

Use the [```Detailed Tutorial```](3.%20Logic/Tutorial.md) to further explore this app.  

</details>

&nbsp;

<details markdown>

&nbsp;

<summary>Key Takeaways: Instant App/API, Fully Flexible, Unique Declarative Rules</summary>

You have seen the **fastest and simplest** way to create **modern, scalable API-based database systems:**

1. Use the `ApiLogicServer create` command to create a Flask/SQLAlchemy project from your database. Zero learning curve. Projects are **instantly executable**, providing:

    * **an Admin App:** multi-page, multi-table apps -- ready for business user agile collaboration
    * **an API:** end points for each table, with filtering, sorting, pagination and related data access -- ready for custom app dev<br><br>

2. **Open Flexibility:** leverage standards for development and deployment:

    * Dev: customize and debug with **<span style="background-color:Azure;">standard dev tools</span>**.  Use *your IDE (e.g. <span style="background-color:Azure;">VSCode, PyCharm</span>)*, <span style="background-color:Azure;">Python</span>, and Flask/SQLAlchemy to create new services.  Manage projects with <span style="background-color:Azure;">GitHub</span>.

    * Deploy: **containerize** your project - deploy on-premise or to the cloud <span style="background-color:Azure;">(Azure, AWS, etc)</span>.
    
    * *Flexible as a framework, Faster then Low Code for Admin Apps*

3. ***Declare* security and multi-table constraint/validation logic**, using **declarative spreadsheet-like rules**.  Addressing the backend *half* of your system, logic consists of rules, extensible with Python event code.

     * *40X more concise than code - unique to API Logic Server*<br><br>

</details>

&nbsp;
<details markdown>

&nbsp;

<summary>Next Steps: New Projects</summary>

As shown above, it's easy to create projects with a single command.  To help you explore, ApiLogicServer provides several pre-installed sqlite sample databases:

```bash
cd tutorial

ApiLogicServer create --db_url=sqlite:///sample_db.sqlite --project_name=nw

# that's a bit of a mouthful, so abbreviations are provided for pre-included samples
ApiLogicServer create --project_name=nw --db_url=nw-                       # same sample as 2, above
ApiLogicServer create --project_name=chinook --db_url=chinook              # artists and albums
ApiLogicServer create --project_name=classicmodels --db_url=classicmodels  # customers, orders
ApiLogicServer create --project_name=todo --db_url=todo                    # 1 table database

```
Then, **restart** the server as above, using the pre-created Run Configuration for `Execute <new project>`.<br><br>

> Next, try it on your own databases: if you have a database, you can have an API and an Admin app in minutes.

&nbsp;

<details markdown>

<summary> SQLAlchemy url required for your own databases </summary>

&nbsp;

The system provides shorthand notations for the pre-installed sample databases above.  For your own databases, you will need to provide a SQLAlchemy URI for the `db_url` parameter.  These can be tricky - try `ApiLogicServer examples`, or, when all else fails, [try the docs](https://apilogicserver.github.io/Docs/Database-Connectivity/).

</details>

&nbsp;

Click here for the [docs](https://apilogicserver.github.io/Docs/).

</details>

&nbsp;

<details markdown>

<summary> Notes </summary>

&nbsp;

**Project Structure**

This tutorial is actually 3 independent projects.  When you create a project using `ApiLogicServer create --project_name=my_project`, the system will create a free-standing project.  The project will include your container settings, IDE settings etc, so you can just open it your IDE to run and debug.

&nbsp;

**Guided Demo**

Demonstrations of API Logic Server often follow this script, provided as take-away notes.

<details markdown>

<summary> Guided Demo Summary </summary>

&nbsp;

1. Run the automatic **Admin App, and Swagger**<br><br>

2. Explore the Admin App (no html, js): `ui/admin/admin.yaml`<br><br>

3. Explore the API
    * **Automatic API:** `api/expose_api_models.py`
      * `database/models.py` - from schema
    * **Custom Endpoint:** `api/customize_api.py` - see `add_order()`<br><br>

4. Explore `logic/declare_logic.py`
    * **Executable Design** - declarative
    * **Breakpoint here**<br><br>

5. Run **Custom APIs and Logic Execution / Debugging**
    * In swagger: **POST ServicesEndPoint/add_order > Try it out**
    * At the breakpoint, observe the 
        * **Debugger State** -- row attributes, etc
        * **Logic Log** -- line for each rule fire, showing row, with indents for chaining

</details markdown>

&nbsp;

</details markdown>

</details>

&nbsp;


<details markdown>

<summary>Key Technology Concepts </summary>


<p align="center">
  <h2 align="center">Key Technology Concepts</h2>
</p>
<p align="center">
  Select a skill of interest, and<br>Click the link to see sample code
</p>
&nbsp;


| Tech Area | Skill | App_Fiddle Example | APILogicProject Logic Example | Notes   |
|:---- |:------|:-----------|:--------|:--------|
| __Flask__ | Setup | [```flask_basic.py```](0.%20App_Fiddle/flask_basic.py) |  [```api_logic_server_run.py```](3.%20Logic/api_logic_server_run.py) |  |
|  | Events | |  [```ui/admin/admin_loader.py```](3.%20Logic/ui/admin/admin_loader.py) |  |
| __API__ | Create End Point | [```api/end_points.py```](0.%20App_Fiddle/api/end_points.py) | [```api/customize_api.py```](3.%20Logic/api/customize_api.py) |  see `def order():` |
|  | Call endpoint |  | [```test/.../place_order.py```](3.%20Logic/test/api_logic_server_behave/features/steps/place_order.py) | |
| __Config__ | Config | [```config.py```](3.%20Logic/config.py) | | |
|  | Env variables |  | [```config.py```](3.%20Logic/config.py) | os.getenv(...)  |
| __SQLAlchemy__ | Data Model Classes | [```database/models.py```](3.%20Logic/database/models.py) |  |  |
|  | Read / Write | [```api/end_points.py```](3.%20Basic_App/api/end_points.py) | [```api/customize_api.py```](3.%20Logic/api/customize_api.py) | see `def order():`  |
|  | Multiple Databases |  | [```database/bind_databases.py```](3.%20Logic/database/bind_databases.py) |   |
|  | Events |  | [```security/system/security_manager.py```](3.%20Logic/security/system/security_manager.py) |  |
| __Logic__ | Business Rules | n/a | [```logic/declare_logic.py```](3.%20Logic/logic/declare_logic.py) | ***Unique*** to API Logic Server  |
| __Security__ | Multi-tenant | n/a | [```security/declare_security.py```](3.%20Logic/security/declare_security.py) |   |
| __Behave__ | Testing |  | [```test/.../place_order.py```](3.%20Logic/test/api_logic_server_behave/features/steps/place_order.py) |  |
| __Alembic__ | Schema Changes |  | [```database/alembic/readme.md```](3.%20Logic/database/alembic/readme.md) |   |
| __Docker__ | Dev Env | | [```.devcontainer/devcontainer.json```](.devcontainer/devcontainer.json) | See also "For_VS_Code.dockerFile" |
|  | Containerize Project |  | [```devops/docker/build-container.dockerfile```](3.%20Logic/devops/docker/build-container.dockerfile) |  |