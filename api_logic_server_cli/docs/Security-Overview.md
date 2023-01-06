Security is under active development.  You can examine the [Prototype in the Preview Version](../#preview-version){:target="_blank" rel="noopener"}.  We are seeking design partners, so contact us if you'd like to discuss - we'd love to hear from you!

## Terms

* Authentication: a login function that confirms a user has access, usually by posting credentials and obtaining a token identifying the users' roles.
* Authorization: controlling access to row/columns based on assigned roles.
* Role: in security, users are assigned one or many roles.  Roles are authorized for access to data, potentially down to the row/column level.

## Overview

The overall flow is shown below, where:

* __Green__ - represents __developer__ responsibilities
* __Blue__ - __System__ processing

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/security/overview.png"></figure>

### Developers Configure Security

Developers are responsible for providing (or using system defaults).

#### Authentication-Provider

This class, given a user/password, returns the list of authorized roles (on None).  It is invoked by the system when client apps log in.

Developers must:

    * Provide this class

    * This class is configured in `config.py`

&nbsp;

#### Authentication Data

Developers must determine the data required to authenticate users.  This can be a SQL Database, LDAP, AD, etc.  It is separate from user databases so it can be shared between systems.  The Authentication-Provider uses it to authenticate a user/password, and return their roles.

&nbsp;

#### `declare_security`

Add code to the pre-created (empty) Python module that defines table/role filters.  The system merges these into each retrieval.

&nbsp;

### System Processing

System processing is summarized below.

#### Startup: `declare_security`

When you start the server, the system (`api_logic_server_run.py`) imports `declare_security`.  This:

1. Imports `from security.system.security_manager import Grant, Security`, which sets up SQLAlchemy listeners for all database access calls

2. Creates `Grant` objects, internally maintained by the system for subsequent use on API calls.

2. The from security import declare_security  # activate security

&nbsp;

#### Login: Auth Provider

When users log in, the app `POST`s their id/password to the system, which invokes the Authentication-Provider to autthenticate and return a set of roles.  These are tokenized and returned to the client, and passed in the header of subsequent requests.

The startup process also 

&nbsp;

#### API: Security Manager

Clients make API calls, providing the login token.  The system

## Use Cases

### Data Security

Security enables you to hide certain rows from designated roles, such as a list of HR actions.

&nbsp;

### Multi-Tenant

Some systems require the data to be split between multiple customers.  One approach here is to 'stamp' each row with a client_id, associate client_id with each customers, and then add the client_id to each search.  The sample illustrates how this can be achieved with [authorization](../Security-Authorization){:target="_blank" rel="noopener"}:

```python
Grant(  on_entity = models.Category,
        to_role = Roles.tenant,
        filter = models.Category.Client_id == Security.current_user().client_id)  # User table attributes
```

&nbsp;

## Status: Preview

This preview is intended to:

* Confirm approach to __role-based row authorization__, using SQLAlchemy [adding-global-where](https://docs.sqlalchemy.org/en/14/orm/session_events.html#adding-global-where-on-criteria) functionality.  See also [the examples](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.with_loader_criteria).
     * Note using SQLAlchemy means that filters apply to all SAFRS and custom api access
     * SQLAlchemy support is working quite well!
* Confirm whether the basic filtering capability __meets the requirements of 1 real-world app__
     * Once *certain* use case is *multi-tenent*
         * Each row is stamped with a `client_id`
         * User table identifies users' `client_id`
         * Enforced in `declare_security.py`:
     * Preliminary finding - first test case worked on real-world app

&nbsp;

This preview is _not_ meant to explore:

* Login Authentication (currently addressed with a place-holder stub)

* Interaction with SAFRS API handling (except to the extent SAFRS uses SQLAlchemy)

* System issues such as performance, caching, etc.


&nbsp;

## Trying this on your own project

We'd love the feedback.  Follow the directions below, and please contact the authors.

&nbsp;

## Setup and Test

You can explore this with and without configuration.  Use the [preview build](../#preview-version){:target="_blank" rel="noopener"}.

&nbsp;

### Pre-configured

Security is enabled when building the sample app.  Test it by

* Admin App - verify the `Categories` screen has 1 row

* cURL

```
curl -X 'GET' \
'http://localhost:5656/api/CategoryTable/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=id' -H 'accept: application/vnd.api+json' -H 'Content-Type: application/vnd.api+json'
```

&nbsp;

### Configure

Build the sample _without customizations_:

    1. `ApiLogicServer create --project_name=nw --db_url=nw-`
    2. cd nw
    3. Add security: `ApiLogicServer add-db --db_url=auth --bind_key=authentication`
        * This uses [Multi-Database Support](../Data-Model-Multi){:target="_blank" rel="noopener"} for the sqlite authentication data
    4. Set `SECURITY_ENABLED = True` in config.py

Test as described above.