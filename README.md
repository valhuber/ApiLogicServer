# Operation
Preliminary version, envisioned to be used:
```
virtualenv venv
pip install -r requireents.txt  -- from where??
ApiLogicServer <project_name>
```
Creates a server project at <project_name>.

This version has only been run under PyCharm (which recall sets
PythonPath to make things easy).  The app is set up to run
```ApiLogicServer/create_server.py``` either
in debugger, or cmd-line.  In either case, we call ```main()```
with default parameters.

Here, the default project is ```my_project```, within ```ApiLogicServer```.

```main()``` executes ```run()```:
1. Clones ```ApiLogicServerProto```
1. Create ```database/models.py```
1. Creates ```ui/basic_web_app``` (a secondary objective for now)
   * This is tricky - we dynamically import ```database/models.py```
    so we can iterate through the metadata
1. Executes ```views, apis = generate_from_model.run()```
1. Appends into these files in the created project
    * ```views``` to ```ui/basic_web_app/app/views.py```
    * ```apis``` to ```api/expose_api_models``` (this is called by ```api/__init__.py```)
    

    Important: for now, this is mac only.

# Next Steps

## Make Generated Project Work
So, let's make the generated app run: run the debugger, and
make required changes to ```my_project```, within ```ApiLogicServer```.
    
## Command Line Operation
And, this needs to run from the command line.
That will be via ```pip``` in the future, but for now:

```
python /Users/val/dev/ApiLogicServer/app_logic_server/create_server.py project=my-project
```
This fails since the pip requirements for codegen are
not met.  Not sure how to resolve... **advice?**
