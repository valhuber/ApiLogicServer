API Logic Server enables you to create projects that support multiple databases, as follows:

1. Create the project, specifying your "main" database

2. Use the `ApiLogicServer add-db` command for each additional database

    * See the example below

&nbsp;

## Example

SQLAlchemy supports multiple databases by using the `bind_key` which is [supported by Flask](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/binds/){:target="_blank" rel="noopener"}.  It is leveraged in creating Api Logic Projects when you add databases like this:

```bash
cd YourApiLogicProject
ApiLogicServer add-db --db-url=todo --bind_key=Todo
``` 

&nbsp;

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/model/multi-db.png?raw=true"></figure>

Observe:

1. Model files are created (prefixed by your `bind-key`) for each table in your `db-url`.  Note:
    * The `bind-key` is inserted into the table class.
    * Sqlite databases are copied to your database folder, simplifying source control.
    * This example uses the shorthand for sqlite databases: `todo`, `classicmodels`, `chinook` and `nw`.  These are included in the install, so you can experiment with them.
2. The `config.py` file is altered per your `db-url`
    * You can use environment variables to override these assignments, to avoid placing passwords in projects.
3. The `bind_databases.py` file is created to bind the `bind_key` to the database url.   This enables SQLAlchemy to access the proper database.

&nbsp;

## Internals

The example above will result in the following log:

```bash
ApiLogicServer 6.90.08 Creation Log:
1. Not Deleting Existing Project
2. Using Existing Project
.. ..Adding Database [Todo] to existing project
.. .. ..Copying sqlite database to: database/Todo_db.sqlite
.. .. ..From /Users/val/dev/ApiLogicServer/api_logic_server_cli/database/todos.sqlite
.. ..Updating config.py file with SQLALCHEMY_DATABASE_URI_TODO...
.. ..Updating database/bind_databases.py with SQLALCHEMY_DATABASE_URI_TODO...
3. Create/verify database/Todo_models.py, then use that to create api/ and ui/ models
 a.  Create Models - create database/Todo_models.py, using sqlcodegen
.. .. ..For database:  sqlite:////Users/val/dev/servers/ApiLogicProject/database/Todo_db.sqlite
.. .. ..Setting bind_key = Todo
.. .. ..Create resource_list - dynamic import database/Todo_models.py, inspect 2 classes in <project>/database
 b.  Create api/expose_api_models.py from models
 c.  Create ui/admin/admin.yaml from models
.. .. ..WARNING - no relationships detected - add them to your database or model
.. .. ..  See https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design
.. .. ..Write /Users/val/dev/servers/ApiLogicProject/ui/admin/Todo_admin.yaml
 d.  Create ui/basic_web_app -- declined
4. Final project fixup
 b.   Update api_logic_server_run.py with project_name=/Users/val/dev/servers/ApiLogicProject and api_name, host, port
 c.   Fixing api/expose_services - port, host
 d.   Updated customize_api_py with port=5656 and host=localhost
 e.   Updated python_anywhere_wsgi.py with /Users/val/dev/servers/ApiLogicProject
```

Notes:

1. In step 2:
    1. Updating `config.py` file with the location of the new database
    2. Updating `database/bind_databases.py` to open this database for SQLAlchemy access
2. In Step 3:
    1. Creating a `models.py` file; note:
        * The additional superclasses,
        * Inclusion of your designated `bind_key`, for step 1.2
3. Note the shorthand for sqlite versions of `todo`, `classicmodels`, `chinook`.  These are included in the install.

&nbsp;

## Runtime Support

### API support

Tables in your new databases are available through swagger.

&nbsp;

### Admin support

An admin app is built for the table in your new database.  Access it via a url that prefixes the `bind-key`, such as `http://localhost:5656/admin/Todo_admin/` (note the trailing slash).

