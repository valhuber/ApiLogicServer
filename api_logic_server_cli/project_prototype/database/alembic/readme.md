This project integrates [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) to perform database migrations.
* Manual: create migration scripts by hand, or
* Autogenerate: alter your `database/models.py`, and have alembic create the migration scripts for you

This project is preconfigured for alembic migrations:
* initialized `database/alembic` directory
* configured `database/alembic/env.py` for autogenerations
* configured `database/alembic.ini` for directory structure

## Manual
As described in the [Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html):
```
cd database
alembic revision -m "my revision"
```
This will create `database/alembic/versions/xxx_my_revision.py`.
* edit the `upgrade()` and `downgrade()` functions as shown in the Tutorial

Then, to run the script
```
alembic upgrade head
```

## Autogenerate
[Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) can be used to forward engineer an altered `database/models.py` to create migration scripts:
```
cd database

alembic revision --autogenerate -m "Added Tables and Columns"  # used to create version

alembic upgrade head  # runs the version, as above for Manual
```

#### Example - Sample Database

Alter your model by pasting in the following, then follow the procedure above:
```

class CategoryNew(SAFRSBase, Base):
    __tablename__ = 'CategoryNew'

    Id = Column(Integer, primary_key=True)
    Name = Column(String(8000))
    Description = Column(String(8000))
    # NewCol = Column(String(8000))
```

Then, comment out the NewCol line, and repeat the migration.

   > Note: this generates a number of warnings for the sample database.  These are caused by _autonum_ columns declared as _null allowed_.  These warnings are benign, and should not affect your own databases.

## Next steps
Consider using [API Logic Server `rebuild`](https://github.com/valhuber/ApiLogicServer/wiki#rebuilding) services to upgrade your API and admin app.