If your project needs to connect to multiple physical database, you can configure this as [illustrated in this example](https://github.com/valhuber/MultiDB){:target="_blank" rel="noopener"}.

A [pre-release is available](../#preview-version){:target="_blank" rel="noopener"}, providing automation for adding databases to existing projects:

```bash
cd YouApiLogicProject
ApiLogicServer add-db --db-url=todo --bind_key=Todo
```

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/model/multi-db.png?raw=true"></figure>

It operates as follows:

1. Model files are created (prefixed by you `bind-key`) for each table in your `db-url`.
    * Note the 'bind-key` is inserted into the table class
    * Note: Sqlite databases are copied to your database folder, simplifying source control
2. The `config.py` file is altered per your `db-url`
    * Note the shorthand for sqlite versions of `todo`, `classicmodels`, `chinook`.  These are included in the install.
3. The `bind_databases.py` file is created to bind the table to the database via its `bind-key`

&nbsp;

## API support

Tables in your new databases are available through swagger.

&nbsp;

## Admin support

An admin app is built for the table in your new database.  Access it via a url that prefixes the `bind-key`, such as `http://localhost:5656/admin/Todo_admin`.