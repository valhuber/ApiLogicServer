This page describes key technical background on using API Logic Server.  These procedures presume that you have performed the following:

* [Installed](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start#Install-Guide) ApiLogicServer

* Run the [Quick Start](https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start) to familiarize yourself with how to create, run and debug projects

&nbsp;

# Customizing ApiLogicProjects
You will typically want to customize and extend the created project.  Edit the files described in the subsections below.

The 2 indicated files in the tree are the Python files that run for the Basic Web App and the API Server.

Projects are created from a [system-supplied prototype](https://github.com/valhuber/ApiLogicServer/tree/main/prototype).  You can use your own prototype from git (or a local directory) using the ```from_git``` parameter.

&nbsp;

### Project Structure

When you create an ApiLogicProject, the system creates a project like this that you customize in your API:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/generated-project.png?raw=true"></figure>

You will observe that the projects are rather small.  That is because the syste creates _models_ that define _what, not now_.  Explore the project and you will find it easy to understand the API, data model, app and logic files.

Note the entire project is file-based, which makes it easy to perform typical project functions such as source control, diff, merge, code reviews etc.

&nbsp;

### Preserving Customizations over Iterations
Your customizations are made to the files in the following sections.  These are separate files from the core model and api files, so that (if you wish) you can recreate the system from a revised schema, then simply copy over the files described below.

&nbsp;

### Customize the API with ```expose_services.py```: add RPCs, Services

Initially the API exposes all your tables as collection endpoints.  You can add additional endpoints by editing ```expose_services.py```, as illustrated by the Add Service example.  For more on customization, see [SAFRS Customization docs](https://github.com/thomaxxl/safrs/wiki/Customization).

&nbsp;

### Customize the Model: add relationships, derived attributes
Model files describe your database tables.  Each database has extensions which can introduce issues in model generation, so facilities are described in [Troubleshooting](Troubleshooting) to edit models and rebuild.

&nbsp;

#### Edit ```models.py```: referential integrity (e.g., sqlite)

[Rebuild support](#rebuilding) enables you to rebuild your project, preserving customizations you have made to the api, logic and app.  You can rebuild from the database, or from the model.

This enables you to edit the model to specify aspects not captured in creating the model from your schema.  For example, sqlite often is not configured to enforce referential integrity.  SQLAlchemy provides  support to fill such gaps.

For example, try to delete the last order for the first customer.  You will encounter an error since the default is to nullify foreign keys, which in this case is not allowed.

You can fix this by altering your ```models.py:```

```
    OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=True, backref='Order')
```

Your api, logic and ui are not (directly) dependent on this setting, so there is no need to rebuild; just restart the server, and the system will properly cascade the `Order` delete to the `OrderDetail` rows.  Note further that logic will automatically adjust any data dependent on these deletions (e.g. adjust sums and counts).

&nbsp;

#### Edit ```model_ext.py```: add relationships, derived attributes
In addition, you may wish to edit ```models_ext.py```, for example:

* to define [relationships](https://github.com/valhuber/LogicBank/wiki/Managing-Rules#database-design), critical for multi-table logic, APIs, and web apps

* to describe derived attributes, so that your API, logic and apps are not limited to the physical data model

&nbsp;

#### Use Alembic to update database schema from model

As of release 5.02.03, created API Logic Projects integrate [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) to perform database migrations.
* Manual: create migration scripts by hand, or
* Autogenerate: alter your `database/models.py`, and have alembic create the migration scripts for you

Preconfiguration includes:
* initialized `database/alembic` directory
* configured `database/alembic/env.py` for autogenerations
* configured `database/alembic.ini` for directory structure

See the `readme` in your `database/alembic` for more information.

&nbsp;


### Customizing the Admin App

```admin.yaml``` describes form layout.  Customize it, for example to [control column layouts](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App#customization), etc.

&nbsp;

## Rebuilding

Ignoring the boxes labeled "rebuild", the key elements of the creation process are illustrated below:

* the system reads the database schema to create `models.py`


* `models.py` drives the creation process


* you customize the created project, mainly by altering the files on the far right

As shown in the diagram, creation is always driven from `models.py.`  Models differ from physical schemas in important ways:
* the system ensure that class names are capitalized and singular


* there are good reasons to customize `models.py`:
   * to add foreign keys missing in the database - these are critical for multi-table apis and applications
   * to provide better naming

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/extended_builder/rebuild-from.png?raw=true"></figure>

You can rebuild your project, preserving customizations (including any additional files you have created).  You have 2 alternatives, depending on where you choose the _"source of truth"_ for your database:

| Source of Truth | Means | Use `rebuild` option |
| :--- |:---|:---|
| Database | The schema is the source of truth<br><br>It includes all the foreign keys | `rebuild-from-datatabase:` rebuilds the files shown in blue and purple. |
| Model | Model is the source of truth<br><br>Use SQLAlchemy services to drive changes into the database |`rebuild-from-model:` rebuilds the files shown in blue |

Note that `ui/admin/admin.yaml` is never overwritten (the dotted line 
means it is written on only on `create` commands).  After rebuilds, merge the new `ui/admin/admin-created.yaml` into your customized `admin.yaml.`

&nbsp;

### API and Admin App merge updates

As of release 5.02.03, ```rebuild``` services provide support for updating customized API and Admin:

| System Object | Support |
| :---  | :--- |
| API | `api/expose_api_models_created.py` created with new `database/models.py` classes |
| Admn App | `ui/admin/admin-merge.yaml` is the merge of `ui/admin/admin.yaml` and new `database/models.py` classes |

Review the altered files, edit (if required), and copy them over the original files.

&nbsp;


# Data Model Classes

Most of API Logic Server functionality derives from the data model classes created from your schema when you create your project.  Here is an example:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/model/relns-admin.png?raw=true"></figure>

Observe that:

1. A __class__ is created for each table.  The name (e.g. `OrderDetail`) is derived from the table name, but is capitalized and singlularized


2. The __table name__ is from your schema, this corresponds to a resource collection in the API


3. Relationships are created on the _one_ side of one-to-many relationships.  The __relationship name__ is the target class + "List", and is available in Python (`items = anOrder.OrderDetailList`).  These names are used in your UI admin apps, and your API


4. Relationships have 2 names; the __backref__ name is now the _many_ side refers to the _one" side (e.g., anOrder = anOrderDetail.order`)


Relationship names are also part of your API:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/model/relns-api.png?raw=true"></figure>

&nbsp;

# User Extensible Creation

The **`extended_builder`** option enables you to extend the creation process. It is intended to accommodate cases where DBMSs provide proprietary features - such as _Table Valued Functions_ (TVFs) - that should be exposed as APIs.

Install as usual, and create your project using the `extended_builder` option, e.g:

```
ApiLogicServer run --db_url='mssql+pyodbc://sa:posey386!@localhost:1433/SampleDB?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no' \
   --extended_builder=extended_builder.py \
   --project_name=TVF
```

Or, use the default extended_builder:

```
ApiLogicServer run --db_url='mssql+pyodbc://sa:posey386!@localhost:1433/SampleDB?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no' \
   --extended_builder='*' \
   --project_name=TVF
```

to designate a file that implements your builder. After the creation process, the system will invoke `extended_builder(db_url, project_directory)` so you can add / alter files as required.

> Full automation for specific DBMS features was considered, but could not conceivably accommodate all the DBMS features that might be desired. We therefore provide this _extensible automation_ approach.

Let's illustrate the use of extensible automation with this example.  Create the sample project as follows:

1.  Acquire [this sql/server docker database](https://github.com/valhuber/ApiLogicServer/wiki/Testing#northwind---sqlserver--docker)
2.  Create the project

```
docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

ApiLogicServer create --project_name=/localhost/sqlserver-types --db_url=mssql+pyodbc://sa:posey386!@localhost:1433/SampleDB?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=no
```

This uses an example extended builder can be found [here](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/extended_builder.py). You can copy this file to a local directory, alter it as required, and specify its location in the CLI argument above. It is loosely based on [this example](https://gist.github.com/thomaxxl/f8cff63a80979b4a4da70fd835ec2b99).

The interface to ApiLogicServer requires that you provide an `extended_builder(db_url, project_directory)` function, like this (the rest is up to you):

```bash
def extended_builder(db_url, project_directory):
    """ called by ApiLogicServer CLI -- scan db_url schema for TVFs, create api/tvf.py
            for each TVF:
                class t_<TVF_Name> -- the model
                class <TVF_Name>   -- the service
        args
            db_url - use this to open the target database, e.g. for meta data
            project_directory - the created project... create / alter files here

    """
    print(f'extended_builder.extended_builder("{db_url}", "{project_directory}"')
    tvf_builder = TvfBuilder(db_url, project_directory)
    tvf_builder.run()
```

This particular example creates this [tvf file](https://github.com/valhuber/ApiLogicServer/blob/main/tvf.txt) in the api folder.

Updates `api/customize_api.py` to expose it, as shown below:

![](https://github.com/valhuber/ApiLogicServer/wiki/images/extended_builder/activate.png?raw=true)


This example illustrates the extended builder approach; the resultant services runs as shown below.

> It does not deal with many data types.

It generates Swagger, with arguments:

![](https://github.com/valhuber/ApiLogicServer/wiki/images/extended_builder/swagger.png?raw=true)

You can run it with this cURL:

```bash
curl -X POST "http://localhost:5656/udfEmployeeInLocation/udfEmployeeInLocation" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/json" -d "{  \"location\": \"Sweden\"}"
```

returns the expected data:

```json
{
  "result": [
    2,
    "Nikita",
    "Sweden"
  ]
}
```

&nbsp;

# Virtual Environment
This section applies only to `pip` installs.  Docker based installs eliminate such environment issues, and are therefore recommended.

You created a virtual environment when you installed ApiLogicServer.  This ```venv``` will work for all of your created ApiLogicServer projects, or you can use a per-project ```venv``` as described below.

Alternatively, you can create a self-contained virtual environment for each project.
The created project contains a ```requirements.txt``` used to create a [virtual environment](https://docs.python.org/3/library/venv.html).
You can create it in the usual manner:

```sh
cd ApiLogicProject
python3 -m venv venv       # may require python -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
pip install -r requirements.txt
```

&nbsp;

# Runtime Architecture

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/Architecture.png?raw=true"></figure>

ApiLogicServer creates a standard Flask-based 3-tier architecture:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) enables you to write custom web apps, and custom api end points

    * ApiLogicServer automatically creates an Admin App using
[safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin), useful for back-office admin access and prototyping

* [SAFRS](https://github.com/thomaxxl/safrs/wiki) provides the API, which you can use to support mobile apps and internal / external integration

* [SQLAlchemy](https://sqlalchemy-utils.readthedocs.io/en/latest/) provides data access.

* [Logic Bank](https://github.com/valhuber/logicbank#readme) listens for updates, and applies your declared logic, for both API and web app updates.

&nbsp;

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
