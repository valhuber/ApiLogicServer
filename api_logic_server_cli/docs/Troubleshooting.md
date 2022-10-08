Please report bugs as [GitHub Issues](https://github.com/valhuber/ApiLogicServer/issues).

# Project Failed to Start (March, 2022)

Recent updates to included libs have broken previous versions of API Logic Server.  This is fixed in a new version (5.00.06) is now available, and recommended.

If you are unable to upgrade to the new version, you can repair your existing install like this (your venv should be active):

```
pip install MarkupSafe==1.1.1
pip install Jinja2==2.11.2
```

&nbsp;&nbsp;

# Install Failures

## `pyodbc` fails to install

For API Logic Server releases 5.02.16 and earlier, installation may fail with issues such as:

```log
sql.h not found - your console log might include:
...
    src/pyodbc.h:56:10: fatal error: 'sql.h' file not found
```

Resolve these as explained in the [Quick Start](../Quick-Start#sqlserver---install-pyodbc).


## Unsupported Architecture - MacOS

You may experience alarming messages when you `pip install` API Logic Server.  These can occur installing `pyodbc`, and can occur when installing API Logic Server, or creating `venv` for created API Logic Projects.  We've seen the following:

```log
  × Running setup.py install for pyodbc did not run successfully.
      /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/cdefs.h:807:2: error: Unsupported architecture
      #error Unsupported architecture
```

Resolve this by adding this to your `~/.zprofile`:

```bash
PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:${PATH}"
export PATH
export ARCHFLAGS="-arch x86_64"  # <=== enable this line
```

&nbsp;&nbsp;

# Initial Project Creation

Project Creation involves 2 steps that can cause errors, described in the following sub-sections.

## Database failed to open
The `db_url` argument is a [SQLAlchemy database uri](https://docs.sqlalchemy.org/en/14/core/engines.html).  Please find several examples we use in our [testing](../Testing).

### Check Connectivity using SQL Tools
A typical cause is lack of connectivity to the database.  Use your local database tools to verify connectivity from your machine to the database.

## Dynamic model import failed

After the database is opened, it is introspected to build `database/models.py`, classes used by SQLAlchemy and the API for database access.  The models file may fail to compile, often due to unexpected names.

Watch for entries like this in the console log:

```
6. Create api/expose_api_models.py and ui/basic_web_app/app/views.py (import / iterate models)
.. ..Dynamic model import using sys.path: /Users/val/dev/servers/sqlserver-types/database

===> ERROR - Dynamic model import failed

===> ERROR - Unable to introspect model classes
.. Using db for meta (models not found)
.. See ../Troubleshooting#manual-model-repair
.. ..WARNING - no relationships detected - add them to your database or model
.. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design
```

You may also encounter errors when the system attempts to start the server, due to invalid model files.
These may look like this:

```
Run created ApiLogicServer with command: python /Users/val/dev/servers/sqlserver-types/api_logic_server_run.py localhost
Traceback (most recent call last):
  File "/Users/val/dev/ApiLogicServer/api_logic_server_cli/cli.py", line 253, in find_meta_data
```

### Repair the model, and `rebuild_from_model`

The system will log errors and attempt to proceed with project creation.  You can then:

1. Open the project in your IDE, and manually correct the ```models.py``` file
   * E.g., specify proper class names
2. Rerun ```ApiLogicServer```, specifying the ```rebuild_from_model``` parameter, like this:
```
ApiLogicServer rebuild-from-model\
--project_name=~/dev/servers/sqlserver-types\
--db_url=mssql+pyodbc://sa:Posey3861@localhost:1433/SampleDB?\driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no
```
3. You will most likely want to activate the api and app files:
   * `api/expose_api_models_created.py` - this file is not used in actual operation, but provided so you can merge or copy it over `api/expose_api_models.py`
   * `ui/admin/admin-created.yaml` - this file is not used in actual operation, but provided so you can merge or copy it over `ui/admin/admin.yaml`

For more on rebuild, see [Rebuilding](https://github.com/valhuber/ApiLogicServer/wiki#rebuilding).

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/model/model-repair-rebuild.png?raw=true"></figure>

&nbsp;&nbsp;

# Docker

Docker can dramatically simplify installation, but be aware of the topics described in the sub-sections below:

## Docker on Windows

Docker requires **Windows Pro** for a [native install, using hyper-v](https://docs.docker.com/desktop/windows/install/).  If Docker Desktop fails to start, check [these instructions](https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package).

If you have **Windows Home**, be aware it's not supported, but some [brave souls have found ways](https://medium.com/@mbyfieldcameron/docker-on-windows-10-home-edition-c186c538dff3).

Docker sometimes fails with multi-level virtualization, such as running Mac > Windows on Fusion.

## VS Code with Docker - unable to open file, unable to read file

Under circumstances still unclear, your container may be unable to locate internal files.  
Port conflicts can cause re-assignments that need corrections.

These are easy to resolve as [explained here](https://stackoverflow.com/questions/60472084/vscode-unable-to-open-file-unable-to-read-file-message-when-clicking-on-an/69396657#69396657).


## VS Code - damaged container

You may need to rebuild your container, as [described here](https://stackoverflow.com/questions/60472084/vscode-unable-to-open-file-unable-to-read-file-message-when-clicking-on-an/69396657#69396657).

## VS code - damaged port settings

You may encounter unexpected port changes, such as using `localhost:5657` instead of the usual `localhost:5656`.  Resolve this as shown below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/fix-vscode-ports.png?raw=true"></figure>

# IDE Issues

## Code Completion fails

Code completion depends on a properly installed `venv`.  The digram below shows how code completion exposes valuable services provided by `logic_row`, and how to verify your `venv` setting for VSCode:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/venv.png?raw=true"></figure>


## `venv` Setup

`venv` setup is automatic for Docker installs.  For local installs, we have seen the issues below.

### PyCharm

In some installations, PyCharm may fail when your `venv` is pre-created.  I have found it best to let PyCharm create the `venv`.

## VSCode fails to discover `venv`

In most cases, VSCode discovers `venv` environments, whether created prior to launching VSCode, or created inside the newly created project.

However, this process occasionally fails.  For example, if you create the project successfully, then delete and recreate it, VSCode may not discover your `venv`.  This is usually resolved by:
1. Create the `venv` as described in the [Quick Start](../Quick-Start#project-execution)
2. Exit / restart VSCode
3. Use __View > Command Palette > Python: Select Interpreter__, and select the entry `"venv”: venv`.  See the diagram below.

It's a good idea to verify your `venv`, as described in the next section.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/select-venv.png?raw=true"></figure>

## Verify your Python environment

As of release 5.02.10, you can run `venv_setup/py.py sys-info`, either
* Using Command Line Python, or
* In VSCode, select the file and use the Launch Configuration __Python: Current File__.
   * Note: this may properly update the Python `venv` information if it was not properly set

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/py-py.png?raw=true"></figure>

&nbsp;&nbsp;

# Database Issues

## Docker API Logic Server connecting to dockerized databases
Even when you can access the database to create the project, your dockerized project may fail to connect.  This is often caused by not enabling your project for network access.  For more information, see [connectivity](../Testing#connecting).


## MySQL

You may need to install special packages, e.g.
```
pip install pymysql 
pip install cryptography
```

## SQL Server - requires `pyodbc'

SqlServer requires the `pyodbc` package.  You can't just `pip install` it.  Attempting to do so will cause errors such as:

```log
sql.h not found - your console log might include:
...
    src/pyodbc.h:56:10: fatal error: 'sql.h' file not found
```

Resolve these as explained in the [Quick Start](../Quick-Start#sqlserver---install-pyodbc).

&nbsp;&nbsp;

# Python Issues

## MacOS Installs

Such installs can be daunting:
* __Which installer:__ Python.org installer, or brew?
* __Additional utlities required:__ Rely on additional tooling, such as `pyenv` or `venv`?
* __Install history:__ is the Mac default Python (2) installed?  Are there prior installs, using one or both of the methods above
* __`pyodbc`__ is particularly challenging

#### Choose simple case
With so many variables, I have researched the simplest possible scenario:
* Clean Monterey install (no existing Python)
* Using `zsh` (not `bash`)
* Use _(only)_ the [Python.org installer](https://www.python.org/downloads/macos/)

#### 1. Basic install - with Command Line Tools
Run the installer, including certificates and updates to your shell. 

Python operations (such as `pip install`) often require command line tools (`c` compiler, etc).  You have 2 ways to get these:

1. Basic command line tools: you have 2 options:

   1. As [described here](https://www.freecodecamp.org/news/install-xcode-command-line-tools/)
   2. Or, many installs (including API Logic Server) will recommend this with a popup dialog (for example, see [this article](https://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/)) - do so unless you require `xcode`...

2. Installation of `xcode` from the Apple App Store (`xcode` install takes a _long_ time -- like, all day)

Next, verify the items below.

#### 2. Verify `python3` runs
This enables not only python, but provides access to required utilities:

```bash
python3 --version
python3 -m venv --help    # creates a venv
python3 -m pip --version  # install from PyPi
```

#### 3. Optionally, enable `python` as default

The basic install requires you use `python3` and `pip3`, as shown above.  This can affect command scripts, and is a bit clumsy.  You can make `python` and `pip` work, by altering these 2 files:

My `~/.zshrc`:

```bash
alias python=/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

setopt interactive_comments
PATH=~/.local/bin:$PATH
# python ~/py.py # discussed below
```

My `~/.zprofile`:

```bash
PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:${PATH}"
export PATH
# export ARCHFLAGS="-arch x86_64"  
```

#### 4. Verify your Python environment

With all these moving parts, I found it necessary to verify my environment every time I start the terminal:

1. Obtain `py.py` from your API Logic Server install - create a project, and copy `venv_setup/py.py` to your home folder

2. Enable the commented out line in `~/.zshrc`

&nbsp; &nbsp;

## Certificate Failures

You may see this in the console log when running ```ApiLogicServer run```:

```log
1. Create ui/basic_web_app with command: flask fab create-app --name /Users/me/Documents/Development/ApiLogicServer/api_logic_server/ui/basic_web_app --engine SQLAlchemy
result: Something went wrong <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)>\nTry downloading from https://github.com/dpgaspar/Flask-AppBuilder-Skeleton/archive/master.zip
```

This may be due to a certificate issue.  The `python.org` installer includes a script for this, or [try this](https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error), or [like this](https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org).
