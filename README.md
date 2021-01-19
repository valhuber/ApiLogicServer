# ApiLogicServer

Creates a server project at ```<project_name>```.

## Current Status

    Update 1/17 7PM
        generating server, mac & windows - IDE or Command Line
        generated server runs, mac and windows
        generated flask app builder runs, mac and windows
        minimal logic operation (server, fab not tested)

#### Change Log
Key changes:
* 1/18: better install instructions (verified mac & windows)

## How to Install it
For reference, we will be creating this structure:

<figure><img src="images/apilogicserver-ide.png"></figure>

Install as any typical project:

```
cd ~/Desktop
Desktop> mkdir server
Desktop> cd server
server> git clone https://github.com/valhuber/ApiLogicServer.git
server> cd ApiLogicServer
ApiLogicServer> virtualenv venv
ApiLogicServer> source venv/bin/activate  # windows venv\Scripts\activate
ApiLogicServer> pip install -r requirements.txt
```


## How to Create the API Logic Server

It will be via ```pip``` in the future, but for now:

```
ApiLogicServer> cd ..  # back to server
server> deactivate
server> mkdir test
server> cd test
test> cp -R ../ApiLogicServer/venv venv   # windows  Xcopy /E /I ..\ApiLogicServer\venv venv >NUL
test> source venv/bin/activate  # windows venv\Scripts\activate

# from arbitrary folder:
(venv) test> % python ../ApiLogicServer/app_logic_server/create_server.py --project_name=my_new_project
# (venv) test> python ..\ApiLogicServer\app_logic_server\create_server.py --project_name=my_new_project

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

## How to Run the API Logic Server

```
test> deactivate
test> cd my_new_project
my_new_project> virtualenv venv
my_new_project> source venv/bin/activate  # windows venv\Scripts\activate
my_new_project> pip install -r requirements.txt
my_new_project> python api_logic_server_run.py
```

This should now run [http://localhost:5000/](http://localhost:5000/), and return data.

## How to run Flask App Builder (FAB)
This is also running (tho, see Flask Admin, below):

```
my_new_project> python ui/basic_web_app/run.py
```
Try http://localhost:8080/, http://0.0.0.0:8080/


#### Flask Admin
This is required to create tables for Users and Roles,
for FAB login.  Not sure whether you can run fab without doing that.

It's pre-installed for the nw (default) database: (user=```admin``, password=```p```)

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

    
# Next Steps

## Project Installation

Is everybody able to run?

##  Cleanup
Let's review these items:

* I moved ```app``` module to ```api``` module... like?

* Also, can we move ```admin``` under ```ui```?

   * Compare to fab?

* Generated code review (e.g., use of ```api``` module vs a ```def```)

* expose_existing is generating garbage for the view


## Fab and Logic

Not working yet.


## Logic Bank works... Constraint Messages?
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

    I understand this to be related to not-yet-published SAFRS?


## Try with other DBs, non-sqlite
These will probably fail in FAB,
since the admin data is not being created.


## PIP Install / Operation
As customers will run.  (Bunch of work here).

In FUTURE, envisioned* to be installed and used like this:
```
virtualenv venv
pip install ApiLogicServer
pip install -r requirements.txt  -- from where??  (this is for calling expose_existing)
ApiLogicServer <project_name>
```

* Calling expose_existing is awkward,
  unsure how it will work using ```pip```.


## Windows
Delete is failing, so the target generation folder must
not exist.  This also leaves the ```.git``` folder,
but not fatal.
