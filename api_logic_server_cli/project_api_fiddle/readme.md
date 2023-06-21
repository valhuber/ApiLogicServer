# API Fiddle

Run under Codespaces -- [click here](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=641207071).

&nbsp;

<details markdown>

<br>

<summary>Welcome: Learn about APIs, using Flask and SQLAlchemy -- via a Codespaces "API Fiddle" </summary>

**Background context**

* **RESTful APIs** have become an accepted approach for **networked database access**
* **JSON:API** is an API **standard** for **self-service** APIs
* Microservice concepts stress that **APIs should enforce the *business logic*** for integrity and security

&nbsp;

**About this site**

* *What:*  **Learn how to build such APIs, using Flask and SQLAlchemy**

* *Why:* learn using a **complete executable environment**, a complement to conventional tutorials and docs:

    * Akin to a **JS Fiddle** - but here for a *complete environment:* running sample projects with live, updatable databases.

    * **Test the API** on the live database, with Swagger, cURL and an Admin App

      * **Discover instant creation** and **logic enforcement**, using API Logic Server<br><br>
    
    * **Explore the project code** -- use the debugger, experiment with it.

* *How:* the enabling technology is Codespaces

    * It creates a cloud machine for these projects, and **starts VSCode in your Browser.**  This eliminates install, configuration, and risk to your local machine.

&nbsp;


**What's in this Project**

This contains 2 ready-to-run projects:<br>

| Project | What it is | Use it to explore... | Notes |
|:---- |:------|:-----------|:-----------|
| 1. Learn APIs using Flask SqlAlchemy | Northwind Database<br>- Single Endpoint | **Flask / SQLAlchemy** basics | With HTTP, REST background |
| 2. Learn JSON_API using API Logic Server | Northwind Database<br> - All Endpoints<br>- With Logic<br>- With Admin App | **JSON:API**, and<br>Rule-based business logic | You can start here if only interested in JSON:API |
| Next Steps | Create other sample databases | More examples - initial project creation from Database |

&nbsp;

These projects use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/) (customers, orders, products).

> Suggestion: close *Welcome*, above, to proceed.

&nbsp;


</details fiddle>

&nbsp;

&nbsp;

---

</details>

&nbsp;

<details markdown>

<br>

<summary>1. Learn APIs using Flask SqlAlchemy -- Fully customizable, but slow</summary>

This first app (_1. Learn Flask / SQLAlchemy_) illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.  Let's run/test it, then explore the code.

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Run / Test </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see **1. Learn APIs using Flask SqlAlchemy**), and the green button to start the server

    * Do ***Not*** click `Open in Browser`<br><br>

2. Copy the `cURL` text,<br>Open the `bash` window, and <br>Paste the `cURL` text

    * Observe the resulting response text<br><br>

![](https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app.png?raw=true)

</details>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;Explore the Code </summary>

&nbsp;

[**Open the readme**](./1.%20Learn%20APIs%20using%20Flask%20SqlAlchemy/readme.md) to understand Flask / SQLAlchemy usage

* The readme also provides brief background on APIs, Flask, and SQLAlchemy
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

Project 2 is much more like a real server:

1.  It implements a **JSON:API -- a *standard* definition** for filtering, sorting, pagination, and multi-table retrieval.

    * Such **standards eliminate complex and time-consuming design**
        * (*Rest*, unlike SQL, does not dictate syntax)<br><br>

    *  JSON:APIs are **self-service**, with *consumer-defined* response inclusion
        * Similar to GraphQL, clients declare what data to include, rather than relying on pre-defined resources.<br><br>

2.  It implements an **Admin App** (ReactAdmin)

3.  It implements **business logic**

First, let's explore the service: &nbsp;  2.a) Start the Server, &nbsp; 2.b) Explore the JSON:API, &nbsp; and 2.c) Explore JSON:API Update Logic.

Then, we'll see how to create it.

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

