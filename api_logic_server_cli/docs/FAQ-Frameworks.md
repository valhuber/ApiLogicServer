## TL;DR - not a framework, rather a low-code approach for creating systems

There are many excellent frameworks for developing web apps.  They provide tools for writing code to handle API and application events.

API Logic Server is not a framework - it is _built_ on frameworks (Flask currently, more are possible).  It is a __low-code approach__ for creating customizable microservices - Apps, APIs, _and_ the underlying business logic.

&nbsp;

## Frameworks - code based app/api handlers

Frameworks require extensive background in web app development, and significant amounts of code.  The video at the end provides an excellent summary of Flask, FAST API, and Django.  While flexibile, they are _complex and time consuming._

&nbsp;

## API Logic Server - low-code declarative, extensible system creation

API Logic Server is designed to provide a significantly faster and simpler __low-code__ approach for creating database systems:

* __Remarkable speed and simplicity:__ given a database, you get an instant system  - _no training, no coding:_

    * an [API](https://valhuber.github.io/ApiLogicServer/Tutorial/#jsonapi-related-data-filtering-sorting-pagination-swagger){:target="_blank" rel="noopener"}, including filtering, pagination, sorting, related data and swagger
    * a multi-page, multi-table [Admin Web App](https://valhuber.github.io/ApiLogicServer/Tutorial/#admin-app-multi-page-multi-table-automatic-joins){:target="_blank" rel="noopener"}, and 
    * SQLAlchemy model classes

* __Fully Customizable:__ you get a [customizable project](https://valhuber.github.io/ApiLogicServer/Tutorial/#customize-and-debug){:target="_blank" rel="noopener"} you can use in your IDE to create custom services with all the flexibility and power of Python, Flask and SQLAlchemy

* __:trophy: Declarative Business Logic:__ unique spreadsheet-like rules that are [40X more concise than legacy code](https://valhuber.github.io/ApiLogicServer/Logic-Why/#customize-and-debug){:target="_blank" rel="noopener"}, extensible with Python

&nbsp;

## Example: todos  -- 1 command project creation

The video at the top shows how to create a system from a `todos` database.  You can create this system with API Logic Server like this:

1. Download the [todos database](https://github.com/valhuber/ApiLogicServer/blob/main/examples/dbs/todos.db){:target="_blank" rel="noopener"} to your desktop

2. Install API Logic Server:

```bash title="Install API Logic Server  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (also available for Docker)"
cd ~/Desktop
mkdir ApiLogicServer
cd ApiLogicServer
python -m venv venv        # may require python3 -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
python -m pip install ApiLogicServer
```
3. Create and run your project
```bash title="Create and Run todos project&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 command"
ApiLogicServer create-and-run --project_name=todo \
   --db_url=sqlite:////Users/Val/Desktop/todos.db  # explicit path (no ~)
```

Explore your project in your IDE, using standard services to code, run and debug.

&nbsp;

## Appendix - Video Conventional Approach

[This video](https://www.youtube.com/watch?v=3vfum74ggHE&t=2s){:target="_blank" rel="noopener"} provides an excellent summary of Flask, FAST API, and Django.