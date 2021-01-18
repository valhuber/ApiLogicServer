# ApiLogicServer

Creates a server project at ```<project_name>```.

## Current Status

    Update 1/17 7PM
        generating server, mac & windows - IDE or Command Line
        generated server runs, mac and windows
        generated flask app builder runs, mac and windows

## How to Install it

Install as any typical project (I do this in PyCharm):

```
git clone https://github.com/valhuber/ApiLogicServer.git
cd ApiLogicServer
virtualenv venv
source venv/bin/activate  # windows venv\Scripts\activate
```

#### *In FUTURE, envisioned* to be installed and used like this:
```
virtualenv venv
pip install ApiLogicServer
pip install -r requirements.txt  -- from where??  (this is for calling expose_existing)
ApiLogicServer <project_name>
```


## How to generate the API Server
The generator is run via
```ApiLogicServer/create_server.py```, either
in the IDE, or cmd-line. 

Running from the IDE is not required, but ensures your parameters are correctly
defaulted, and confirms a successful install:

```
# run create_server.py from IDE
```
Running that way is hard-coded to create default project: ```Desktop/my_project```.
Expected console log:

```
API Logic Server Creation 1.0.0 (using debug default arguments)

Delete dir: /Users/val/Desktop/my_project
Create Project with command: git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git /Users/val/Desktop/my_project
Delete dir: /Users/val/Desktop/my_project/.git
Create database/models.py with command: python /Users/val/dev/ApiLogicServer/expose_existing/sqlacodegen/sqlacodegen/main.py sqlite:////Users/val/dev/ApiLogicServer/app_logic_server/nw.sqlite  > /Users/val/Desktop/my_project/database/models.py
Create ui/basic_web_app with command: flask fab create-app --name /Users/val/Desktop/my_project/ui/basic_web_app --engine SQLAlchemy
Create ui/basic_web_app/app/views.py and api/expose_api_models.py (import / iterate models)
Writing: /api/expose_api_models.py
Update api_logic_server_run.py, config.py and ui/basic_web_app/config.py with project_name and db_url
Writing: /ui/basic_web_app/app/views.py

Process finished with exit code 0
```


<figure><img src="images/apilogicserver-ide.png"></figure>

### How to generate from the Command Line
    
This is the expected usage.
It will be via ```pip``` in the future, but for now:

```
cd ~
mkdir test
cd test
cp -a <ApiLogicServer>/venv. venv
# eg, cp -R /Users/val/dev/ApiLogicServer/venv venv
# eg, Xcopy /E /I C:\Users\val\dev\ApiLogicServer\venv C:\Users\val\Desktop\test\venv >NUL
source venv/bin/activate  # windows venv\Scripts\activate

# from arbitrary folder:
(venv) val@Vals-MacBook-Pro-16 test % python /Users/val/dev/ApiLogicServer/app_logic_server/create_server.py --project_name=my_new_project --db_url=sqlite:////Users/val/dev/ApiLogicServer/app_logic_server/nw.sqlite
# (venv) C:\Users\val\Desktop\test> python C:\Users\val\dev\ApiLogicServer\app_logic_server\create_server.py --project_name=my_new_project

API Logic Server Creation 1.0.0 here

Tables Not Exposed [ProductDetails_V]: 
Generate Flask AppBuilder [Y/n]: 
Favorite Column Names [name description]: 
Non Favorite Column Names [id]: 
Delete dir: /Users/val/Desktop/test/my-new-project
Error: /Users/val/Desktop/test/my-new-project : No such file or directory
Create Project with command: git clone --quiet https://github.com/valhuber/ApiLogicServerProto.git /Users/val/Desktop/test/my-new-project
Delete dir: /Users/val/Desktop/test/my-new-project/.git
Create database/models.py with command: python /Users/val/dev/ApiLogicServer/expose_existing/sqlacodegen/sqlacodegen/main.py sqlite:////Users/val/dev/ApiLogicServer/app_logic_server/nw.sqlite  > /Users/val/Desktop/test/my-new-project/database/models.py
Create ui/basic_web_app with command: flask fab create-app --name /Users/val/Desktop/test/my-new-project/ui/basic_web_app --engine SQLAlchemy
Create ui/basic_web_app/app/views.py and api/expose_api_models.py (import / iterate models)
Writing: /api/expose_api_models.py
Update api_logic_server_run.py, config.py and ui/basic_web_app/config.py with project_name and db_url
Writing: /ui/basic_web_app/app/views.py
(venv) val@Vals-MacBook-Pro-16 test % 
```

