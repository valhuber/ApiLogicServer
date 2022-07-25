
Recall that you execute your API Logic Project by __starting the server__, like this:

```
ApiLogicServer> cd my_new_project
my_new_project> python api_logic_server_run.py
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
