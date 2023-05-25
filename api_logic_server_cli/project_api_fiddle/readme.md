# API Fiddle

Run under Codespaces -- [click here](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=641207071).


<details markdown>

<br>

<summary>An "API Fiddle" - courtesy Codespaces</summary>

About this site:

* *What:*  **Learn about JSON:API, Flask, and SQLAlchemy**

* *Why:* a complement to conventional tutorials and docs, learn using a **complete executable environment**:

    * Akin to a **JS Fiddle** - but here for a *complete environment:* running sample projects with live, updatable databases.

    * **Test the JSON:API** on the live database, with Swagger, cURL and an Admin App. 

      * **Discover instant creation** and **logic enforcement**, using API Logic Server<br><br>
    
    * **Explore the project code** -- use the debugger, experiment with it.

* *How:* the enabling technology is Codespaces.  It creates a cloud machine for these projects, and **starts VSCode in your Browser.**  This eliminates install, configuration, and risk to your local machine.

</details fiddle>

&nbsp;

----

&nbsp;

<details markdown>

<br>

<summary>Welcome -- Learn about APIs, using Flask and SQLAlchemy</summary>

This Learning Center is designed to help you learn about creating APIs, specifically JSON:APIs, using Python Flask and SQLAlchemy.  

**RESTful APIs** have become a common element of a modern software architecture to provide **networked database access**s.  Microservice concepts stress that **APIs should enforce the *business logic*** for integrity and security.

This contains 2 ready-to-run projects:<br>

| Project | What it is | Use it to explore... | Notes |
|:---- |:------|:-----------|:-----------|
| 1. Learn APIs using Flask SqlAlchemy | Northwind Database<br>- Single Endpoint | **Flask / SQLAlchemy** basics | With HTTP, REST background |
| 2. Learn JSON_API using API Logic Server | Northwind Database<br> - All Endpoints<br>- With Logic | **JSON:API**, and<br>Rule-based business logic | You can start here if only interested in JSON:API |
| Next Steps | Create other sample databases | More examples - initial project creation from Database |

&nbsp;

These projects use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/) (customers, orders, products).

> Suggestion: close *Welcome*, above, to proceed.

&nbsp;
&nbsp;

---

</details>

&nbsp;

<details markdown>

<br>

<summary>1. Learn APIs using Flask SqlAlchemy -- Fully customizable, but slow</summary>

This first app (_1. Learn Flask / SQLAlchemy_) illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.  Let's run/test it, then explore the code.

To run, use the Run Configuration, and test with `cURL`.  

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Show me how </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see **1. Learn APIs using Flask SqlAlchemy**), and the green button to start the server

    * Do ***Not*** click `Open in Browser`<br><br>

2. Copy the `cURL` text

3. Open the `bash` window, and paste the `cURL` text

    * Observe the resulting response text<br><br>

4. [**Open the readme**](./1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/readme.md) to understand Flask / SQLAlchemy usage

    * The readme also provides brief background on APIs, Flask, and SQLAlchemy

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app.png?raw=true)

</details>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;--> Fully Customizable, but Faster Would Be Better</summary>

&nbsp;

Frameworks like Flask are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project **does not provide:**

<img align="right" width="150" height="150" src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/vscode/app-fiddle/horse-feathers.jpg?raw=true" alt="Horse Feathers">

* an API endpoint for each table

    * We saw above it's straightforward to provide a *single endpoint.*  It's quite another matter -- ***weeks to months*** -- to provide endpoints for **all** the tables, with pagination, filtering, and related data access.  That's a horse of an entirely different feather.<br><br>

* a User Interface

* any security, or business logic (multi-table derivations and constraints).

Below, we'll see an approach that combines the ***flexibility of a framework with the speed of low-code.***

</details>

&nbsp;

When you are done, **stop** the server (Step 3).

&nbsp;

> You might want to close _1. Learn APIs using Flask SqlAlchemy..._, above.

&nbsp;

&nbsp;

---

</details>

&nbsp;



<details markdown>

<summary>2. Learn JSON_API using API Logic Server -- Standard API, Logic Enabled, Declarative</summary>

<br>

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Project Overview</summary>

<br>

Project 2 is much more like a real server.  It:

* Implements a **JSON:API -- a standard definition** for filtering, sorting, pagination, and multi-table retrieval.
  * Such **standards eliminate complex and time-consuming design**

  *  JSON:APIs are **self-service**, with *consumer-defined* response inclusion
      * Similar to GraphQL, clients declare what data to include, rather than relying on pre-defined resources.<br><br>

* Was **built using API Logic Server** --  an open source project providing:

  * **Automatic Creation:** a single command creates the project from your database (including an Admin App)

  * **Customize with your IDE:** declare spreadsheet-like **business logic rules**, and code extra API endpoints


&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;What is API Logic Server </summary>

&nbsp;

**What is Installed**

API Logic server installs with `pip`, in a docker container, or (here) in codespaces.  As shown below, it consists of a:

