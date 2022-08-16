### Postgres - install `psycopg2`

This is included in Docker, but not for local installs.  To install `psycopg2` (either global to your machine, or within a `venv`):

```bash
pip install psycopg2-binary==2.9.3
```

Please see the examples on the [testing](../Database-Connectivity) for important considerations in specifying SQLAlchemy URIs.

&nbsp;