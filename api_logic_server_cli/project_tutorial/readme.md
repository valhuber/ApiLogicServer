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

This illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.

Execute using the Run Configuration, and test with `cURL`.  You can explore key aspects of this app in the [1. Basic_app/readme.md](./1.%20Basic_App/readme.md).

<details markdown>

<summary> Show me how </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see *1. Basic App: Flask / SQLAlchemy*), and the green button to start the server

2. Copy the `cURL` text, and paste it into the `bash`/`zsh` window

3. When you have reviewed the result ([here's the readme](./1.%20Basic_App/readme.md)), **stop** the server

<figure><img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app-tutorial-tutorial.png?raw=true"></figure>

</details>

&nbsp;

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project **does not provide:**

* an API endpoint for each table

* a User Interface

* any security, or business logic (multi-table derivations and constraints).

The next section illustrates an approach that creates executable projects instantly, including support for an API, an Admin App, and logic / security.


</details>

&nbsp;


<details markdown>

<summary>2. API Logic Project: Automation -- Instant, Fully Customizable, Open Source</summary>

<br>

Instead of frameworks, we might consider a Low Code approach.  Low Code tools provide excellent custom user interfaces.  However, these often require extensive screen painting, and typically require a proprietary IDE.

The *2. ApiLogicProject* app provides an alternative, creating an entire project by reading your schema.  This automated approach is:

* **Instant:** faster than Low Code screen painting, with instant APIs and Admin User Interfaces:

  * **API:** an endpoint for each table, with filtering, sorting, pagination and related data access.  Swagger is automatic.

      * We saw above it's straightforward to provide a *single endpoint.*  It's quite another matter -- *weeks to months* -- to provide endpoints for **all** the tables, that include all the services noted above.  That's a horse of an entirely different feather.<br><br>

  * **Admin UI:** multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show.  It executes a yaml file, so basic customizations do not require HTML or JavaScript background.

      * Custom UIs can be built using your tool of choice (React, Angular, etc), using the API<br><br>

* **Fully Customizable:** use Python and standard IDEs such as VSCode or PyCharm. We'll see several examples in the `ApiLogicProject_Logic`, below. 

* **Open Source:** install with pip or docker.


This application was *not coded* - **it was created** using the API Logic Server CLI (Command Language Interface), with 1 command (don't do this now - it's already been done):

```bash
ApiLogicServer create --project_name=ApiLogicProject --db_url=nw-  # use Northwind, no customizations
```

To execute (see *Show me how*, below, for details): **restart the server** with **Run and Debug >> *2. API Logic Server: Instant, Open***, and then start the Browser at localhost:5656 **(url in the console log)**

&nbsp;

<details markdown>

<summary> Show me how </summary>

&nbsp;

To run the ApiLogicProject app, **stop the running server** (see figure above), and

1. Restart the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **2. API Logic Server: Instant, Open**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656, using the **url shown in the console log**

Don't spend too much time exploring the app, we'll see a much better version in just a moment...

<figure><img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/2-apilogicproject-tutorial-tutorial-tutorial.png?raw=true"></figure>

</details>

&nbsp;

> Key Takeway: you will achieve this level automation for your projects: provide a database, get an instant API and Admin App.  Then, customize in your IDE. 

&nbsp;

An instant Admin App and API are a great start, but there are some significant short-comings:

* **No security -** no login authentication

* **No logic -** multi-table derivations and constraints for save logic

    * For example, open **Customer** (left nav menu), **click `ALFKI`**, and **EDIT > DELETE the first Order**.  Re-click Customer from the left nav menu - it should have reduced the customer's balance from 2102, but it's unchanged.   That's because there is *no logic...*

Let's see how these are addressed, in the next section.

</details>

&nbsp;

<details markdown>

<summary>3. Api Logic Project Logic: Unique Spreadsheet-like Rules -- 40X More Concise</summary>

<br>

A running API and UI are a great start, but completing the project requires customization - new endpoints, and particularly business logic for integrity and security.  This can be as much as half the effort, so we really haven't achieved "Low Code" until these are addressed.

These are addressed using your IDE, with:

* **Standard Code:** use Flask and SQLAlchemy, exactly as you normally do, and


* **Logic:** unique spreadsheet-like rules address multi-table constraints and derivations, improving conciseness by a remarkable 40x.  Rules are **declared in *your IDE,*** with full support for code completion, logging, and debugging.

Customizations are illustrated in the project [`3. ApiLogicProject_Logic`](3.%20ApiLogicProject_Logic/).  To see the changes, run the app like this:

1. **Stop the server** using the red "stop" button.
2. **Restart the server** with the same procedure as Step 2, above, but choose Run Configuration ***3. API Logic Project: Logic***.<br>

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Remind me how</summary>

1. Restart the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **3. API Logic Project: Logic**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656, using the **url shown in the console log**

</details>

&nbsp;

This project is the customized version of _2. ApiLogicProject_, above.  The table below lists some of the key customizations you can explore.

&nbsp;

<p align="center">
  <h2 align="center">Explore Key Customizations</h2>
</p>
<p align="center">
  Explore customizations in project: <i>3. ApiLogicProject_Logic</i><br>
  Click Explore Code to see the code.
</p>

| Customization Area           | Try It                                                                                                                                                                                            | Click to Explore Code                                                                                  | Notes                |
|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------|:---------------------|
| **Login Authentication**     | Click Category - observe you need to **login** now (user u1, password p)                                                                                                                                  | [```config.py```](3.%20ApiLogicProject_Logic/config.py)                                       | See SECURITY_ENABLED |
| **Role-Based Authorization** | Observe categories has **fewer rows**                                                                                                                                                                         | [```security/declare_security.py```](3.%20ApiLogicProject_Logic/security/declare_security.py) |                      |
| **Admin App**                | Observe **help text** describes features                                                                                                                                                 | [```ui/admin/admin.yaml```](3.%20ApiLogicProject_Logic/ui/admin/admin.yaml)                  | Not complex JS, HTML                     |
| **Multi-table Update Logic** | Delete Order now adjusts the customer balance                                                                                                                                                    | [```logic/declare_logic.py```](3.%20ApiLogicProject_Logic/logic/declare_logic.py)             |  Spreadsheet-like logic                    |                                                                
| **New API endpoint**         | Use Swagger for endpoint: *CategoriesEndPoint/get_cats*<br><br>See [docs](https://apilogicserver.github.io/Docs/Security-Swagger/) - authenticate as **u1**  | [```api/customize_api.py```](3.%20ApiLogicProject_Logic/api/customize_api.py)                 | Standard Flask/SQLAlchemy  |

&nbsp;

> **Key Take-aways** <br>1. **Instant** project creation -- 1 command for an executable project<br>2. Spreadsheet-like **Rules** -- rules are a key topic, driving agility, quality and collaboration; for more information, [see here](https://apilogicserver.github.io/Docs/Logic-Why/)<br>3. Fully Customizable in ***your* IDE** -- standard Flask/SQLAlchemy

&nbsp;

Use the [```Detailed Tutorial```](3.%20ApiLogicProject_Logic/Tutorial.md) to further explore this app.

</details>

&nbsp;
<details markdown>

&nbsp;

<summary>Next Steps: new projects</summary>

As shown above, it's easy to create projects with a single command.  To help you explore, ApiLogicServer provides several pre-installed sqlite databases.  For example, create a project for this 1 table database:

```bash
cd tutorial
ApiLogicServer create --project_name=todo --db_url=todo
```
Then, **restart** the server as above, using the Run Configuration for `Execute ToDo`.

You can also try these other examples (be sure to `cd tutorial`; use the name below for both the _project_name_ and the _db_url_):

* **chinook** - albums and artists
* **classicmodels** - customers and orders

Launch configurations have been pre-created, then re-execute the Admin app as above.<br><br>

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