* **CLI:** the `ApiLogicServer create` command you saw above
* **Runtime Packages:** for API, UI and Logic execution<br>

![](https://apilogicserver.github.io/Docs/images/Architecture-What-Is.png)

&nbsp;

**Development Architecture**

It operates as shown below:

* A) Create your database as usual

* B) Use the CLI to generate an executable project

  * E.g.: `ApiLogicServer create --project_name=nw --db_url=nw-`

  * The system reads your database to create an executable API Logic Project<br>
&nbsp;

* C) Customize and debug it in VSCode, PyCharm, etc.

  * Declare logic, code new endpoints, customize the data model


![](https://apilogicserver.github.io/Docs/images/creates-and-runs.png)

&nbsp;

**Standard, Scalable Modern Architecture**

* A modern 3-tiered architecture, accessed by **APIs**
* Logic is **automatically invoked**, operating as a SQLAlchemy event listener
  * Observe logic is *automatic re-used* by web apps and custom services
* **Containerized** for scalable cloud deployment - the project includes a dockerfile to containerize it to DockerHub.


![API Logic Server Intro](https://apilogicserver.github.io/Docs/images/Architecture.png)

</details what is api logic server>

&nbsp;

Let's &nbsp;  2.a) Start the Server, &nbsp; 2.b) Explore the JSON:API, &nbsp; and 2.c) Explore JSON:API Update Logic.

&nbsp;

> You might want to close _Project Overview_, above.

&nbsp;

</details project overview>


&nbsp;


<details markdown>

<summary>&nbsp;&nbsp;&nbsp;2.a) Start the Server and Open the Admin App</summary>

&nbsp;

1. Start the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **2. Learn JSON_API using API Logic Server**, and
    3. Click the green button to start the server
<br><br>

2. **Open in Browser** as shown below (you'll need to wait a moment for the server to restart for debug support).
    * This opens the Admin App, which provides access to Swagger.

![](https://apilogicserver.github.io/Docs/images/tutorial/2-apilogicproject.png)

</details run project>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;2.b) Explore JSON:API Get Using Swagger</summary>

<br>

Let's now use Swagger (automatically created) to explore the API.

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.1) Open Swagger from the Admin App Home Page </summary>

&nbsp;

Automatic Swagger: from the **Home** page of the Admin App, execute it like this:

  1. Click **2. API, with oas/Swagger**
  2. Click **Customer**
  3. Click **Get**
  4. Click **Try it out**
  5. Click **Execute**:

![](https://apilogicserver.github.io/Docs/images/tutorial/explore-api.png)  

</details swagger>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.2) Consumer-defined response: the include argument</summary>

&nbsp;

Note the `include` argument; you can specify:

```
OrderList,OrderList.OrderDetailList,OrderList.OrderDetailList.Product
```

You can paste the `Customer` response into tools like [jsongrid](https://jsongrid.com/json-grid):

![](https://apilogicserver.github.io/Docs/images/tutorial/jsongrid.png)

</details consumer>

&nbsp;


<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.3) Extensible: Python, Flask, SQLAlchemy </summary>

&nbsp;

All the API functions so far were completely created by API Logic Server.  As required, you extend the API using standard Python, Flask and SQLAlchemy.

See the code in `api/customize_api.py`, and find the code `order()`.  Test it with the cURL string provided in the comments.

You can also make the endpoint **visible in swagger**.  Find the code `ServicesEndPoint(safrs.JABase)`.

&nbsp;

> Suggestion: close *2.b) Explore JSON:API Get Using Swagger*, above, to proceed.

&nbsp;

</details extensible>

</details what is json:api>

&nbsp;
<details markdown>

<summary>&nbsp;&nbsp;&nbsp;2.c) Explore JSON:API Update Logic </summary>

&nbsp;

APIs must ensure that updates adhere to business rules: **multi-table derivations and constraints**.  Such business logic is not only critical, it's extensive: it often constitutes **nearly half the code**.

API Logic Server enables you to declare **spreadsheet-like rules** for multi-table derivations and constraints, extensible with Python.  Just as a spreadsheet simplifies financial analysis, these **rules are 40X more concise than code.**

* Rules are declared in `logic/declare_logic.py` (IDE provides *code completion*)

* For more on rules, see `logic/readme_declare_logic.py`

&nbsp;

**Patch to test logic**

If we:

1. Set the breakpoint as shown in the screenshot below, and then 
2. `Patch` the data below

```bash
curl -X 'PATCH' \
  'http://localhost:5656/api/OrderDetail/1040/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "attributes": {
      "Quantity": 160
    },
    "type": "OrderDetail",
    "id": "1040"
  }
}'
```

We see the log of logic execution (note the **multi-table rule chaining**), and the system state at our breakpoint:

