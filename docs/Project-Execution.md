
## How to Run the API Logic Server

```
ApiLogicServer> cd my_new_project
my_new_project> python api_logic_server_run.py
```

This should now run [http://localhost:5656/](http://localhost:5656/), and return data.

&nbsp;

#### Host and Port Handling

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

###### Overriding Host and Port

When you run created applications, you can provide arguments to override these defaults.  For example:

```bash
ApiLogicServer run --project_name=~/dev/servers/api_logic_server --host=myhost --port=myport

python ~/dev/servers/api_logic_server/api_logic_server_run.py myhost myport      # equivalent to above
```

&nbsp;

## How to run the Admin App
Start the ApiLogicServer, and run your browser at

```html
http://localhost:5656/
```

&nbsp;

## How to run the Basic Web App
You can run the Basic Web App like this:

```bash
ApiLogicServer run-ui [--host=myhost --port=myport]

my_new_project> python ui/basic_web_app/run.py [host port]
```

Try http://localhost:5002/, http://0.0.0.0:5002/