![](https://apilogicserver.github.io/Docs/images/ui-admin/admin-home.png)


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

  1. Click the link: **2. API, with oas/Swagger**
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

You can paste the `Customer` response into tools like [jsongrid](https://jsongrid.com/json-grid), shown below.  Note the response *includes* OrderDetail data:

![](https://apilogicserver.github.io/Docs/images/tutorial/jsongrid.png)

</details consumer>

&nbsp;


<details markdown>

<summary>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.3) Additional Services </summary>

&nbsp;

Servers often include non-JSON:API endpoints, such as the `ServicesEndPoint - add_order` to post an Order and its OrderDetails.

&nbsp;

> Suggestion: close *2.b) Explore JSON:API Get Using Swagger*, above, to proceed.

&nbsp;

</details extensible>

</details what is json:api>

&nbsp;

<details markdown>

<summary>&nbsp;&nbsp;&nbsp;2.c) Explore JSON:API Patch Logic </summary>

&nbsp;

APIs must ensure that updates adhere to business rules: **multi-table derivations and constraints**.  Such business logic is not only critical, it's extensive: it often constitutes **nearly half the code**.

It's what makes an API a service.

&nbsp;

**Patch to test logic**

This server implements such logic.  Test it by `patch`ing the data below in the Terminal Window:

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

We see that it fails - as it *should*.  Note this is a non-trivial ***muti-table*** transaction - it must:

1. Get the price from the Product
2. Compute the amount (price * quantity), which requires we...
3. Adjust the Order amount, which requires we...
4. Adjust the Customer balance, which enables us to...
5. Check the credit limit - we see it's exceeded, so we roll the transaction back and return the error response 

&nbsp;

> You might want to close _2.c) Explore JSON:API Patch Logic_, above.

</details explore api logic server>

&nbsp;

<details markdown>

&nbsp;

<summary>&nbsp;&nbsp;&nbsp;Creation is Automated: Project, SQLAlchemy Models, API, Admin, Logic </summary>

You could code all this using Flask and SQLAlchemy... but it would *take a **long** time*.

In fact, this system was not coded by hand - it was **created using API Logic Server** --  an open source project providing:

  * **Automatic Creation:** a single command creates the project from your database: SQLAlchemy Models, API, and the Admin App

  * **Customize with your IDE:** declare spreadsheet-like **business logic rules**, and code extra API endpoints using the same Flask / SQLAlchemy techniques described in the first project

      * Rules are 40X more concise than code.<br><br>


Use the [```Detailed Tutorial```](./2.%20Learn%20JSON_API%20using%20API%20Logic%20Server/tutorial.md) to further explore this app. 

&nbsp;

<details markdown>

&nbsp;

<summary>&nbsp;&nbsp;&nbsp;Explore Creating New Projects</summary>

As noted above, you can create projects with a single command.  To help you explore, there are several pre-installed sqlite sample databases:

```bash
cd API_Fiddle

ApiLogicServer create --db_url=sqlite:///sample_db.sqlite --project_name=nw

# that's a bit of a mouthful, so abbreviations are provided for pre-included samples
ApiLogicServer create --project_name=nw --db_url=nw                        # same sample as 2, above
ApiLogicServer create --project_name=nw- --db_url=nw-                      # no customization
ApiLogicServer create --project_name=chinook --db_url=chinook              # artists and albums
ApiLogicServer create --project_name=classicmodels --db_url=classicmodels  # customers, orders
ApiLogicServer create --project_name=todo --db_url=todo                    # 1 table database

```
Then, **restart** the server as above, using the pre-created Run Configuration for `Execute <new project>`.<br><br>

> Next, try it on your own databases: if you have a database, you can have an API and an Admin app in minutes.

> > Note: The system provides shorthand notations for the pre-installed sample databases above.  For your own databases, you will need to provide a SQLAlchemy URI for the `db_url` parameter.  These can be tricky - try `ApiLogicServer examples`, or, when all else fails, [try the docs](https://apilogicserver.github.io/Docs/Database-Connectivity/).

</details new projects>

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


</details automated creation>

&nbsp;

</details 2. JSON_API>

&nbsp;

&nbsp;

---

&nbsp;
&nbsp;

<details markdown>

&nbsp;

<summary>Appendix: What is API Logic Server</summary>


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

<details markdown Key technology>

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