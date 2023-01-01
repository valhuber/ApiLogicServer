Security is under active development.  You can examine the [Prototype in the Preview Version](../#preview-version){:target="_blank" rel="noopener"}.  We are seeking design partners, so contact us if you'd like to discuss - we'd love to hear from you!

## Terms

* Authentication: a login function that confirms a user has access, usually by posting credentials and obtaining a token identifying the users' roles.
* Authorization: controlling access to row/columns based on assigned roles.
* Role: in security, users are assigned one or many roles.  Roles are authorized for access to data, potentially down to the row/column level.

## Overview

The overall flow is shown below, where:

* Green - represents developer responsibilities
* Blue - System processing

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

### System

System support is summarized below.

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

&nbsp;

## Status

Running in preview build, _without_ authentication (currently hard-wired).

&nbsp;

## Trying this on your own project

We'd love the feedback.  Please contact the authors.