While you will probably want to run it from your IDE (see [IDE > Open and Execute](../IDE-Execute)), you can also run from a Terminal Window, as follows.

__1. Start the Server__
The `api_logic_server_run.py` file is executable.  The simplest way to run it is:

``` title="Either from Docker terminal, or from local terminal with `venv` set"
ApiLogicServer run
```

You can also run it directly:

``` bash title="Either from Docker terminal, or from local terminal with `venv` set"
python api_logic_server_run.py       # options exist to override URL, port
```

__2. Open in your Browser__
The server should start, and suggest the URL for your Browser.  That will open a page like this where you can explore your data using the automatically created [Admin app](../Working-with-the-Admin-App), and explore the API with automatically generated Swagger:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/admin-home.png?raw=true"></figure>