#### Issue setting PYTHONPATH
For now, the ```venv``` copy is required - I was unable to "push" PYTHONPATH to run ```expose_existing``` in ```run_command(cmd: str, env=None)```:
```
result_b = subprocess.check_output(cmd, shell=True, env=use_env)
```

## How to run the API Logic Server

```
# pwd - still in test
cd my_new_project
virtualenv venv
source venv/bin/activate  # windows venv\Scripts\activate
pip install -r requirements.txt
python api_logic_server_run.py
```

This should now run, and return data.

## How to run Flask App Builder (FAB)
This is also running:

```
python ui/basic_web_app/run.py
```
Try http://localhost:8080/, http://0.0.0.0:8080/
    
# Next Steps

## Windows
Delete is failing, so the target generation folder must
not exist.  This also leaves the ```.git``` folder,
but not fatal.


##  Cleanup
Let's review these items:

* I moved ```app``` module to ```api``` module... like?

* Also, can we move ```admin``` under ```ui```?

* Generated code review (e.g., use of ```api``` module vs a ```def```)

* expose_existing is generating garbage for the view

## Engage Logic Bank
Trivial constraint works:
```
    Rule.constraint(validate=models.Customer,
                    as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="Balance must be < Credit Limit")
```
Patch this data:
```
{
  "data": {
    "attributes": {
      "Id": "ALFKI",
      "CreditLimit": "10"
    },
    "type": "Customer",
    "id": "ALFKI"
  }
}
```

But not seeing any useful message in swagger, other than console (once logging set up)....
```
Logic Phase:		ROW LOGIC (sqlalchemy before_flush)			 - 2021-01-18 08:13:49,523 - logic_logger - DEBUG
Logic Phase:		ROW LOGIC (sqlalchemy before_flush)			 - 2021-01-18 08:13:49,523 - logic_logger - DEBUG
..Customer[ALFKI] {Update - client} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 1016.0000000000, CreditLimit:  [2000.0000000000-->] 10, OrderCount: 9, UnpaidOrderCount: 4  row@: 0x106409d90 - 2021-01-18 08:13:49,524 - logic_logger - DEBUG
..Customer[ALFKI] {Update - client} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 1016.0000000000, CreditLimit:  [2000.0000000000-->] 10, OrderCount: 9, UnpaidOrderCount: 4  row@: 0x106409d90 - 2021-01-18 08:13:49,524 - logic_logger - DEBUG
..Customer[ALFKI] {early_events} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 1016.0000000000, CreditLimit:  [2000.0000000000-->] 10, OrderCount: 9, UnpaidOrderCount: 4  row@: 0x106409d90 - 2021-01-18 08:13:49,524 - engine_logger - DEBUG
..Customer[ALFKI] {formula_rules} Id: ALFKI, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Address: Obere Str. 57, City: Berlin, Region: Western Europe, PostalCode: 12209, Country: Germany, Phone: 030-0074321, Fax: 030-0076545, Balance: 1016.0000000000, CreditLimit:  [2000.0000000000-->] 10, OrderCount: 9, UnpaidOrderCount: 4  row@: 0x106409d90 - 2021-01-18 08:13:49,525 - engine_logger - DEBUG
[2021-01-18 08:14:14,409] ERROR: ValidationError: Balance must be < Credit Limit
[2021-01-18 08:14:19,776] ERROR: Generic Error: get_instance : 
[2021-01-18 08:14:19,776] INFO: Error in http://localhost:5000/Customer/ALFKI/
```


## PIP Install / Operation
As customers will run.

## Try with other DBs, non-sqlite
These will probably fail in FAB,
since the admin data is not being created.

## Flask Admin
This is required to create tables for Users and Roles,
for FAB login.  Not sure whether you can run fab without doing that.

It creates tables in your database, so probably best
not to have it automatic.

```
cd my_project
echo $PYTHONPATH
PYTHONPATH="/Users/val/dev/my_project:$PYTHONPATH"
export PYTHONPATH

cd ui/basic_web_app
(venv)$ export FLASK_APP=app
(venv)$ flask fab create-admin
Username [admin]:
User first name [admin]:
User last name [user]:
Email [admin@fab.org]:
Password:
Repeat for confirmation:
```


