### Update - `psycopg2` pre-installed as of 06.02.00

`psycopg2` was updated at the end of September 2020.  So, as of release 6.2, this is restored into the build of ApiLogicServer.

&nbsp;

### Postgres - install `psycopg2` -- Release 5.03.33 through 6.1

This is included in Docker, but not for local installs.  To install `psycopg2` (either global to your machine, or within a `venv`):

```bash
pip install psycopg2-binary==2.9.3
```

Please see the examples on the [testing](../Database-Connectivity) for important considerations in specifying SQLAlchemy URIs.

