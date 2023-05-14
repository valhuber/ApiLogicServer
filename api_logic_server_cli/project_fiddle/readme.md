# Learning Center

<details markdown>

<br>

<summary>Welcome to this Tutorial -- APIs, using Flask and SQLAlchemy</summary>

Problem: network database access (B2B, App Integration, mobile apps).

Solution: RESTful API

http (url <svr, verb, args>, request, response, header)

conceptual framework, not a spec ==> Design Work, Communications (==> Swagger)


Flask and SQLAlchemy (or Django, FASTApi, ...)

Use this Tutorial to learn: 

- Learn APIs, using Flask and SQLAlchemy
- JSON_API, using API Logic Server

These projects use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/) (customers, orders, products).


| Project | What it is | Use it to... |
|:---- |:------|:-----------|
| 1. Learn APIs using Flask SqlAlchemy | Northwind Database - Single Endpoint | Explore **Flask / SQLAlchemy** basics |
| 2. Learn JSON_API With API Logic Server | Northwind Database - Customized, with Logic | Explore **customizing** with code, and rule-based logic |
| Next Steps | Create other sample databases | More examples - initial project creation from Database |

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

2. Copy the `cURL` text

3. Create a new `bash`/`zsh` window, and paste the `cURL` text

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app-tutorial.png?raw=true)

</details>

&nbsp;

[Open the readme](./1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/readme.md) for background APIs, Flask, SQLAlchemy, and a walk-through of the code.

When you are done, **stop** the server (Step 3).

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

Below, we'll see an approach that combines the ***flexibility of a framework with the speed of low-code.***

</details>

&nbsp;

You might want to close _1. Learn APIs using Flask SqlAlchemy..._, above.

&nbsp;

---

</details>

&nbsp;



<details markdown>

<summary>2. Learn JSON_API using API Logic Server -- Declarative API, Admin App, Logic</summary>

<br>

This project implements a **JSON:API -- a API standard definition** for filtering, sorting, pagination, and multi-table retrieval.  It also provides Swagger, for exploring the API.

The project was built using **API Logic Server**.  A single command creates the project from the database structure.  It provides not only the **JSON:API / Swagger**, but also an **Admin App**, and a **logic engine** for multi-table constraints and derivations.

Let's &nbsp;  a) Run the project, &nbsp; b) Explore the JSON:API, &nbsp; and c) Explore JSON:API Update Logic Using API Logic Server.

&nbsp;


<details markdown>

<summary>&nbsp;&nbsp;&nbsp;a) Run the project</summary>

&nbsp;

1. Start the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **2. Learn JSON_API using API Logic Server**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656, using the **url shown in the console log**.
  * This opens the Admin App, which provides access to Swagger.

![](https://apilogicserver.github.io/Docs/images/tutorial/2-apilogicproject-tutorial.png)

</details run project>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;b) Explore JSON:API </summary>

&nbsp;

Unlike SQL which defines a predictable syntax, RESTful API elments are programmer-defined --  arguments for filtering and sorting, multi-table response formats etc.  It is **complex and time-consuimg to design** such an API.

JSON:API addresses by defining a **standard API style**.  This saves design time and provides predictablilty.

JSON:API also answers a key design challenge of APIs by making them *consumer-defined*.  This enables other organizations and business partners to  **self-service** their own API needs.

This project implements the JSON:API style, providing:

* An endpoint for each table, with CRUD support - create, read, update and delete

* Get requests provide filtering, sorting, and pagination.  APIs include related data access, based on relationships in the models file (typically derived from foreign keys).

* Automatic Swagger: from the **Home** page of the Admin App, execute it like this:

  1. Click **2. API, with oas/Swagger**
  2. Click **Customer**
  3. Click **Get**
  4. Click **Try it out**
  5. Click **Execute**:

![](https://apilogicserver.github.io/Docs/images/tutorial/explore-api.png)  

Note the `include` argument; you can specify:

```
OrderList,OrderList.OrderDetailList,OrderList.OrderDetailList.Product
```

You can paste the `Customer` response into tools like [jsongrid](https://jsongrid.com/json-grid):

![](https://apilogicserver.github.io/Docs/images/tutorial/jsongrid.png)

Impl: models.py, expose_models (Python as DSL)

Enforces logic and security - automatic partitioning of logic from (each) client app

</details what is json:api>

&nbsp;
<details markdown>

<summary>&nbsp;&nbsp;&nbsp;c) Explore JSON:API Update Logic </summary>

&nbsp;

APIs must ensure that updates adhere to business rules: **multi-table derivations and constraints**.  Such logic is critical, and often constitutes **nearly half the code**.

API Logic Server enables you to declare **spreadsheet-like rules** for multi-table derivations and constraints, extensible with Python.  Just as a spreadsheet simplifies financial analysis, these **rules are 40X more concise than code.**

* Rules are declared in `2. Learn JSON_API using API Logic Server/logic/declare_logic.py`
  * Note the use of Python as a DSL (Domain Specific Language)
  * This leverages IDE support for type-checking, code completion, logging and debugging
* For more on rules, see `2. Learn JSON_API using API Logic Server/logic/readme_declare_logic.py`

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

</details what is api logic server>

&nbsp;

 
**Patch to test logic**

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

&nbsp;

If set the breakpoint as shown, and then `Patch` this data, we see the log of logic execution, and the system state at our breakpoint:

![API Logic Server Intro](https://apilogicserver.github.io/Docs/images/tutorial/patch-orderdetail.png)

Use the [```Detailed Tutorial```](3.%20Logic/Tutorial.md) to further explore this app.  

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

</details key takeaways>

&nbsp;

<details markdown>

&nbsp;

<summary>Notes, Next Steps: New Projects</summary>

**Project Structure**

<details markdown>

&nbsp;

<summary>Project Structure</summary>

This tutorial is actually 3 independent projects.  When you create a project using `ApiLogicServer create --project_name=my_project`, the system will create a free-standing project.  The project will include your container settings, IDE settings etc, so you can just open it your IDE to run and debug.

</details project structure>

&nbsp;

**Creating New Projects**

<details markdown>

<summary>Creating New Projects</summary>

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

Click here for the [docs](https://apilogicserver.github.io/Docs/).

</details url>

</details new projects>

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