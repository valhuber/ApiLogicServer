
## Starting the Server

### Via the IDE

As described in the Quick Start, Run Configurations are provided to start the server in your IDE.

&nbsp;

### Directly

Recall that you execute your API Logic Project by __starting the server__, like this:

```
ApiLogicServer (venv)> cd my_new_project
my_new_project(venv)> python api_logic_server_run.py
```
Note this presumes you have activated your `venv`.  The system also provides shell scripts you can use:
```
sh run.sh  # windows - use run.ps1
```

Then, __to run the Admin App and Swagger:__

Run your browser at

```html
http://localhost:5656/
```

Or, to run the Basic Web App:

```bash
ApiLogicServer run-ui [--host=myhost --port=myport]  # or...
my_new_project> python ui/basic_web_app/run.py [host port]
```

Try http://localhost:5002/, http://0.0.0.0:5002/

&nbsp;

### Using the Run script

Alternatively, you can start the server using the run script, e.g.:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/server-run.png"></figure>

### Stopping the server

You can stop the server by cancelling it, or via an API:

```
http://localhost:5656/stop?msg=API stop - Stop API Logic Server
```

This can be useful in testing if you don't have access to the server console.  The `msg` parameter is optional.

&nbsp;

## Host and Port Handling

ApiLogicServer attempts to avoid port conflicts.  These can arise from:

* Common use of 8080

* Mac use of 5000

To avoid conflicts, ports are defaulted as follows:

| For |  Port |
|:--------------|:--------------|
| ApiLogicServer | `5656` |
| Basic Web App | `5002` |


Hosts are defaulted as follows:

| Installed as |  Basic Web App Host |
|:--------------|:--------------|
| Docker | `0.0.0.0` |
| Local Install | `localhost` |

&nbsp;

### Create time overrides

You can override these defaults when you create the application like this:

```bash
ApiLogicServer create --project_name=~/dev/servers/api_logic_server \
                      --host=myhost --port=myport --swagger_host=mycloud
```

&nbsp;

### Runtime overrides

When you run created applications, you can provide arguments to override the defaults.  Discover the arguments using `--help`:

```bash
(venv) val@Vals-MBP-16 ApiLogicProject % python api_logic_server_run.py -h

API Logic Project Starting: /Users/val/dev/servers/ApiLogicProject/api_logic_server_run.py
usage: api_logic_server_run.py [-h] [--port PORT] [--flask_host FLASK_HOST] [--swagger_host SWAGGER_HOST]
                               [--swagger_port SWAGGER_PORT] [--http_type HTTP_TYPE] [--verbose VERBOSE]
                               [--create_and_run CREATE_AND_RUN]
                               [flask_host_p] [port_p] [swagger_host_p]

positional arguments:
  flask_host_p
  port_p
  swagger_host_p

options:
  -h, --help                       show this help message and exit
  --port PORT                      port (Flask) (default: 5656)
  --flask_host FLASK_HOST          ip to which flask will be bound (default: localhost)
  --swagger_host SWAGGER_HOST      ip clients use to access API (default: localhost)
  --swagger_port SWAGGER_PORT      swagger port (eg, 443 for codespaces) (default: 5656)
  --http_type HTTP_TYPE            http or https (default: http)
  --verbose VERBOSE                for more logging (default: False)
  --create_and_run CREATE_AND_RUN  system use - log how to open project (default: False)
(venv) val@Vals-MBP-16 ApiLogicProject % 

```
These are used for [Codespaces support](https://valhuber.github.io/ApiLogicServer/Tech-CodeSpaces/){:target="_blank" rel="noopener"}

&nbsp;

__Notes:__

* `host` is the flask-host, which maps to the IP address of the interface to which flask will be bound (on the machine itself
* `swagger_host` maps to the ip address as seen by the clients

For example, 127.0.0.1 (localhost) or 0.0.0.0 (any interface) only have meaning on your own computer.
Also, it's possible to map hostname->IP DNS entries manually in /etc/hosts, but users on other computers are not aware of that mapping.

&nbsp;
## Production Deployment

As noted in the [gunicorn documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/):

  > While lightweight and easy to use, Flask’s built-in server is not suitable for production as it doesn’t scale well. 

#### gunicorn
You can run API Logic Server servers under [gunicorn](https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/){:target="_blank" rel="noopener"}.  To use the default API Logic Server ports:

```
gunicorn api_logic_server_run:flask_app -w 4 -b localhost:5656
```

Or, to use the default gunicorn ports:

```
gunicorn api_logic_server_run:flask_app -w 4
```

You will also need to:

1. Update the default server/port settings in `api_logic_server_run.py`
2. Start your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

#### PythonAnywhere
Please see the [Install Instructions](../Install) for information on PythonAnywhere.
