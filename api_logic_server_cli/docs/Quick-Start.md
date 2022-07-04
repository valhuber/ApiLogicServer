This page shows how to create the sample API Logic Server project.  These procedures presume that you have  [Installed](../Quick-Start#Install-Guide) API Logic Server.  Instructions are provided for command line, and for using IDEs such as VS Code and PyCharm.pip install -r requirements.txt   


# Overview
The video below illustrates using this stack to create, execute and customize the [default project](Database).  The blue box below shows the API Logic Server installed in a Docker container.  This contains:
* APiLogicServer, consisting of
  * The CLI (Command Language Interface) used below
  * The API Logic Server runtime (SAFRS, Logic Bank, Flask, SQLAlchemy etc)
* The Python environment (compiler, `pip`, etc)

For a local install, these exact same elements are made available in your `venv` after your `pip install ApiLogicServer.`

[![Using VS Code](https://github.com/valhuber/apilogicserver/wiki/images/creates-and-runs-video-vsc.png?raw=true?raw=true)](https://youtu.be/5nYVNJTfWbs "Using VS Code with the ApiLogicServer container")

The sections below further describe details of this process.

# Install Guide

You can install API Logic Server locally using `pip`, using Docker, or pythonanywhere (a cloud service).

  > While `pip` is a simple install, it requires a Python environment, which is _not_ so simple.  We therefore recommend you consider Docker - it's a simpler install, and aligns you with a likely deployment environment.

&nbsp;

Open the appropriate section below.

<details>

  <summary>Docker Install</summary>
&nbsp;
As described in the [readme](https://github.com/valhuber/ApiLogicServer/blob/main/README.md):

```bash
cd ApiLogicServer      # a directory of projects on local host

# Start (install if required) the API Logic Server docker container...

docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server
```

This will start a command line in the Docker container.
You are now able to issue commands like `ApiLogicServer create` as described in the readme.

The `api_logic_server` image supports startup arguments so you can control the `api_logic_server` container, by running a startup script or by supplying environment variables.  You might, for example, have automated test procedures that load projects from `GitHub` and run tests.

For more information, see [Working With Docker](../Working-With-Docker).

&nbsp;

### Next Steps

Create, start and debug the sample project as described below in [Project Creation](#Project-Creation).

&nbsp;

</details>


<details>
  <summary>Local Install</summary>
&nbsp;
API Logic Server requires Python 3.8 or higher, since it relies on `from future import annotations`.

The first section below verifies whether your Python environment is current.  

The following section explains how to install a current Python environment.

### Verify Pre-reqs: Python 3.8+, pip3

Ensure you have these pre-reqs:

```bash
python --version
python -m venv --help    # creates a venv
python -m pip --version  # install from PyPi
```

  > Note: you may need to use `python3` instead of `python`.  You can customize this as described in the [Troubleshooting Guide](../Troubleshooting#python-issues).

&nbsp;

### Install Python (if required)

If you are missing any, install them as described here.  Skip this step if your pre-reqs are fine.  To install Python:

* On Windows - run the windows installer - be sure to specify "add Python to Path"

* On Mac/Linux - your OS may provide installer options.
  
  * For example, Ubuntu provides the *Software Update* utility.  

  * Mac users can use the [standard installer](https://www.python.org/downloads/); follow the recommendations to install certificates and update your shell.

    > Installing Python on the Mac can be... _dramatic._  Consult the [Troubleshooting Guide](../Troubleshooting#python-issues).

  * Alternatively, many prefer [using homebrew](https://brew.sh/), as described [here](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)

&nbsp;

### Install API Logic Server in a virtual environment

Then, install API Logic Server in the usual manner:

```bash
cd ApiLogicServer          # directory of your choice
python3 -m venv venv       # may require python -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
pip install ApiLogicServer # you may need to use pip3
```

&nbsp;

### SqlServer - install `pyodbc`

This is included in Docker, but not for local installs.  To install `pyodbc` (either global to your machine, or within a `venv`):

* Linux

```bash
apt install unixodbc-dev   # Linux only
pip install pyodbc
```

* Mac - using [brew](https://brew.sh/):

Install the [Microsoft ODBC driver](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16), then:

```bash
# may be required - brew install unixodbc      # Mac only
pip install pyodbc
```

Please see the examples on the [testing](../Testing#northwind---sqlserver--docker) for important considerations in specifying SQLAlchemy URIs.

&nbsp;

### Next Steps

Create, start and debug the sample project - see the [Quick Start](#Quick-Start).

&nbsp;

</details>

<details>
  <summary>Pythonanywhere Install</summary>

You can create an ApiLogicServer on [PythonAnywhere](http://pythonanywhere.com) for any cloud-accessible database.  Open a bash console, and:

```bash  
python3 -m venv venv  # ensures that Python3 is used  
source venv/bin/activate

python3 -m pip install ApiLogicServer

ApiLogicServer create --host=ApiLogicServer.pythonanywhere.com --port=   # ApiLogicServer == your account  
```

__1. Create Application__

Here is an example using a pythonanywhere-hosted MySQL database (__note__ the escape character for the $ in the database name:  
```  
ApiLogicServer create --project_name=Chinook \
--host=ApiLogicServer.pythonanywhere.com --port= \
--db_url=mysql+pymysql://ApiLogicServer:***@ApiLogicServer.mysql.pythonanywhere-services.com/ApiLogicServer\$Chinook
```

__2. Create and configure a web app__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/python-anywhere.png?raw=true"></figure>

__3. Update the wsgi__
And copy the contents of ```/home/ApiLogicServer/api_logic_server/python_anywhere_wsgi.py``` over the wsgi file created by pythonanywhere.

__4. Update the Admin App `api_root`__
The first few lines of the Admin.yaml and Admin Config page should be (update the last line:
```
about:
  date: December 26, 2021 09:00:00
  recent_changes: altered tab captions
  version: 3.50.51
api_root: https://apilogicserver.pythonanywhere.com/api
```

__5. Verify `admin.yanl`__
Verify that the `ui/admin.yaml` ends with something like this:

```bash
settings:
  HomeJS: https://apilogicserver.pythonanywhere.com/admin-app/home.js
  max_list_columns: 8
```

__6. Restart the Web App__
You start ApiLogicServer from the web console, *not* from the command line

__6. Run the application__

You can open the Admin App in your browser [http://apilogicserver.pythonanywhere.com/admin-app/index.html](http://apilogicserver.pythonanywhere.com/admin-app/index.html).


You can use ```curl```:  
```  
curl -X GET "http://ApiLogicServer.pythonanywhere.com/api/employees/?include=office%2Cparent%2CEmployeeList%2CCustomerList&fields%5BEmployee%5D=employeeNumber%2ClastName%2CfirstName%2Cextension%2Cemail%2CofficeCode%2CreportsTo%2CjobTitle&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=employeeNumber%2ClastName%2CfirstName%2Cextension%2Cemail%2CofficeCode%2CreportsTo%2CjobTitle%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"  
```

</details>

&nbsp;&nbsp;

## Tools - IDE, git etc

An IDE is recommended but optional - any will do (I've used [PyCharm](https://www.jetbrains.com/pycharm/download) and [VSCode](https://code.visualstudio.com), install notes [here](https://github.com/valhuber/fab-quick-start/wiki/IDE-Setup)), though different install / generate / run instructions apply for running programs.

API Logic Projects also work with `git`, or your perferred source control system.

&nbsp;&nbsp;

# Project Creation

Use this procedure __for Docker installs:__

```
cd ApiLogicServer  # directory of API Logic Server projects on local host

# Start (install if required) the API Logic Server docker container

docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

$ ApiLogicServer create --project_name=/localhost/ApiLogicProject --db_url=
```

The procedure is similar __for local installs:__
```
cd ApiLogicServer          # your install folder
source venv/bin/activate   # windows venv\Scripts\activate
ApiLogicServer create      # accept default project name, db
```

In either case, the `create` command builds an `ApiLogicProject` - a directory, shown here in VSCode:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png?raw=true"></figure>

  > The procedures above will create the sample project, which we recommend to start with.  You will then want to create a project with your own database.  For that, you will require a [SQLAlchemy URI](https://docs.sqlalchemy.org/en/14/core/engines.html).  You can see some examples:

```bash
ApiLogicServer examples   # prints a list of url examples
```

</details>
  
&nbsp;

# Project Execution 

Select your desired configuration below, and see how to run, customize and debug your ApiLogicProject.

  > Note: as of release 5.02.10, projects are created with a `venv_setup` directory which may be helpful in establishing and verifying your Python environment.  For more information, see the [Trouble Shooting Guide](../Troubleshooting#ide-issues).

<details>
  <summary>Command Line</summary>
  
&nbsp;&nbsp;  

While you will probably want to run it from your IDE (see next section), you can also run from the command line as described below.

__1. Start the Server__
The `api_logic_server_run.py` file is executable.  The simplest way to run it is:
```
ApiLogicServer run        # in Docker Terminal, or with venv active
```

__2. Open in your Browser__
The server should start, and suggest the URL for your Browser.  That will open a page like this where you can explore your data using the automatically created [Admin app](../Working-with-the-Admin-App), and explore the API with automatically generated Swagger:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/admin-home.png?raw=true"></figure>
</details>

<details>
  <summary>VS Code - local install</summary>

&nbsp;&nbsp; 

__1. Create your project__

```
cd ApiLogicServer          # your install folder
source venv/bin/activate   # windows venv\Scripts\activate

ApiLogicServer create   # Return to accept default project name, db

```

__2. Open your project with VS Code__

You can open the IDE yourself, or from the command line:

```
cd ApiLogicServer

# start VS Code either as an application, or via the command line
#    .. macOS users may require: https://code.visualstudio.com/docs/setup/mac

code ApiLogicProject  # using command line to open VS Code on project
```


__3. Remote Container - Decline__
Decline the option above to use the remote-container.   You can prevent this by deleting the `.devcontainer` folder.


__4. Create Virtual Environment__
You then create your virtual environment, activate it, and install the  ApiLogicServer runtime.  

In VS Code: __Terminal > New Terminal Window__, and...

```
python3 -m venv ./venv            # windows: python -m venv venv
# VS Code will recognize your `venv` and ask whether to establish it as your virtual environment.  Say yes.  
source venv/bin/activate          # windows: venv\Scripts\activate
pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
```

> The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.

For more information, see [Work with Environments](https://code.visualstudio.com/docs/python/environments#_work-with-environments)

__5. Install Python Extension__

You may be prompted for this (recent versions of VSCode might auto-detect language support):

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/4-install-python-extension.png"></figure>


__6. Run the server__
You are ready to run
1. Run/Debug: `ApiLogicServer`

> You may get a message: _"The Python path in your debug configuration is invalid."_  Open View > Command Pallet, type “Python Select Interpreter” and Select your `venv`.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/run-debug.png"></figure>

</details>


<details>
  <summary>VS Code - Docker</summary>

&nbsp;&nbsp;

Integrated Development Environments (IDEs) provide code editing and debugging, as well as many other services.  

The created Docker project is a standard Python project, [fully customizable](https://github.com/valhuber/ApiLogicServer#customize-the-created-project) with your existing IDE and other development tools.

> Significantly, you can utilize the Python environment from the Docker machine, __eliminating the need to install and configure Python__.   These procedures apply to local and Docker-based Python.

Pre-reqs:
* Docker (if elected)
* VS Code 1.61
* [VS Code Shell Command](https://code.visualstudio.com/docs/setup/mac)

The steps below explain how to load, run, verify and debug your projects.
The _load_ step differs depending on whether you are using Docker.


__1. Load your docker project__

Create and load your project like this:

```bash
cd ~/Desktop                # directory of API Logic Server projects on local host

# [Install and] Start the API Logic Server docker container
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

# (Now inside the container)
ApiLogicServer create   # Return to accept default project name, db

exit  # exit container to localhost
```

   > Observe you __exit the Docker container___.  We'll start VSCOde _locally_ below, where it will restart Docker as a Remote Container below.  _Local_ operation means your project files are accessed locally (not via `/localhost`), which enables local file operations such as git.

```bash
# start VS Code either as an application, or via the command line
# macOS users may require: https://code.visualstudio.com/docs/setup/mac
code ApiLogicProject  # loads VS Code; accept container suggestions, and press F5 to run (described below)
```


__2. Remote Container - Accept__

Created projects are configured to support:
* launch configurations for running `ApiLogicServer` and the `Basic Web App`
* Docker-based Python environments, per `.devcontainer`

So, when you open the created project, VS Code recognizes that Docker configuration, and provides an option to **Reopen** the project in a [remote container](https://code.visualstudio.com/docs/remote/containers).  Accept this option.


<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/open-in-container.png"></figure>

__3. Run ApiLogicServer__

Click __Run and debug > Run ApiLogicServer__.

This will start the server, and offer to run the Browser on the Admin app.  For more information, [see here](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#run).

__4. Install Python Extension__

When you run, you may encounter the message below; if so:
1. Click Extensions (as shown)
2. Ensure Python support is installed and enabled

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/docker-install-python-extension.png"></figure>


__ApiLogicServer Container upgrades__

If you update your ApiLogicServer container to a new version, your existing projects may appear to be damaged.  You can fix them easily:

1. Click the Dev Container button (in the lower left)
1. Choose **Rebuild Container**

</details>


<details>
  <summary>Pycharm - local install</summary>

&nbsp;&nbsp;

__1. Create your project__

```
cd ApiLogicServer          # your install folder
source venv/bin/activate   # windows venv\Scripts\activate

ApiLogicServer create   # Return to accept default project name, db

```


__2. Do *not* create the `venv` outside PyCharm__


__3. Open the ApiLogic Project__

__4. Create a new Virtual Environment using PyCharm defaults__

PyCharm will ask you to configure a Python Interpreter.  Do so as shown below.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/PyCharm/PyCharm-create-venv.png"></figure>


__5. `pip` install__

Some versions of Pycharm automatically load your dependencies, others do not.  But it's simple to load them using the terminal window:

```bash
source venv/bin/activate          # windows: venv\Scripts\activate
pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
```

> The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.



__6. Run the pre-configured `run` launch configuration__

Some versions of Pycharm may require that you update the Launch Configuration(s) to use your `venv`.

</details>


<details>
  <summary>Pycharm - PRO required for Docker</summary>
  
&nbsp;&nbsp;

__1. Configure Python Interpreter using Docker__
See [these instructions for PyCharm](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html); you should be able to configure a Python interpreter like this:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/docker-python.png"></figure>

__2. Run the pre-configured launch configuration__

You can use this to run the created project:
1. Try to run the `api_logic_server_run.py` (right mouse click).

It won't run, but does create a launch configuration...
1. Edit the created launch configuration, as follows:
1. Specify the `Parameters`
1. Specify the `Docker container settings`

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/run-parameters.png"></figure>

</details>

&nbsp;

# Next Step - Tutorial

The sample project contains a `readme`, which is a Tutorial.  It will walk you through running, customizing and debugging the project.

You can also view the [Tutorial on git](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#api-logic-server---sample-tutorial).

# Verify - run cURL, Swagger, Debugger
Be sure to verify that Swagger can perform a `get`; VSCode will offer to run the Browser for you (you can also run [http://localhost:5656/](http://localhost:5656/)):

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/5-run-swagger.png"></figure>

The sample database provides an excellent opportunity to study key elements of ApiLogicServer:
* The customizable project is open in VSCode, editing `declare_logic.py`, which illustrates how [5 rules can replace 200 lines of code](https://github.com/valhuber/LogicBank/wiki/by-code)
* Create logic using IDE services such as code completion
* Use IDE services to breakpoints and inspect variables and the log as shown below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/logic-debug.png"></figure>

# Logic Debugging (VS Code)

To illustrate:
1. Set the breakpoints above
2. And then use Swagger (see below) to trigger a transaction that causes the breakpoint above to be hit.  This particular endpoint is a [custom service](#customizing-apilogicprojects)

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/add-order.png"></figure>

3. Inspect your variables, review the log as shown above
    * Indentation illustrates logic chaining, but this is obscured with _word wrap_; you will probably want to use the **Debug Console**, with `"redirectOutput": true` in your **Launch Configuration:**

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/no-line-wrap.png"></figure>

&nbsp;

# Trouble Shooting
See [Trouble Shooting](../Troubleshooting#docker).
