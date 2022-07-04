As described in the [readme](https://github.com/valhuber/ApiLogicServer/blob/main/README.md):

```bash
cd ApiLogicServer      # a directory of projects on local host

# Start (install if required) the API Logic Server docker container...

docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server
```

This will start a command line in the Docker container.
You are now able to issue commands like `ApiLogicServer create` as described in the readme.

The `api_logic_server` image supports startup arguments so you can control the `api_logic_server` container, by running a startup script or by supplying environment variables.  You might, for example, have automated test procedures that load projects from `GitHub` and run tests.


> Already installed?  Upgrade to the latest (5.03.06): ```docker pull apilogicserver/api_logic_server``` (you may need to [rebuild your container](https://valhuber.github.io/ApiLogicServer/Execute-VSCode-Docker/)).

For more information, see [Working With Docker](../Working-With-Docker).

