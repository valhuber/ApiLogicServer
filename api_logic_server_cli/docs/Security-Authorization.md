# Authorization Prototype

This is a prototype of security, for user feedback.  It is **not** ready for production - it does not even contain Authentication.

## Goals

[This POC](https://github.com/valhuber/security-poc#readme) is intended to:

* Confirm approach to __role-based row authorization__, using SQLAlchemy [adding-global-where](https://docs.sqlalchemy.org/en/14/orm/session_events.html#adding-global-where-on-criteria) functionality.  See also [the examples](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.with_loader_criteria).
     * Note using SQLAlchemy means that filters apply to all SAFRS and custom api access
     * SQLAlchemy support is working quite well!
* Confirm whether the basic filtering capability __meets the requirements of 1 real-world app__
     * Once *certain* use case is *multi-tenent*
         * Each row is stamped with a `client_id`
         * User table identifies users' `client_id`
         * Enforced in `declare_security.py`:
     * Preliminary finding - first test case worked on real-world app

```python
Grant(  on_entity = models.Category,
        to_role = Roles.tenant,
        filter = models.Category.Id == Security.current_user().client_id)  # User table attributes
```

&nbsp;

This POC is _not_ meant to explore:

* Login Authentication (currently addressed with a place-holder stub)

* Interaction with SAFRS API handling (except to the extent SAFRS uses SQLAlchemy)

* System issues such as performance, caching, etc.

&nbsp;

## Setup and Test

You can run this in 2 ways:

1. Use the [experimental build](), and
     1. Create the sample project
     2. Set `SECURITY_ENABLED = True` in config.py

2. Or, run the pre-built project in codespaces:

     1. Open [this repository](https://github.com/valhuber/security-poc) in codespaces

         * Takes about a minute; wait until the Ports tab shows up

     2. Start the server, using the provided Launch Configuration

     3. Issue this in the codespaces (_not_ your local machine) terminal window, and verify it returns 1 row:


To Test (if running in Codespaces, use the Codespaces terminal - _not_ your local computers' terminal):

```
curl -X 'GET' \
'http://localhost:5656/api/CategoryTable/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=id' -H 'accept: application/vnd.api+json' -H 'Content-Type: application/vnd.api+json'
```

&nbsp;

## Active Code

See `api_logic_server_run.py`, around line 400, which activates `security/system/security_manager.py`.

&nbsp;

## Declaring Logic

Analogous to logic declarations, Developers declare filters for users' roles (role-based access control).  A user can have multiple roles; a users' filters are **and**ed together:

<figure><img src="https://github.com/valhuber/security-poc/blob/main/doc/images/declare-security.png?raw=true"></figure>

&nbsp;

## Design Notes

<figure><img src="https://github.com/valhuber/security-poc/blob/main/doc/images/basic-design.png?raw=true"></figure>

&nbsp;

### Authentication DB

Note this uses [Multi-DB Support](https://github.com/valhuber/MultiDB).  

The database file is `security/authentication_provider/sql/authentication_db.sqlite`, patterned after an earlier prototype `admin_api.py` (currently unused).  This database adds:

* Roles (`Role` and `UserRole`)
* User.client_id, to test multi-tenant (the test user is **aneu**).

<figure><img src="https://github.com/valhuber/security-poc/blob/main/doc/images/authentication-db.png?raw=true"></figure>

&nbsp;

### Authentication Provider

Like Harry Truman's remark that 12 economists have 13 opinions, organizations have a myriad set of ways to identify valid users.  So, a key requirement is an extensible "pluggable" mechanism.

We are using Abstract Classes ([thanks](https://medium.com/techtofreedom/10-remarkable-python-oop-tips-that-will-optimize-your-code-significantly-a47e4103b44d)) to define provider expectations in `security/authentication_provider/abstract_authentication_provider.py`.

There are 2 implementations (both are working):

* `security/authentication_provider/memory`
* `security/authentication_provider/sql` - uses the _Authentication DB_, above

You select the _authentication_provider_ in `config.py`:

```python
    from security.authentication_provider.sql.auth_provider import Authentication_Provider
    SECURITY_PROVIDER = Authentication_Provider
```

You can define new authentication providers, e.g. for Active Directory, LDAP, etc.

&nbsp;

## Status

Now initially running, per [this support](https://github.com/sqlalchemy/sqlalchemy/discussions/8976), using the in-memory auth provider `security/authentication_provider/mem_auth_row.py.`

The db-based provider (`security/authentication_provider/sql/auth_provider.py`) is also running.

&nbsp;

## Trying this on your own project

We'd love the feedback.  Please contact the authors.
