Except for the sample project, projects are created with security disabled.  So, a typical project creation sequence might be:

1. Create your project without security

    * Verify connectivity, API operation, Admin App operation, etc.

2. Activate Security

This page describes how to activate security.

&nbsp;

## Pre-configured Sample

Security is enabled when building the sample app.  Explore / test it as described in [Authorization](../Security-Authorization/#sample).

&nbsp;

## Automatic - sqlite Auth Provider

Activate security using the `ApiLogicServer add-security` command.

Suggestion: you can test it using the sample _without customizations_, as follows:

```bash
ApiLogicServer create --project_name=nw --db_url=nw-
cd nw
ApiLogicServer add-security
```

Test it as described in [Authorization](../Security-Authorization/#sample).

Note the use of `db_url=nw-` to create the sample, _without customization or security._

> If you are new to API Logic Server, this is a good way to observe basic project creation.  You can use the `ApiLogicServer add-cust` command to add customizations and security after you explore the basic project.

This command will:

1. Add the sqlite database and models, using `ApiLogicServer add-db --db_url=auth --bind_key=authentication`
    * This uses [Multi-Database Support](../Data-Model-Multi){:target="_blank" rel="noopener"} for the sqlite authentication data
2. Add User.Login endpoint to the User model
3. Set `SECURITY_ENABLED` in `config.py`
4. Add Sample authorizations to security/declare_security.py

&nbsp;

## Manual Configuration 

To configure security:

1. Declare Grants
    * Paste into your `security/declare_security.py` from [this sample](../Security-Authorization/#sample){:target="_blank" rel="noopener"}
2. Set `SECURITY_ENABLED = True` in config.py
3. Configure your Authentication-Provider, using your own [Authentication-Provider](Security-Authentication-Provider){:target="_blank" rel="noopener"},

&nbsp;

## Appendix: Internals

The Security Manager and sqlite Authentication-Provider are built into created projects from the [system's prototype project](https://github.com/valhuber/ApiLogicServer/tree/main/api_logic_server_cli/project_prototype_nw).
