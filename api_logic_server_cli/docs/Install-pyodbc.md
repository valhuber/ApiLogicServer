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
pip install pyodbc==4.0.34
```

Please see the examples on the [testing](../Database-Connectivity) for important considerations in specifying SQLAlchemy URIs.

&nbsp;

### Limitations - SqlServer Sort fields

Note Sql/Server may not sort on certain fields such as images or long text.  This shows up, for example, in the Docker SqlServer sample database for `Category`.  So, when testing these in Swagger, modify your Sort fields accordingly.

&nbsp;