This page lists some of the databases we have tested, including various (Mac-oriented) configuration notes.

If you are using (recommended) docker for API Logic Server, start the docker machine like this (Windows users - use Powershell):

```
cd ~/dev/servers  # project directories will be created here
docker network create dev-network  # only required once
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 --net dev-network -v ${PWD}:/localhost apilogicserver/api_logic_server
```

&nbsp;

# Northwind - sqlite (default sample)

See [Sample Database](Sample-Database).

This is a sqlite database, packaged with API Logic Server, so you can explore without any installs.  It is obtained from [Northwind](https://github.com/jpwhite3/northwind-SQLite3), and altered to include several columns to demonstrate rules.

Run under API Logic Server docker:
```
ApiLogicServer run --project_name=/localhost/docker_project
```

You can use an existing sqlite database like this:
```
ApiLogicServer create --project_name=Allocation --db_url=sqlite:////Users/val/Desktop/database.sqlite
```

&nbsp;

# Docker Databases

Docker is a wonderful way to get known databases for your project, without database installs.  The docker databases below were created for use with API Logic Server, but you may find them generally useful.

&nbsp;

## Connecting

If you are running API Logic Server in a container, and accessing dockerized databases, you will need to enable connectivity by uncommenting the indicated line in the diagram below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/databases/docker-db-access.png"></figure>

The diagram above, and the examples below, presume you have created a docker network called `dev-network`, as shown at the top of this page.

&nbsp;

## classicmodels - MySQL / Docker

Docker below built from [MySQL Tutorials](https://www.mysqltutorial.org/mysql-sample-database.aspx/) - Customers, Orders...

```
docker run --name mysql-container --net dev-network -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=p apilogicserver/mysql8.0:version1.0.7
```

Then access using Docker:
```
ApiLogicServer create --project_name=/localhost/classicmodels --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels
```

&nbsp;

### Using VSCode sqltools
If you are using VSCode, you may wish to use tools to query your database.  A useful resource is [this video](https://www.youtube.com/watch?v=wzdCpJY6Y4c&ab_channel=BoostMyTool), which illustrates using *SQLTools*, a VSCode extension.  Connecting to Docker databases has proven difficult for many, but this video shows that the solution is to create a *native* user:
```
Create new MySQL user with old authentication method:
CREATE USER 'sqluser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'sqluser'@'%';
FLUSH PRIVILEGES;
```

&nbsp;

### Additional MySQL databases
These databases are also provided in the MySQL docker loaded above.

Note: these databases do not have Flask AppBuilder Admin data; to run Flask AppBuilder, you must [add admin data like this](Working-with-Flask-AppBuilder).

&nbsp;

#### Sakila - MySQL / Docker

Obtained from [Sakila](https://github.com/LintangWisesa/Sakila_MySQL_Example) - Actors and Films.

Installed in Docker per [these instructions](https://medium.com/@crmcmullen/how-to-run-mysql-in-a-docker-container-on-macos-with-persistent-local-data-58b89aec496a).

```
ApiLogicServer create --project_name=/localhost/sakila --db_url=mysql+pymysql://root:p@mysql-container/sakila
```

&nbsp;

#### Chinook - MySql / Docker

Obtained from [Chinook](https://github.com/lerocha/chinook-database) - Artists and Tracks.

```
ApiLogicServer create --project_name=/localhost/chinook --db_url=mysql+pymysql://root:p@mysql-container/Chinook
```

&nbsp;

## Northwind - Postgres / Docker

Obtained from [pthom at git](https://github.com/pthom/northwind_psql).

Installed in Docker per [these instructions](https://dev.to/shree_j/how-to-install-and-run-psql-using-docker-41j2).

```
docker run -d --name postgresql-container --net dev-network -p 5432:5432 -e PGDATA=/pgdata -e POSTGRES_PASSWORD=p apilogicserver/postgres:version1.0.2
```

Run under API Logic Server docker:
```
ApiLogicServer create --project_name=/localhost/postgres --db_url=postgresql://postgres:p@postgresql-container/postgres
```

> It may be necessary to replace the docker container name with your IP address, e.g., --db_url=postgresql://postgres:p@10.0.0.236/postgres

Docker pgadmin:
```
docker run --name pgadmin -p 5050:5050 thajeztah/pgadmin4
```

JDBC (for tools): `postgresql://postgres:p@10.0.0.234/postgres`

Also note the datatype ```bpchar``` (blank-padded char) results in several evidently benign messages like:
```
packages/sqlalchemy/dialects/postgresql/base.py:3185: SAWarning: Did not recognize type 'bpchar' of column 'customer_id'
```

&nbsp;

## Northwind - SqlServer / Docker

Start SQL Server:

```
docker run --name sqlsvr-container --net dev-network -p 1433:1433 -d apilogicserver/sqlsvr:version1.0.0
```

Then, under API Logic Server, Docker installed:
```
ApiLogicServer create --project_name=/localhost/sqlserver --db_url=mssql+pyodbc://sa:posey386\!@sqlsvr-container:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server\&trusted_connection=no
```

You will probably also want to get [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15), and configure a connection like this (password: posey386!):

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/databases/sqlsvr-conn.png"></figure>

### SqlServer SQLAlchemy URIs

Important considerations for SQLAlchemy URIs:

* The example above runs on a mac

* It depends on the version of ODBC Driver; for example, a more recent version is:

```
  mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no
```

* Observe the additional parameter for encryption ([see here](https://stackoverflow.com/questions/71587239/operationalerror-when-trying-to-connect-to-sql-server-database-using-pyodbc))

* On Linux (and inside docker), the URI is:

```bash
--db_url='mssql+pyodbc://sa:posey386!@sqlsvr-container:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'
```

&nbsp;

# Accessing Docker databases from `pip` install

You can also use the `pip` install version.  Differences to note:
* the `/localhost` path is typically not required
* the server host address is `localhost`
* Note related in install procedure, the SqlServer example illustrates you can single-quote the url, instead of using the `\` escapes

```
ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no'

ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'

ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres
```

&nbsp;

# Managing Database in your IDE

Various IDEs provide tools for managing databases.

&nbsp;

## PyCharm Database Tools

Pycharm provides [database tools](https://www.jetbrains.com/help/pycharm/2021.3/database-tool-window.html), as shown below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/PyCharm/database-tools.png"></figure>

&nbsp;

# VSCode Database Tools

I use [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools).  To use it, you must first install drivers:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/SQLTools/SQLTools-drivers.png"></figure>

Then, you can explore the sample:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/SQLTools/SQLTools-sample.png"></figure>

&nbsp;
