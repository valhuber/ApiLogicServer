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

## Active Code

See `api_logic_server_run.py`, around line 400, which activates `security/system/security_manager.py`.

&nbsp;

## Declaring Logic

Analogous to logic declarations, Developers declare filters for users' roles (role-based access control).  A user can have multiple roles; a users' filters are **and**ed together:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/security/declare-security.png"></figure>



