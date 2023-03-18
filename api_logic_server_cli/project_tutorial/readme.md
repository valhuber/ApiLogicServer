# Tutorial

<details markdown>

<br>

<summary>Welcome to this Tutorial</summary>

Use this Tutorial for a quick tour of API Logic Server 

- **Instant** project creation from a database
- **Fully customizable,** using both standard code (Flask/SQLAlchemy), and **rules** -- in *your* IDE

This contains several projects:


| Project | What it is | Use it to... |
|:---- |:------|:-----------|
| 1. Basic_App | Hand Coded app - 1 endpoint | Learn basic Flask / SQLAlchemy coding |
| 2. ApiLogicProject | Northwind Database - Uncustomized | Explore **automated project creation** from Database |
| 3. ApiLogicProject_Logic | Northwind Database - Customized | Explore **customizing** with code, and rule-based logic |
| Next Steps | Create other sample databases | More examples - initial project creation from Database |

&nbsp;

Using this tutorial:

- Project 1 is focused on learning Flask/SQLAlchemy.  
    - You probably want to **skip** this initially.
    - One advantage of API Logic Server is that you can deliver results *while you learn* Python, Flask and SQLAlchemy.
- If you want to focus on **project creation,** you can start with *Next Steps*.
- The Key Technology Concepts (at end) is an inventory of essential skills for creating Flask/SQLAlchemy systems.  Each are illustrated here.

Projects 1-3 use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/).  

If you are running via `pip install` (not Docker or Codespaces), you need to [setup your virtual environment](https://apilogicserver.github.io/Docs/Project-Env/#shared-venv).


</details>

&nbsp;

<details markdown>

<br>

<summary>1. Basic App: Manually Coded -- Learn Flask / SQLAlchemy - Fully customizable, but slow</summary>

This first app (_1. Basic App_) illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.  Let's run/test it, then explore the code.

To run, use the Run Configuration, and test with `cURL`.  

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Show me how </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see *1. Basic App: Flask / SQLAlchemy*), and the green button to start the server

2. Copy the `cURL` text, and paste it into the `bash`/`zsh` window

3. When you have reviewed the result ([here's the readme](./1.%20Basic_App/readme.md)), **stop** the server

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app-tutorial.png?raw=true)


</details>


&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;--> Fully Customizable, but Faster Would Be Better</summary>

&nbsp;

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project **does not provide:**

<img align="right" width="150" height="150" src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/vscode/app-fiddle/horse-feathers.jpg?raw=true" alt="Horse Feathers">

* an API endpoint for each table

    * We saw above it's straightforward to provide a *single endpoint.*  It's quite another matter -- *weeks to months* -- to provide endpoints for **all** the tables, with pagination, filtering, and related data access.  That's a horse of an entirely different feather.<br><br>

* a User Interface

* any security, or business logic (multi-table derivations and constraints).

Instead of frameworks, we might consider a Low Code approach.  Low Code tools provide excellent custom user interfaces.  However, these often require extensive screen painting, and typically require a proprietary IDE.

The next section introduces an approach that is as flexible as a framework, but faster than Low Code for APIs and Admin Apps.

</details>

</details>

&nbsp;


<details markdown>

<summary>2. API Logic Project: Automation -- Customizable as a framework, Faster than Low Code</summary>

<br>

The *2. ApiLogicProject* app illustrates an alternative, creating an entire project by reading your schema.  This automated approach is:

* **Instant:** faster than Low Code screen painting, with instant APIs and Admin User Interfaces:

  * **Admin UI:** multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show.  It executes a yaml (model) file, so basic customizations do not require HTML or JavaScript background.  Ready for Agile collaboration.

      * Custom UIs can be built using your tool of choice (React, Angular, etc), using the API<br><br>

  * **API:** an endpoint for each table, with filtering, sorting, pagination and related data access.  Swagger is automatic.  Ready for custom app dev.

* **Fully Customizable:** with **standard dev tools**.  Use *your IDE*, Python, and Flask/SQLAlchemy to create new services.  We'll see several examples in the `ApiLogicProject_Logic`, below. 

* **Open Source:** install with pip or docker.


This application was *not coded* - **it was created** using the API Logic Server CLI (Command Language Interface), with 1 command (don't do this now - it's already been done):

```bash
ApiLogicServer create --project_name=ApiLogicProject --db_url=nw-  # use Northwind, no customizations
```
&nbsp;

To execute (see *Show me how*, below, for details): **restart the server** with **Run and Debug >> *2. API Logic Server: Instant, Open***, and then start the Browser at localhost:5656 **(url in the console log)**

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Show me how </summary>

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/2-apilogicproject-tutorial.png?raw=true)

&nbsp;

</details>

&nbsp;

> Key Takeway: you will achieve this level automation for your projects: provide a database, get an instant API and Admin App.  Ready for agile collaboration, custom app dev.  Then, customize in your IDE. 

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;What is API Logic Server </summary>

