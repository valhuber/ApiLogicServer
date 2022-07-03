
You can create an ApiLogicServer on [PythonAnywhere](http://pythonanywhere.com) for any cloud-accessible database.  Open a bash console, and:

```bash  
python3 -m venv venv  # ensures that Python3 is used  
source venv/bin/activate

python3 -m pip install ApiLogicServer

ApiLogicServer create --host=ApiLogicServer.pythonanywhere.com --port=   # ApiLogicServer == your account  
```

__1. Create Application__

Here is an example using a pythonanywhere-hosted MySQL database (__note__ the escape character for the $ in the database name:  
```  
ApiLogicServer create --project_name=Chinook \
--host=ApiLogicServer.pythonanywhere.com --port= \
--db_url=mysql+pymysql://ApiLogicServer:***@ApiLogicServer.mysql.pythonanywhere-services.com/ApiLogicServer\$Chinook
```

__2. Create and configure a web app__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/python-anywhere.png?raw=true"></figure>

__3. Update the wsgi__
And copy the contents of ```/home/ApiLogicServer/api_logic_server/python_anywhere_wsgi.py``` over the wsgi file created by pythonanywhere.

__4. Update the Admin App `api_root`__
The first few lines of the Admin.yaml and Admin Config page should be (update the last line:
```
about:
  date: December 26, 2021 09:00:00
  recent_changes: altered tab captions
  version: 3.50.51
api_root: https://apilogicserver.pythonanywhere.com/api
```

__5. Verify `admin.yanl`__
Verify that the `ui/admin.yaml` ends with something like this:

```bash
settings:
  HomeJS: https://apilogicserver.pythonanywhere.com/admin-app/home.js
  max_list_columns: 8
```

__6. Restart the Web App__
You start ApiLogicServer from the web console, *not* from the command line

__6. Run the application__

You can open the Admin App in your browser [http://apilogicserver.pythonanywhere.com/admin-app/index.html](http://apilogicserver.pythonanywhere.com/admin-app/index.html).


You can use ```curl```:  
```  
curl -X GET "http://ApiLogicServer.pythonanywhere.com/api/employees/?include=office%2Cparent%2CEmployeeList%2CCustomerList&fields%5BEmployee%5D=employeeNumber%2ClastName%2CfirstName%2Cextension%2Cemail%2CofficeCode%2CreportsTo%2CjobTitle&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=employeeNumber%2ClastName%2CfirstName%2Cextension%2Cemail%2CofficeCode%2CreportsTo%2CjobTitle%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"  
```
