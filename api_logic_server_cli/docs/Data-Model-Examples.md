To make experimenting easier, several sqlite databases are included in the install.  Use them as described below.

## `db_url` Abbreviations

SQLAlchemy URIs can be fiddly.  For example, the sample database is specified like this:

```
ApiLogicServer create --project_name=Allocation --db_url=sqlite:////Users/val/Desktop/database.sqlite
```

So, API Logic Server supports the following `db_url` shortcuts:

* nw - same as the sample (customers and orders; you can also use an empty `db_url`)
* nw- - same as nw, but no customizations
* chinook - albums and artists
* classicmodels - customers and orders
* auth - authentication data
* todo - a simple 1 table database

&nbsp;

## Creating Sample Projects

You can use the abbreviations to create projects.  For example, create the sample project _without customizations_ to see how API Logic Server would support your own databases:

```
ApiLogicServer create --project_name=nw_no_customizations --db_url=nw-
```

__Notes:__

1. Docker users would typically precede the `project_name` with `localhost/`

2. Codespaces users should specify `project_name` as `./`