&nbsp;

API Logic server installs with `pip`, in a docker container, or in codespaces.  As shown below, it consists of a:

* **CLI:** the `ApiLogicServer create` command you saw above
* **Runtime Packages:** for API, UI and Logic execution

![](https://apilogicserver.github.io/Docs/images/Architecture-What-Is.png)

&nbsp;

It operates as shown below:

* Reads your database to create an executable API Logic Project; customize and debug it in VSCode, PyCharm, etc.
* The executing server is a standard horizontally scalable Flask project, using SQLAlchemy for database access.  

![](https://apilogicserver.github.io/Docs/images/creates-and-runs.png)

For production deployment, the project includes a dockerfile to containerize it to DockerHub.

</details>


&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;--> Instant, But Customization Required</summary>

&nbsp;

An instant Admin App and API are a great start, but there are some significant short-comings:

* **No security -** no login authentication

* **No logic -** multi-table derivations and constraints for save logic

    * For example, open **Customer** (left nav menu), **click `ALFKI`**, and **EDIT > DELETE the first Order**.  Re-click Customer from the left nav menu - it should have reduced the customer's balance from 2102, but it's unchanged.   That's because there is *no logic...*

    * Backend update logic can be as much as half the effort, so we really haven't achieved "Low Code" until this are addressed.

Let's see how these are addressed, in the next section.

</details>

</details>

&nbsp;

<details markdown>

<summary>3. Api Logic Project Logic: Customized -- Code and unique spreadsheet-like Rules (40X more concise)</summary>

<br>

Customizations are addressed using your IDE, with:

* **Standard Code:** use Flask and SQLAlchemy, exactly as you normally do, and


* **Logic:** unique spreadsheet-like rules address multi-table constraints and derivations, improving conciseness by a remarkable 40x.  Rules are **declared in *your IDE,*** with full support for code completion, logging, and debugging.

Customizations are illustrated in the project [`3. ApiLogicProject_Logic`](3.%20ApiLogicProject_Logic/).  To see the effect of the changes, run the app like this:

1. **Stop the server** using the red "stop" button.
2. **Restart the server** with the same procedure as Step 2, above, but choose Run Configuration ***3. API Logic Project: Logic***.<br>

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

This project is the customized version of _2. ApiLogicProject_, above.  The table below lists some of the key customizations you can explore.

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
| **New API endpoint <--**         | Use Swagger for endpoint: *CategoriesEndPoint/get_cats*<br><br>See [docs](https://apilogicserver.github.io/Docs/Security-Swagger/) - authenticate as **u1**  | [```api/customize_api.py```](3.%20ApiLogicProject_Logic/api/customize_api.py)                 | Standard Flask/SQLAlchemy  |
| **Multi-table Update Logic <--** | Delete Order now adjusts the customer balance                                                                                                                                                    | [```logic/declare_logic.py```](3.%20ApiLogicProject_Logic/logic/declare_logic.py)             |  Spreadsheet-like rules                    |                                                                
| **Admin App <--**  | Observe **help text** describes features                                                                                                                                                 | [```ui/admin/admin.yaml```](3.%20ApiLogicProject_Logic/ui/admin/admin.yaml)                  | Not complex JS, HTML                     |
| **Login Authentication**     | Click Category - observe you need to **login** now (user u1, password p)                                                                                                                                  | [```config.py```](3.%20ApiLogicProject_Logic/config.py)                                       | See SECURITY_ENABLED |
| **Role-Based Authorization** | Observe categories has **fewer rows**                                                                                                                                                                         | [```security/declare_security.py```](3.%20ApiLogicProject_Logic/security/declare_security.py) |                      |

&nbsp;

Use the [```Detailed Tutorial```](3.%20ApiLogicProject_Logic/Tutorial.md) to further explore this app.  

</details>

&nbsp;

<details markdown>

&nbsp;

<summary>Key Takeaways: Instant App/API, Standard-based Customization, Unique Declarative Rules</summary>

You have seen the **fastest and simplest** way to create **modern, scalable API-based database systems:**

1. Use the `ApiLogicServer create` command to create a Flask/SQLAlchemy project from your database. Zero learning curve. Projects are **instantly executable**, providing:

    * **an Admin App:** multi-page, multi-table apps -- ready for business user agile collaboration
    * **an API:** end points for each table, with filtering, sorting, pagination and related data access -- ready for custom app dev<br><br>

2. **Customize** and debug your application with **standard dev tools**.  Use *your IDE*, Python, and Flask/SQLAlchemy to create new services.

     * Flexible as a framework, faster than Low Code for Admin Apps<br><br>

3. ***Declare* security and multi-table constraint/validation logic**, using unique spreadsheet-like rules. Logic consists of rules, extensible with Python event code as required.

     * 40X more concise than code - unique to API Logic Server

</details>

&nbsp;
<details markdown>

&nbsp;

<summary>Next Steps: new projects</summary>

As shown above, it's easy to create projects with a single command.  To help you explore, ApiLogicServer provides several pre-installed sqlite databases.  For example, create a project for this 1 table database:

```bash
cd tutorial
ApiLogicServer create --project_name=nw --db_url=nw-                       # same sample as 2, above
ApiLogicServer create --project_name=chinook --db_url=chinook              # artists and albums
ApiLogicServer create --project_name=classicmodels --db_url=classicmodels  # customers, orders
ApiLogicServer create --project_name=todo --db_url=todo                    # 1 table database

```
Then, **restart** the server as above, using the pre-created Run Configuration for `Execute <new project>`.<br><br>

> Next, try it on your own databases: if you have a database, you can have an API and an Admin app in minutes.

&nbsp;

<details markdown>

<summary> Providing the db_url for your own database </summary>

&nbsp;

The system provides shorthand notations for the pre-installed sample databases above.  For your own databases, you will need to provide a SQLAlchemy URI for the `db_url` parameter.  These can be tricky - try `ApiLogicServer examples`, or, when all else fails, [try the docs](https://apilogicserver.github.io/Docs/Database-Connectivity/).

</details>

&nbsp;

Click here for the [docs](https://apilogicserver.github.io/Docs/).

</details>

&nbsp;

<details markdown>

<summary> Notes </summary>




Please find additional notes below.

<details markdown>

<summary> Project Structure </summary>

&nbsp;

This tutorial is actually 3 independent projects.  When you create a project using `ApiLogicServer create --project_name=my_project`, the system will create a free-standing project.  The project will include your container settings, IDE settings etc, so you can just open it your IDE to run and debug.

</details>


</details>

&nbsp;

<p align="center">
  <h2 align="center">Key Technology Concepts</h2>
</p>
<p align="center">
  Select a skill of interest, and<br>Click the link to see sample code
</p>
&nbsp;


| Tech Area | Skill | Basic App Example | APILogicProject Logic Example | Notes   |
|:---- |:------|:-----------|:--------|:--------|
| __Flask__ | Setup | [```flask_basic.py```](1.%20Basic_App/flask_basic.py) |  [```api_logic_server_run.py```](3.%20ApiLogicProject_Logic/api_logic_server_run.py) |  |
|  | Events | |  [```ui/admin/admin_loader.py```](3.%20ApiLogicProject_Logic/ui/admin/admin_loader.py) |  |
| __API__ | Create End Point | [```api/end_points.py```](1.%20Basic_App/api/end_points.py) | [```api/customize_api.py```](3.%20ApiLogicProject_Logic/api/customize_api.py) |  see `def order():` |
|  | Call endpoint |  | [```test/.../place_order.py```](3.%20ApiLogicProject_Logic/test/api_logic_server_behave/features/steps/place_order.py) | |
| __Config__ | Config | [```config.py```](3.%20ApiLogicProject_Logic/config.py) | | |
|  | Env variables |  | [```config.py```](3.%20ApiLogicProject_Logic/config.py) | os.getenv(...)  |
| __SQLAlchemy__ | Data Model Classes | [```database/models.py```](3.%20ApiLogicProject_Logic/database/models.py) |  |  |
|  | Read / Write | [```api/end_points.py```](3.%20Basic_App/api/end_points.py) | [```api/customize_api.py```](3.%20ApiLogicProject_Logic/api/customize_api.py) | see `def order():`  |
|  | Multiple Databases |  | [```database/bind_databases.py```](3.%20ApiLogicProject_Logic/database/bind_databases.py) |   |
|  | Events |  | [```security/system/security_manager.py```](3.%20ApiLogicProject_Logic/security/system/security_manager.py) |  |
| __Logic__ | Business Rules | n/a | [```logic/declare_logic.py```](3.%20ApiLogicProject_Logic/logic/declare_logic.py) | ***Unique*** to API Logic Server  |
| __Security__ | Multi-tenant | n/a | [```security/declare_security.py```](3.%20ApiLogicProject_Logic/security/declare_security.py) |   |
| __Behave__ | Testing |  | [```test/.../place_order.py```](3.%20ApiLogicProject_Logic/test/api_logic_server_behave/features/steps/place_order.py) |  |
| __Alembic__ | Schema Changes |  | [```database/alembic/readme.md```](3.%20ApiLogicProject_Logic/database/alembic/readme.md) |   |
| __Docker__ | Dev Env | | [```.devcontainer/devcontainer.json```](.devcontainer/devcontainer.json) | See also "For_VS_Code.dockerFile" |
|  | Containerize Project |  | [```devops/docker/build-container.dockerfile```](3.%20ApiLogicProject_Logic/devops/docker/build-container.dockerfile) |  |