You can install API Logic Server locally using `pip`, using Docker, or pythonanywhere (a cloud service).

  > While `pip` is a simple install, it requires a Python environment, which is _not_ so simple.  We therefore recommend you consider Docker - it's a simpler install, and aligns you with a likely deployment environment.


Open the appropriate section below, and see the [Install Notes](Installation-Notes) at the end.


=== "With Docker"
  
    As described in the [readme](https://github.com/valhuber/ApiLogicServer/blob/main/README.md):

    ```bash
    cd ApiLogicServer      # a directory of projects on local host

    # Start (install if required) the API Logic Server docker container...

    docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server
    ```

    This will start a command line in the Docker container.
    You are now able to issue commands like `ApiLogicServer create` as described in the readme.

    The `api_logic_server` image supports startup arguments so you can control the `api_logic_server` container, by running a startup script or by supplying environment variables.  You might, for example, have automated test procedures that load projects from `GitHub` and run tests.


    > Already installed?  Upgrade to the latest (5.03.10): ```docker pull apilogicserver/api_logic_server``` (you may need to [rebuild your container](https://valhuber.github.io/ApiLogicServer/Execute-VSCode-Docker/)).

    For more information, see [Working With Docker](../Working-With-Docker).



=== "Local Install"

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
=== "PythonAnyWhere"


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


## Installation Notes

### Alert - Project fails to start

Recent updates to included libs have broken previous versions of API Logic Server.  This is fixed in a new version (5.00.06), and is strongly recommended.  You can also repair broken installations as described in [Troubleshooting](../Troubleshooting).

### Heads up - Certificate Issues
We sometimes see Python / Flask AppBuilder Certificate issues - see [Troubleshooting](../Troubleshooting#certificate-failures).

### Default Python version
In some cases, your computer may have multiple Python versions, such as ```python3```.  ```ApiLogicServer run``` relies on the default Python being 3.8 or higher.  You can resolve this by:
* making ```python3``` the default Python, or
* using ```ApiLogicServer create```, and running ```python3 api_logic_server_run.py```

&nbsp; &nbsp;