Authentication Providers are developer-supplied code, called by the system during login.  It is passed the id/password, and returns a user row and list of roles.

The underlying presumptions:

1. Multiple systems will share the same authentication data, so this data will be separate from each application

2. Organizations will utilize a wide variety of techniques to maintain authorization data (databases, LDAP, AD etc), so an open "interface" approach is required.

&nbsp;

## Abstract_Authentication_Provider

To ensure that Authentication-Providers implement the api expected by the system, you should inherit from this class.

&nbsp;

### Configure Authentication Provider

You select the _authentication_provider_ in `config.py`:

```python
    from security.authentication_provider.sql.auth_provider import Authentication_Provider
    SECURITY_PROVIDER = Authentication_Provider
```

You can define new authentication providers, e.g. for Active Directory, LDAP, etc.

&nbsp;

## Memory Auth Provider

Provided for quick prototyping.

&nbsp;

## sqlite Auth Provider

This provided to demonstrate a typical sql-based Authentication-Provider.

&nbsp;

### Authentication DB

Note this uses [Multi-DB Support](..Data-Model-Multi).  

The database file is `security/authentication_provider/sql/authentication_db.sqlite`.  This database includes:

* Users
* Roles (`Role` and `UserRole`)
* User.client_id, to test multi-tenant (the test user is **aneu**).

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/security/authentication-db.png"></figure>

&nbsp;

