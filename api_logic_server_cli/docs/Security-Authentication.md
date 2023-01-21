Once you have activated security, the system require you to login to obtain a token, and provide this token on subsequent APIs.  This page describes how to login and provide a token.

&nbsp;

## Obtain a token

The sample test apps obtain a token [as shown here](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/test/api_logic_server_behave/features/steps/test_utils.py){:target="_blank" rel="noopener"}.  This is also illustrated in the swagger section, below.

&nbsp;

### Swagger Authentication

Once you activate, tokens are required, including in Swagger.  You can obtain a token and authenticate as described below for the sqlite authentication-provider:

1. Access the User Login service
2. Use the __Try it now__ feature as shown below
3. Copy the token value for use in the next step

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/security/user-post-for-token.png"></figure>

At the top of Swagger, locate the Authenticate button.  Copy the token, precede it with __Bearer__, and login like this:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/security/login.png"></figure>

&nbsp;

## Provide token in header

The sample test apps use this token on API calls [as shown here](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype_nw/test/api_logic_server_behave/features/steps/place_order.py){:target="_blank" rel="noopener"}.