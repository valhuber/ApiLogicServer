# Tutorial

<details markdown>

&nbsp;

<summary>Approach: Learn By Example</summary>

Tutorials are useful ways to learn, but the __key concepts__ can be overshadowed by mechanics, and often don't include the real-world __IDE experience__.

Here we take a different approach: a __running app__ you can explore, using the table below:

* Explore code samples for key technology areas
* In a _running_ project
* That you can experiment with (debug, alter...)

To __explore code__, click the _Sample Code_ link - that will open that code file.

To __run__, use the Run/Debug configurations ("play" button, upper left).  There are 3 web apps you can run:

1. __Basic Flask: hand-coded__ web app with minimal functionality

2. __API Logic Server: Uncustomized *automation*__.  Using the [Northwind Database](https://valhuber.github.io/ApiLogicServer/Sample-Database/), this illustrates what you can expect for an initial project using your own database

3. __API Logic Project: Logic and Security__, illustrating the use of a standard IDE to add code, and declarative logic and security


</details>

&nbsp;

<details markdown>

&nbsp;

<summary>1. Basic App: Flask / SQLAlchemy -- flexible, but slow</summary>

This illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project does not provide:

* an API endpoint for each table

* a User Interface

* any security, or business logic (multi-table derivations and constraints).


</details>

&nbsp;

<details markdown>


<summary>2. API Logic Project: Instant, Open</summary>

&nbsp;

Instead of frameworks, we might employ a Low Code approach.  Low Code tools provide excellent custom user interfaces.  However, these often require extensive screen painting, and typically require a proprietary IDE.

The *API Logic Project No Customization* app provides an alternative, creating an entire project by reading your schema.  This approach is:

* **Instant:** faster than Low Code screen painting, with instant APIs and Admin User Interfaces:

  * **API:** an endpoint for each table, with filtering, sorting, pagination and related data access

  * **Admin UI:** multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show.  It executes a yaml file, so basic customizations do not require HTML or JavaScript background.

      * Custom UIs can be built using your tool of choice (React, Angular, etc), using the API

* **Open:** a fully open approach:

  * **Open Source:** install with pip or docker
  * **Open Technology:** using standard IDEs such as VSCode or PyCharm.  All of the key technology concepts you mastered above (Flask, SQLAlchemy) still fully apply.

This application was created using the API Logic Server CLI (Command Language Interface), with 1 command:

```bash
ApiLogicServer create --project_name=ApiLogicProject --db_url=nw-  # use Northwind, no customizations
```

To run:

1. Execute the Run Configuration: 2. API Logic Server: Uncustomized Automation

2. Run the admin app: **Ports > Admin App > globe**

<details markdown>

<summary> Show me how </summary>

&nbsp;

TBD

</details>

</details>

&nbsp;
<details markdown>


<summary>3. Api Logic Project Logic: Unique Spreadsheet-like Rules are 40X More Concise</summary>

&nbsp;

A running API and UI are a great start, but completing the project still requires logic and security.  This can be as much as half the effort, so we really haven't achieved "Low Code" until these are addressed.

A unique feature of API Logic Server is provision for:

* **Business Logic Automation:** using unique spreadsheet-like rules, extensible with Python 🏆

* These are declared in your IDE, with full support for code completion, logging, and debugging

This application is a clone of the prior example, customized in VSCode:

* **API:** additional endpoints are defined in ```ApiLogicProject/api/customize_api.py```
* **Logic:**
  ** **Rules** are declared in  ```ApiLogicProject/logic/declare_logic.py```
  ** **Security** (multi-tenant support) is declared in ```ApiLogicProject/security/declare_security.py```
* **User Interface:** alterations are visible in ```ApiLogicProject/ui/admin/admin.yaml```

You can use VSCode to *diff* these from their originals in the *ApiLogicProjectNoCustomizations*.

</details>

&nbsp;

<details markdown>

&nbsp;

<summary>Next steps: new projects</summary>


As shown above, it's easy to create projects with a single command.  To help you explore, ApiLogicServer provides several prepackaged sqlite databases.  For example, create a project for this 1 table database:

```bash
cd tutorial
ApiLogicServer create --project_name=todo --db_url=todo
```
You can also try these other examples (be sure to `cd tutorial`; use the name below for both the _project_name_ and the _db_url_):

* **chinook** - albums and artists
* **classicmodels** - customers and orders

Launch configurations have been pre-created, then re-execute the Admin app as above.

</details>

&nbsp;

<p align="center">
  <h2 align="center">Key Technology Concepts</h2>
</p>
<p align="center">
  Select a skill of interest, and<br>Click the link to see sample code
</p>
&nbsp;


| Tech Area | Skill | Basic Example | API Logic Server | Notes   |
|:---- |:------|:-----------|:--------|:--------|
| __Flask__ | Setup | [```flask_basic.py```](Basic_app/flask_basic.py) |  [```api_logic_server_run.py```](ApiLogicProject/api_logic_server_run.py) |  |
|  | Events | [```api/end_points.py```](Basic_app/api/end_points.py) |  [```ui/admin/admin_loader.py```](ApiLogicProject/ui/admin/admin_loader.py) |  |
| __API__ | Create End Point | [```api/end_points.py```](Basic_app/api/end_points.py) | [```api/customize_api.py```](ApiLogicProject/api/customize_api.py) |  see `def order():` |
|  | Call endpoint |  | [```test/.../place_order.py```](ApiLogicProject/test/api_logic_server_behave/features/steps/place_order.py) | y  |
| __Config__ | Config | [```config.py```](ApiLogicProject/config.py) | | x |
|  | Env variables |  | [```config.py```](ApiLogicProject/config.py) | os.getenv(...)  |
| __SQLAlchemy__ | Data Model Classes | [```database/models.py```](ApiLogicProject/database/models.py) |  | x  |
|  | Read / Write | [```api/end_points.py```](Basic_app/api/end_points.py) | [```api/customize_api.py```](ApiLogicProject/api/customize_api.py) | see `def order():`  |
|  | Multiple Databases |  | [```database/bind_databases.py```](ApiLogicProject/database/bind_databases.py) |   |
|  | Events |  | [```security/system/security_manager.py```](ApiLogicProject/security/system/security_manager.py) | x  |
| __Logic__ | Business Rules | n/a | [```logic/declare_logic.py```](ApiLogicProject/logic/declare_logic.py) | ***Unique*** to API Logic Server  |
| __Security__ | Multi-tenant | n/a | [```security/declare_security.py```](ApiLogicProject/security/declare_security.py) |   |
| __Behave__ | Testing |  | [```test/.../place_order.py```](ApiLogicProject/test/api_logic_server_behave/features/steps/place_order.py) | x  |
| __Alembic__ | Schema Changes |  | [```database/alembic/readme.md```](ApiLogicProject/database/alembic/readme.md) |   |
| __Docker__ | Dev Env | [```.devcontainer/devcontainer.json```](.devcontainer/devcontainer.json) | x | See also "dockerFile":... |
|  | Containerize Project |  | [```devops/docker/build-container.dockerfile```](ApiLogicProject/devops/docker/build-container.dockerfile) |  |