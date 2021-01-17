# ApiLogicServer

Creates a server project at <project_name>.

## Current Status

    Update 1/16 6PM
        generating server, windows & mac
        server runs, mac (not windows)
        generated flask app builder runs (mac)


This version has only been run under PyCharm (which recall sets
PythonPath to make things easy).  The app is set up to run
```ApiLogicServer/create_server.py``` either
in debugger, or cmd-line.  In either case, we call ```main()```
with default parameters.  cmd-line does not work yet.

## How to Install it
Preliminary version - **run from IDE:**
Install as any typical project (I do this is PyCharm):

```
git clone https://github.com/valhuber/ApiLogicServer.git
cd ApiLogicServer
virtualenv venv
source venv/bin/activate
```

*Envisioned* to be used:
```
virtualenv venv
pip install ApiLogicServer
pip install -r requirements.txt  -- from where??
ApiLogicServer <project_name>
```


## How to generate the API Server

Install as any typical project (I do this is PyCharm):

```
cd app_logic_server
# run create_server.py from IDE
```
Currently hard-coded to create default project: ```Desktop/my_project```.
Expected log:
```
Delete dir: /Users/val/Desktop/my_project
Create Project with command: git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git /Users/val/Desktop/my_project
Delete dir: /Users/val/Desktop/my_project/.git
Create database/models.py with command: python /Users/val/dev/ApiLogicServer/expose_existing/sqlacodegen/sqlacodegen/main.py sqlite:////Users/val/dev/ApiLogicServer/app_logic_server/nw.sqlite  > /Users/val/Desktop/my_project/database/models.py
Create ui/basic_web_app with command: flask fab create-app --name /Users/val/Desktop/my_project/ui/basic_web_app --engine SQLAlchemy
Create ui/basic_web_app with command: flask fab create-app --name /Users/val/Desktop/my_project/ui/basic_web_app --engine SQLAlchemy result: Downloaded the skeleton app, good coding!
Create ui/basic_web_app/app/views.py and api/expose_api_models.py (import / iterate models)
Writing: /api/expose_api_models.py
Update api_logic_server_run.py, config.py and ui/basic_web_app/config.py with project_name and db_url
Writing: /ui/basic_web_app/app/views.py

Process finished with exit code 0
```


<figure><img src="images/apilogicserver-ide.png"></figure>

## How to run the API Server

```
cd ~/Desktop/my_project
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python api_logic_server.py
```

This should now run, and return data.

## How to run Flask App Builder (FAB)
This is also running (on mac at least):

```
cd ui/BasicWebApp
# run run.py under IDE
```


## Basic Operation (Internals)

```main()``` executes ```run()```:
1. Clones ```ApiLogicServerProto``` (subprocess.check_output(git clone))
1. Create ```database/models.py``` (subprocess.check_output(modified sqlacodegen))
1. Creates ```ui/basic_web_app``` (a secondary objective for now)
1. Executes ```views, apis = generate_from_model.run()```
   * This is tricky - we _dynamically_ import ```database/models.py```
     (from previous step), so we can iterate through the metadata
1. Appends into these files in the created project
    * ```views``` to ```ui/basic_web_app/app/views.py```
    * ```apis``` to ```api/expose_api_models``` (this is called by ```api/__init__.py```)
    
    
# Next Steps

## Engage Logic Bank
Not tried yet

## Run outside IDE, via PIP
As customers might run

## Try with other DBs, non-sqlite
These will probably fail in FAB, since the admin data is not being created.
    
## Command Line Operation
And, this needs to run from the command line.
That will be via ```pip``` in the future, but for now:

```
# usual project install (git clone, virtualenv... as above)

cd some_folder
cp <ApiLogicServer>/venv venv
source venv/bin/activate

python /Users/val/dev/ApiLogicServer/app_logic_server/create_server.py --project=my-project
```

For now, the ```venv``` is required - I was unable to "push" PYTHONPATH to run ```expose_existing``` in ```run_command(cmd: str, env=None)```:
```
result_b = subprocess.check_output(cmd, shell=True, env=use_env)
```

