The fastest way to explore API Logic Server - *with __no install__* - is to follow this guide to create, explore and customize a project using Codespaces.

!!! Caution "Requires Codespaces Beta, or in organization with Codespaces enabled"
    There are currently restrictions on Codespaces usage.  It appears these will be [removed in the near future](https://github.com/community/community/discussions/32791){:target="_blank" rel="noopener"}.

<details markdown>

<summary>What is API Logic Server</summary>

&nbsp;
&nbsp;

API Logic Server reads your schema to __create an executable web app project:__ an API and an Admin UI. 

__Customize in standard IDEs__ with Python.

__Unique spreadsheet-like business rules__ for multi-table derivations and constraints - 40X more concise than code.

Follow the steps below to be up and running in about a minute - no install, no configuration.  You can run the created project to explore its functionality, and how to customize it in VSCode.

<details markdown>

<summary>Why Does It Matter: Faster, Simpler, Architectural Quality</summary>

&nbsp;

Automation makes it __faster:__ what used to require weeks or months is now immediate.  Unblock UI Dev, and engage business users - _early_ - instead of investing in a misunderstanding.

Automation makes it __simpler:__ this reduces the risk of architectural errors, e.g., APIs without pagination.

And finally, automation guarantees a base level of __architecture:__ systems will always have APIs (no more logic in UI controllers), logic will be always shared between UIs and APIs, and predictable for maintenance teams.


</details>

</details>

&nbsp;

## 1. Open in Codespaces

Open [this template project](https://github.com/ApiLogicServer/ApiLogicProject) in Codespaces.

<details markdown>

<summary>Show Me How</summary>

&nbsp;

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-on-codespaces.jpg?raw=true"></figure> 

&nbsp;

__1. Use your GitHub account__ - no additional sign-up required

__2. Load the working_software_now project from GitHub__

To access this GitHub project with Codespaces

1. __Open [this page](https://github.com/ApiLogicServer/working_software_now)  _in a new window___, and 
2. Click __Open > Codespaces__ as shown below
3. You will see an empty project.

These instructions will continue in Codespaces.

<details markdown>

&nbsp;

<summary>What Just Happened</summary>


You will now see the template project - open in VSCode, _in the Browser._  But that's just what you _see..._

Behind the scenes, Codespaces has requisitioned a cloud machine, and loaded the template - with a _complete development environment_ - Python, your dependencies, git, etc.  

You are attached to this machine in your Browser, running VSCode.

> :trophy: Pretty remarkable.

</details>

</details>


&nbsp;

## 2. Create a project

Paste this into the Terminal window:

```
ApiLogicServer create --project_name=./ --db_url=
```

<details markdown>

<summary>What Just Happened</summary>

&nbsp;

This is **not** a coded application.

The system examined your database (here, the default), and __created an _executable project:___

* __API__ - an endpoint for each table, with full CRUD services, filtering, sorting, pagination and related data access

* __Admin UI__ - multi-page / multi-table apps, with page navigations and automatic joins

__Projects are Customizable, using _your IDE_:__ the Project Explorer shows the project structure.  Use the code editor to customize your project, and the debugger to debug it.

__Business Logic is Automated:__ use unique spreadsheet-like rules to declare multi-table derivations and constraints - 40X more concise than code.  Extend logic with Python.


<details markdown>

<summary>Using your own database</summary>

&nbsp;

In this case, we used a default Customers/Orders database.  To use your own database, provide the `db_url` [like this](../Database-Connectivity/).

</details>
</details>

&nbsp;

## 3. Start Server, Admin App

The project is ready to run:

1. Use the default __Run Configuration__ to start the server, and 

2. Click __Ports > Globe__ to start the web app. 

<details markdown>

&nbsp;

<summary>Show Me How</summary>

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port-launch-simple.jpg?raw=true"></figure>

</details>

&nbsp;

## 4. Explore the Tutorial

[Open the Tutorial](Tutorial.md) to explore the sample project.

<details markdown>

&nbsp;

<summary>Tutorial Overview</summary>

The Tutorial will enable you to explore 2 key aspects:

* __Initial Automation__ - API and UI creation are automated from the data model. So, later, you'd see this level of automation for your own databases.

* __Customization and Debugging__ - this sample also includes customizations for extending the API and declaring logic, and how to use VSCode to debug these.  The Tutorial will clearly identify such pre-built customizations.

</details>

&nbsp;

Extensive [product documentation is available here](https://valhuber.github.io/ApiLogicServer/) - checkout the [FAQs](https://valhuber.github.io/ApiLogicServer/FAQ-Frameworks/).

&nbsp;

# API Logic Server Background

### Motivation

We looked at approaches for building database systems:  

<br/>

__Frameworks__

Frameworks like Flask or Django enable you to build a single endpoint or _Hello World_ page, but a __multi-endpoint__ API and __multi-page__ application would take __weeks__ or more.

<br/>

__Low Code Tools__

These are great for building great UIs, but

* Want a multi-page app -- __without requiring detail layout for each screen__
* Want to __preserve standard dev tools__ - VSCode, PyCharm, git, etc
* Need an answer for __backend logic__ (it's nearly half the effort)

&nbsp;

### Our Approach: Instant, Standards-based Customization, Logic Automation

API Logic Server is an open source Python project.  It runs as a standard Python (`pip`) install, or under Docker. It consists of:

* a set of runtimes (api, user interface, data access) for project execution, plus 

* a CLI (Command Language Interface) to create executable projects with a single command

Then,

* Customize your projects in standard IDEs such as VSCode or PyCharm

* Declare multi-table derivation and constraint logic using spreadsheet-like rules

    * :trophy: 40X more concise than code
    * Extend with Python


> :bulb: API Logic Server reads your schema, and creates an executable, customizable project.

&nbsp;

