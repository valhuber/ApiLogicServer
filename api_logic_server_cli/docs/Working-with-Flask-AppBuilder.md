This page describes considerations for using [Flask AppBuilder](https://flask-appbuilder.readthedocs.io/en/latest/).

# Create Flask AppBuilder Admin
The FAB system requires tables in your database for authenticating and authorizing users (tables such as `ab_user`, `ab_user_role`, etc).  Create these as follows (Username: `admin`, Password: `p`):
```
cd api_logic_server  # your --project_name
export PYTHONPATH="/Users/val/dev/servers/api_logic_server"  
source venv/bin/activate  # windows: venv\Scripts\activate
(venv)cd ui/basic_web_app
(venv)$ export FLASK_APP=app
(venv)$ flask fab create-admin
Username [admin]:
User first name [admin]:
User last name [user]:
Email [admin@fab.org]:
Password:p
Repeat for confirmation:p
```

# Important: Activate Logic after Create Admin
For databases other than Northwind, logic is initially disabled to avoid *unhashable* issues in Create Admin.
When Create Admin is completed, edit ```ui/basic_web_app/app/__init__.py``` to enable logic like this:
```
import database.models as models
from logic import declare_logic
from logic_bank.logic_bank import LogicBank
# *** Enable the following after creating Flask AppBuilder Admin ***
LogicBank.activate(session=db.session, activator=declare_logic)  # edited to enable logic
```

# Edit ```views.py``` Files to Customize Pages

### Background: ```views.py``` files
Flask AppBuilder ```ui/basic_web_app/app/views.py``` files contain segments like this that define pages for each table:

```
class EmployeeModelView(ModelView):
   datamodel = SQLAInterface(Employee)
   list_columns = ["LastName", "Employee.LastName", "FirstName", "Title", "ReportsTo"]
   show_columns = ["LastName", "Employee.LastName", "FirstName", "Title", "ReportsTo", "BirthDate", "HireDate", "Address", "City", "State", "Country", "PostalCode", "Phone", "Fax", "Email", "EmployeeId"]
   edit_columns = ["LastName", "FirstName", "Title", "ReportsTo", "BirthDate", "HireDate", "Address", "City", "State", "Country", "PostalCode", "Phone", "Fax", "Email", "EmployeeId"]
   add_columns = ["LastName", "FirstName", "Title", "ReportsTo", "BirthDate", "HireDate", "Address", "City", "State", "Country", "PostalCode", "Phone", "Fax", "Email", "EmployeeId"]

   related_views = [EmployeeModelView , CustomerModelView]. # FAILS TO COMPILE

appbuilder.add_view(
      EmployeeModelView, "Employee List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: Track
```

These are tedious to code, so they are created by ApiLogicServer.  In order to create good-looking pages, these are _not_ simply column lists, e.g.:
* "Favorite" fields are placed first
    * Control this with the ApiLogicServer CLI ```--favorites``` option
* Joins are created for "id" columns (e.g., show Product _Names,_ not Product _IDs_)
* etc

### Edit ```views.py``` - display options (e.g., charts)
You can hand-edit these pages to make further customizations, including advanced functionality such as charts.


# Mutually Referring Tables Require Fixup

Note the ```related_views``` makes class references in the code snippet above.  Recall that Python is a 1 pass compiler - you can't make references to things that aren't defined.  

So, ApiLogicServer sorts the view classes so that referenced classes are first.  That's why you will see _"table already generated"_ messages, as shown above.

The problem is that when 2 tables (pages) refer to each other, this is not possible.  So, you need to hand-edit the ```view.py``` files to remove these, like this:
```
   related_views = [CustomerModelView]  # omitted self relationships: employees 
```

Self-relationships are corrected automatically; you may need to correct other mutually referring tables.

# Starting Flask AppBuilder
Start the server as follows:
```
cd ui/basic_web_app
export FLASK_APP=app
python run.py [server [port]
```
The console will suggest you login with your Browser at [http://localhost:5002](http://localhost:5002).  You may also need to try [http://127.0.0.1: 5002](http://127.0.0.1: 5002).