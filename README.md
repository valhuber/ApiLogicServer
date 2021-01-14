# ApiLogicServer Operation
Preliminary version, *envisioned* to be used:
```
virtualenv venv
pip install ApiLogicServer
pip install -r requirements.txt  -- from where??
ApiLogicServer <project_name>
```
Creates a server project at <project_name>.

This version has only been run under PyCharm (which recall sets
PythonPath to make things easy).  The app is set up to run
```ApiLogicServer/create_server.py``` either
in debugger, or cmd-line.  In either case, we call ```main()```
with default parameters.  cmd-line does not work yet.

## How to run it

Install as any typical project (I do this is PyCharm):

```
git clone https://github.com/valhuber/ApiLogicServer.git
cd ApiLogicServer
virtualenv venv
source venv/bin/activate
cd app_logic_server
python create_server.py  # or run from IDE
```

Here, the default project is ```my_project```, within ```ApiLogicServer```.

    Update: now working on windows


## Basic Operation (Internals)

```main()``` executes ```run()```:
1. Clones ```ApiLogicServerProto``` (subprocess.check_output(git clone))
1. Create ```database/models.py``` (subprocess.check_output(modified sqlacodegen))
1. Creates ```ui/basic_web_app``` (a secondary objective for now)
   * This is tricky - we _dynamically_ import ```database/models.py```
     (from previous step), so we can iterate through the metadata
1. Executes ```views, apis = generate_from_model.run()```
1. Appends into these files in the created project
    * ```views``` to ```ui/basic_web_app/app/views.py```
    * ```apis``` to ```api/expose_api_models``` (this is called by ```api/__init__.py```)
    
    
# Next Steps

## Make Generated Project Work
So, let's make the generated app run: run the debugger, and
make required changes to ```my_project```, within ```ApiLogicServer```.
    
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

