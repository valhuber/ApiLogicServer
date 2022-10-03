A critical part of enabling API Logic Server automation is providing for Primary and Foreign Keys.  

## Primary Keys

These are expected to defined in the database.  They are required for updates, and for the Admin App.

&nbsp;

### Infer Primary Key

In some (discouraged) cases, your schema might not declare a primary key, but designate a specific column as `unique`.  The `infer_unqiue_keys` option is provided to address such cases.

&nbsp;

## Foreign Keys

These are also expected to be defined in the database.  They are required for a large set of automation, including:

* Multi-table APIs

* Multi-table forms, including Automatic Joins

* Multi-Table logic (such as sums, counts, parent references, and copy)

If these are missing in the schema, you can provide them in the SQLAlchemy models, as illustrated in [the sample project](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype_nw/database/customize_models.py).