![API Logic Server Intro](https://apilogicserver.github.io/Docs/images/tutorial/patch-orderdetail.png)


&nbsp;

Use the [```Detailed Tutorial```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/tutorial.md) to further explore this app.  

&nbsp;

<details markdown>

&nbsp;

<summary>Key Takeaways: JSON:APIs -- Instantly, With Logic and Admin App; Standard Tools </summary>

**JSON:APIs** are worth a look:

* **Eliminate design complexity and delays** with standards
* **Eliminate bottlenecks** in backend development with Self-service APIs 

**API Logic Server** creates JSON:API systems instantly:

1.  **Instantly executable projects** with the `ApiLogicServer create` command, providing:

    * **a JSON:API:** end point for each table -- multi-table, filtering, sorting, pagination... ready for custom app dev
    * **an Admin App:** multi-page, multi-table apps... ready for business user agile collaboration<br><br>

2. **Leverage Standard Tools** for development and deployment:

    * Dev: customize and debug with **<span style="background-color:Azure;">standard dev tools</span>**.  Use *your IDE (e.g. <span style="background-color:Azure;">VSCode, PyCharm</span>)*, <span style="background-color:Azure;">Python</span>, and Flask/SQLAlchemy to create new services.  Manage projects with <span style="background-color:Azure;">GitHub</span>.

    * Deploy: **containerize** your project - deploy on-premise or to the cloud <span style="background-color:Azure;">(Azure, AWS, etc)</span>.
    
    * *Flexible as a framework, Faster then Low Code for Admin Apps*

3. ***Declare* security and multi-table constraint/validation logic**, using **declarative spreadsheet-like rules**.  Addressing the backend *half* of your system, logic consists of rules, extensible with Python event code.

     * *40X more concise than code - unique to API Logic Server*<br><br>

</details key takeaways>

&nbsp;

<details markdown>

&nbsp;

**Try Creating New Projects**

<details markdown>

<summary>Creating New Projects</summary>

&nbsp;

As described above, you can create projects with a single command.  To help you explore, ApiLogicServer provides several pre-installed sqlite sample databases:

```bash
cd API_Fiddle

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

</details url>

</details new projects>

&nbsp;

<summary>Notes, Next Steps: New Projects</summary>

**Project Structure**

<details markdown>

&nbsp;

<summary>Project Structure</summary>

This tutorial is actually 2 independent projects.  When you create a project using `ApiLogicServer create --project_name=my_project`, the system will create a free-standing project.  The project will include your container settings, IDE settings etc, so you can just open it your IDE to run and debug.

</details project structure>


</details notes next steps>

</details explore api logic server>

&nbsp;

&nbsp;

---

</details 2. JSON_API>

&nbsp;

<details markdown>

<summary>Appendix: Key Technology Concepts Review</summary>


<p align="center">
  <h2 align="center">Key Technology Concepts</h2>
</p>
<p align="center">
  Select a skill of interest, and<br>Click the link to see sample code
</p>
&nbsp;


| Tech Area | Skill | 1. Learn APIs Example | 2. Learn JSON:API Example | Notes   |
|:---- |:------|:-----------|:--------|:--------|
| __Flask__ | Setup | [```flask_basic.py```](1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/flask_basic.py) |  [```api_logic_server_run.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/api_logic_server_run.py) |  |
|  | Events | |  [```ui/admin/admin_loader.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/ui/admin/admin_loader.py) |  |
| __API__ | Create End Point | [```api/end_points.py```](1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/api/end_points.py) | [```api/customize_api.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/api/customize_api.py) |  see `def order():` |
|  | Call endpoint |  | [```test/.../place_order.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/test/api_logic_server_behave/features/steps/place_order.py) | |
| __Config__ | Config | [```config.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/config.py) | | |
|  | Env variables |  | [```config.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/config.py) | os.getenv(...)  |
| __SQLAlchemy__ | Data Model Classes | [```database/models.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/database/models.py) |  |  |
|  | Read / Write | [```api/end_points.py```](3.%20Basic_App/api/end_points.py) | [```api/customize_api.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/api/customize_api.py) | see `def order():`  |
|  | Multiple Databases |  | [```database/bind_databases.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/database/bind_databases.py) |   |
|  | Events |  | [```security/system/security_manager.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/security/system/security_manager.py) |  |
| __Logic__ | Business Rules | n/a | [```logic/declare_logic.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/logic/declare_logic.py) | ***Unique*** to API Logic Server  |
| __Security__ | Multi-tenant | n/a | [```security/declare_security.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/security/declare_security.py) |   |
| __Behave__ | Testing |  | [```test/.../place_order.py```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/test/api_logic_server_behave/features/steps/place_order.py) |  |
| __Alembic__ | Schema Changes |  | [```database/alembic/readme.md```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/database/alembic/readme.md) |   |
| __Docker__ | Dev Env | | [```.devcontainer/devcontainer.json```](.devcontainer/devcontainer.json) | See also "For_VS_Code.dockerFile" |
|  | Containerize Project |  | [```devops/docker/build-container.dockerfile```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/devops/docker/build-container.dockerfile) |  |