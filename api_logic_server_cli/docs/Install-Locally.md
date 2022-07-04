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