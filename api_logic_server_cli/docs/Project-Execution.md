
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

When you run created applications, you can provide arguments to override the defaults.  For example:

```bash
ApiLogicServer run --project_name=~/dev/servers/api_logic_server \
                   --host=myhost --port=myport --swagger_host=mycloud

python ~/dev/servers/api_logic_server/api_logic_server_run.py \
                   myhost myport mycloud     # equivalent to above
```

&nbsp;

__Notes:__

* `host` is the flask-host, which maps to the ip address of the interface to which flask will be bound (on the machine itself
* `swagger_host` maps to the ip address as seen by the clients

For example, 127.0.0.1 (localhost) or 0.0.0.0 (any interface) only have meaning on your own computer.
Also, it's possible to map hostname->ip dns entries manually in /etc/hosts, but users on other computers are not aware of that mapping.
