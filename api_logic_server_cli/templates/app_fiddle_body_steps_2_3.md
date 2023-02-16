<summary>2. API Logic Project: Instant, Open</summary>

&nbsp;

Instead of frameworks, we might consider a Low Code approach.  Low Code tools provide excellent custom user interfaces.  However, these often require extensive screen painting, and typically require a proprietary IDE.

The *2. ApiLogicProject* app provides an alternative, creating an entire project by reading your schema.  This approach is:

* **Instant:** faster than Low Code screen painting, with instant APIs and Admin User Interfaces:

  * **API:** an endpoint for each table, with filtering, sorting, pagination and related data access.  Swagger is automatic.

  * **Admin UI:** multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show.  It executes a yaml file, so basic customizations do not require HTML or JavaScript background.

      * Custom UIs can be built using your tool of choice (React, Angular, etc), using the API

* **Open:** a fully open approach:

  * **Open Source:** install with pip or docker

  * **Open Technology:** using standard IDEs such as VSCode or PyCharm.  All of the key technology concepts you mastered above (Flask, SQLAlchemy) still fully apply.

This application was *not coded* - **it was created** using the API Logic Server CLI (Command Language Interface), with 1 command (don't do this now - it's already been done):

```bash
ApiLogicServer create --project_name=ApiLogicProject --db_url=nw-  # use Northwind, no customizations
```

To execute (see *Show me how*, below, for details): **restart the server** with **Run and Debug >> *2.API...***, and then start the Browser at localhost:5656 **(url in the console log)**

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

<figure><img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/2-apilogicproject.png?raw=true"></figure>

</details>

&nbsp;

> Key Takeway: you will achieve this level automation for your projects: provide a database, get an instant API and Admin App.  Then, customize in your IDE. 

&nbsp;

An instant Admin App and API are a great start, but there are some significant short-comings:

* **No security -** no login authentication

* **No logic -** multi-table derivations and constraints for save logic

    * For example, open **Customers**, **double-click first Order**, and **delete the first Order**.  Re-click Customer from the left nav menu - it should have reduced the customer's balance from 2102, but it's unchanged.   That's because there is *no logic...*

Let's see how these are addressed, in the next section.

</details>

&nbsp;

<details markdown>


<summary>3. Api Logic Project Logic: Unique Spreadsheet-like Rules -- 40X More Concise</summary>

&nbsp;

A running API and UI are a great start, but completing the project still requires logic and security.  This can be as much as half the effort, so we really haven't achieved "Low Code" until these are addressed.

A unique feature of API Logic Server is provision for:

* **Business Logic Automation:** using unique spreadsheet-like rules for multi-table derivation and constraint update logic, extensible with Python.  Rules offer significant advantages:

  * Remarkable agility with automatic dependency management - 40x more concise than code
  * Simplify maintenance with automatic ordering
  * Improve quality through automatic reuse and partitioning
  * Faciliate collaboration since business users can read them


* Rules are **declared in *your IDE,*** with full support for code completion, logging, and debugging.

The *3. ApiLogicProject_Logic* application is a clone of the prior example, customized in VSCode:

* **API:** additional endpoints are defined in ```3. ApiLogicProject_Logic/api/customize_api.py```

* **Logic:** the project now implements logic and security

* **User Interface:** the app now has help text that walks you through the key features

You can run the app.  

1. **Stop the server** using the red "stop" button).
2. **Restart the server** with the same procedure as Step 2, above, but choose Run Configuration ***3. API Logic Project: Logic***.  

Observe the customizations in `3. ApiLogicProject_Logic`:

1. Click Category - you need to **login** now (user u1, password p).  That's because authentication has been activated.

2. Categories has fewer rows per **multi-tenant Grant logic** in ```3. ApiLogicProject_Logic/security/declare_security.py```

3. The app now shows **help text** to introduce its features per updates in ```3. ApiLogicProject_Logic/ui/admin/admin.yaml```

4. Our Delete Order test adjusts the customer balance, since we how have **business logic** in ```3. ApiLogicProject_Logic/logic/declare_logic.py```

5. You can explore the Swagger via *item 2 on the Home* page

    * You will need to authenticate as explained in the [project documentation](https://apilogicserver.github.io/Docs/Security-Overview/)

    * You can try the customized API with the custom service using *CategoriesEndPoint/get_cats,* authenticated as *u1*.  See  ```ApiLogicProject_Logic/api/customize_api.py```

You can use VSCode to *diff* these from their originals in the `2. ApiLogicProject`.

&nbsp;

> **Key Take-aways** <br>1. **Instant** project creation<br>2. Spreadsheet-like **Rules**<br>3. Fully Customizable in ***your* IDE**.


</details>
&nbsp;

<details markdown>

&nbsp;

<summary>Next Steps: new projects</summary>

Use the [```Detailed Tutorial```](3.%20ApiLogicProject_Logic/Tutorial.md) to further explore this app.


As shown above, it's easy to create projects with a single command.  To help you explore, ApiLogicServer provides several pre-installed sqlite databases.  For example, create a project for this 1 table database:

```bash
cd tutorial
ApiLogicServer create --project_name=todo --db_url=todo
```
Then, **restart** the server as above, using the Run Configuration for `Execute ToDo`.

You can also try these other examples (be sure to `cd tutorial`; use the name below for both the _project_name_ and the _db_url_):

* **chinook** - albums and artists
* **classicmodels** - customers and orders

Launch configurations have been pre-created, then re-execute the Admin app as above.

> Next, try it on your own databases: if you have a database, you can have an API and an Admin app in minutes.

&nbsp;

<details markdown>

<summary> Providing the db_url for your own database </summary>

&nbsp;

The system provides shorthand notations for the pre-installed sample databases above.  For your own databases, you will need to provide a SQLAlchemy URI for the `db_url` parameter.  These can be tricky - try `ApiLogicServer examples`, or, when all else fails, [try the docs](https://apilogicserver.github.io/Docs/Database-Connectivity/).

</details>


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
| __API__ | Create End Point | [```api/end_points.py```](Basic_App/api/end_points.py) | [```api/customize_api.py```](3.%20ApiLogicProject_Logic/api/customize_api.py) |  see `def order():` |
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