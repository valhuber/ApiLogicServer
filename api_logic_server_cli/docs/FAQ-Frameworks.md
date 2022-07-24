There are many excellent frameworks for developing web apps.  Here is an [excellent video](https://www.youtube.com/watch?v=3vfum74ggHE&t=2s){:target="_blank" rel="noopener"}, describing how to create an app using Flask, Django and Fast API.

API Logic Server is designed to provide a significantly faster and simpler __low-code__ way to create database systems:

* __Remarkable speed and simplicity:__ given a database, you get an instant system  - _no training, no coding:_

    * an [API](https://valhuber.github.io/ApiLogicServer/Tutorial/#jsonapi-related-data-filtering-sorting-pagination-swagger){:target="_blank" rel="noopener"}, including filtering, pagination, sorting, related data and swagger
    * a multi-page, multi-table [Admin Web App](https://valhuber.github.io/ApiLogicServer/Tutorial/#admin-app-multi-page-multi-table-automatic-joins){:target="_blank" rel="noopener"}, and 
    * SQLAlchemy model classes

* __Fully Customizable:__ you get a [customizable project](https://valhuber.github.io/ApiLogicServer/Tutorial/#customize-and-debug){:target="_blank" rel="noopener"} you can use in your IDE to create custom services with all the flexibility and power of Python, Flask and SQLAlchemy

* __:trophy: Declarative Business Logic:__ unique spreadsheet-like rules that are [40X more concise than legacy code](https://valhuber.github.io/ApiLogicServer/Logic-Why/#customize-and-debug){:target="_blank" rel="noopener"}, extensible with Python

## Example: todos

The video at the top shows how to create a system from a `todos` database.  You can create this system with API Logic Server like this:

1. Download the [todos database](https://github.com/valhuber/ApiLogicServer/blob/main/examples/dbs/todos.db){:target="_blank" rel="noopener"}
2. Install API Logic Server:

```bash title="Install API Logic Server  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (also available for Docker)"
python -m venv venv        # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
python -m pip install ApiLogicServer
```
3. Create and run your project
```bash title="Create and Run todos project"
ApiLogicServer create-and-run --project_name=todo \
   --db_url=sqlite:////Users/val/dev/todo_example/todos.db 
```

Explore your project in your IDE, using standard services to code, run and debug.