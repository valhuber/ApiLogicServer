The fastest way to explore API Logic Server - *with __no install__* - is to follow this [Exploration Guide](#exploration-guide) to create, explore and customize a project.

!!! Caution "Codespaces sometimes not authorized"
    While Codespaces is almost always enabled, we have seen some instances where it is not.  We are [researching this](https://github.com/community/community/discussions/32791){:target="_blank" rel="noopener"} with the Codespaces team.

If you are new to API Logic Server, the following section provides a brief overview.

&nbsp;

# Why: Partial Automation, Proprietary IDEs

We saw __shortfalls in current approaches__ for building database systems:

* __Frameworks: too slow -__ _multi-endpoint APIs_ and _multi-page apps_ would require _weeks_ in frameworks such as Flask or Django, since it's all code -- no automation

* __Low Code Tools: no backend automation, proprietary IDEs__ - good UI automation, but none for backend business logic (nearly half the effort), and often do not leverage existing IDEs (VSCode, PyCharm, etc).

&nbsp;

# Instant, Full System Automation, Leverage Existing Tools
So, we created API Logic Server as an __open source__ Python project: a __CLI__ for project creation, and a set of __execution runtimes.__  Install with a standard Python (`pip`) install or Docker.<br/><br/>

## Project Creation is Instant: Single Command
 
&nbsp;&nbsp;&nbsp;&nbsp;
`ApiLogicServer create --project_name=ApiLogicProject --db_url=`<br/><br/>


## Projects are Highly Functional: Admin UI and API
API Logic Server reads your schema, and creates an  __executable__ project:

* __API__ - an endpoint for each table, with filtering, sorting, pagination and related data access

* __Admin UI__ - multi-page / multi-table apps, with page navigations and automatic joins<br/><br/>

## Projects are Customizable: Using _Your_ IDE

Customize projects in __your IDE__ (VSCode, PyCharm, etc.) for edit, debug and code management.<br/> <br/>


## Business Logic is Automated: Unique Rules :trophy: 

Declare business logic with spreadsheet-like rules (40x more concise than code), extensible with Python.

&nbsp;

# Exploration Guide

Use these instructions to run API Logic Server in the cloud (courtesy Codespaces) - create a project, run it, and customize it using VSCode.

&nbsp;

## Open in Codespaces

Explore API Logic Server running under CodeSpaces as follows.

__1. Use your GitHub account__ - no additional sign-up required

__2. Load this project from GitHub, and create the Sample__

To load this GitHub project with Codespaces:

&nbsp; &nbsp; &nbsp; a. [Open this page in a ___new window___](https://github.com/ApiLogicServer/ApiLogicProject), and 

&nbsp; &nbsp; &nbsp; b. Click __Code > Codespaces__ as shown below
   <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-on-codespaces.jpg?raw=true"></figure> 

&nbsp; &nbsp; &nbsp; __c. You will see an empty project - running in VSCode, _in the Browser_.__   
   > But that's just what you _see..._ <br/><br/>
   > Behind the scenes, Codespaces has requisitioned a cloud machine, and loaded your project - with a _complete development environment_ - Python, your dependencies, git, etc.<br/>  
   > You are attached to this machine in your Browser, running VSCode.<br/><br/>
   > :trophy: Pretty remarkable.<br/><br/>

&nbsp; &nbsp; &nbsp; __d. Create the Sample__

To create the sample, paste the following into the terminal window:<br/>

```
ApiLogicServer create --project_name=./ --db_url=
```

where:

   * `project_name` is specified to be the current directory (normally a new directory)

   * `db_url` is specified as the sample (normally a SQLAlchemy URI to your own database)<br/><br/>

__3. Add and Configure a Port__

Referring to the figure below (steps 3-5), click the __Ports__ tab, and:

* Add the Port (5656)
* Make the port __public__ (use right-click to alter the Visibility)

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port-launch-simple.jpg?raw=true"></figure>
<br/>

__4. Start the Server__

* Click __Run/Debug__ on the left toolbar
* Use the pre-defined Launch Configuration - click the green __run__ button<br/><br/>

__5. Start the Browser__

* Click the globe (on the Ports tab), as shown below.  This should start your Browser, and the links on the left (Customer etc) should return data.

<details markdown>
<summary>If errors, use this procedure</summary>

The above procedure is simplified, based on some assumptions about Codespaces.  If the Browser fails to launch, try the following for explicit specification of the forwarded port:

__4. Configure the pre-created `Codespaces-ApiLogicServer` launch configuration__ (see above)

__5. Start the Server__ using the provided Launch Configuration = `Codespaces-ApiLogicServer`

__6. Open the Browser__

Click the globe, as shown above.  This should start your Browser, and the links on the left (Customer etc) should return data.

</details>

&nbsp;

## Run the Tutorial

The Tutorial will enable you to explore 2 key aspects:

* __Initial Automation__ - API and UI creation are automated from the data model. So, later, you'd see this level of automation for your own databases.

* __Customization and Debugging__ - this sample also includes customizations for extending the API and declaring logic, and how to use VSCode to debug these.  The Tutorial will clearly identify such pre-built customizations.

Now, [open the Tutorial](Tutorial.md).
