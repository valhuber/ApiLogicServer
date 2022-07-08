## Customize the Model: add relationships, derived attributes
Model files describe your database tables.  You can extend these, e.g. to __add relationships__, and __add derived attributes__.

> Note: relationships are a particularly critical aspect of the model.  While they normally come from your schema and are discovered during `ApiLogicServer create`, they are often missing from the database.  You can add them as shown below.
  
&nbsp;

### Edit ```models.py```: referential integrity (e.g., sqlite)

[Rebuild support](../Project-Rebuild) enables you to rebuild your project, preserving customizations you have made to the api, logic and app.  You can rebuild from the database, or from the model.

This enables you to edit the model to specify aspects not captured in creating the model from your schema.  For example, sqlite often is not configured to enforce referential integrity.  SQLAlchemy provides  support to fill such gaps.

For example, try to delete the last order for the first customer.  You will encounter an error since the default is to nullify foreign keys, which in this case is not allowed.

You can fix this by altering your ```models.py:```

```
    OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=True, backref='Order')
```

Your api, logic and ui are not (directly) dependent on this setting, so there is no need to rebuild; just restart the server, and the system will properly cascade the `Order` delete to the `OrderDetail` rows.  Note further that logic will automatically adjust any data dependent on these deletions (e.g. adjust sums and counts).

&nbsp;

### Edit ```model_ext.py```: add relationships, derived attributes
In addition, you may wish to edit ```models_ext.py```, for example:

* to define [relationships](https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design), critical for multi-table logic, APIs, and web apps

* to describe derived attributes, so that your API, logic and apps are not limited to the physical data model

&nbsp;

### Use Alembic to update database schema from model

As of release 5.02.03, created API Logic Projects integrate [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) to perform database migrations.

* Manual: create migration scripts by hand, or
* Autogenerate: alter your `database/models.py`, and have alembic create the migration scripts for you

Preconfiguration includes:

* initialized `database/alembic` directory
* configured `database/alembic/env.py` for autogenerations
* configured `database/alembic.ini` for directory structure

See the `readme` in your `database/alembic` for more information.
