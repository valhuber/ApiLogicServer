This page does _not_ address created projects, rather, it is about the API Logic Server system used to create projects.  It is for those who want to extend the product or understand how it works, not for those simply using the product.

# How to Install it

## Obtain the projects from GitHub

To create the projects:

1. Create an empty folder (e.g., `~/dev`)
2. Download and run [the install-ApiLogicServer-dev procedure](https://github.com/valhuber/ApiLogicServer/blob/main/install-ApiLogicServer-dev.sh) (note: Windows users use `install-ApiLogicServer-dev.ps1`), e.g.:

```bash title="Install API Logic Server Development environment"
cd ~/dev  # project directories created here
sh install-ApiLogicServer-dev.sh vscode
```

  * This will use `git clone` to create folders in `dev:` ApiLogicServer, safrs-react-admin, and servers.  It's basically straightforward, _though note_ the `cp` command which copies the `safrs-react-admin` runtime to API Logic Server for subsequent creation of API Logic Projects:

```bash
    mkdir servers    # good place to create ApiLogicProjects
    git clone https://github.com/valhuber/ApiLogicServer
    git clone https://github.com/thomaxxl/safrs-react-admin
    cd ApiLogicServer
    cp -r ../safrs-react-admin/build api_logic_server_cli/create_from_model/safrs-react-admin-npm-build
```

## Open `~/dev/ApiLogicServer` in your IDE

`install-ApiLogicServer...` will create a project, and open it VS Code or PyCharm.

Python requires a virtual environment; the procedure differs for `vscode` vs. `charm`:

* `vscode` projects are created with a `venv` and are ready to run the Launch Configurations to create the sample
* `charm` projects require that you create the `venv` with the PyCharm

It should look something like this:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/dev-project.png?raw=true"></figure>

## Create the Sample (`~/dev/servers/ApiLogicProject`)

Once in your IDE, you can run the pre-defined launch configuration `0 - Create and Run ApiLogicProject` to create and run the sample.  This creates `~/dev/servers/ApiLogicProject`.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/vscode/dev-run.png?raw=true"></figure>


## Develop / Debug admin app

Once you have created the API Logic Project, you can restart the server like this (it is _not_ necessary to recreate the sample each time you run):

```bash title="Start API Logic Project"
cd ~/dev/servers/ApiLogicProject
python3 api_logic_server_run.py
```

You can obtain an editable version of the admin app like this:

```bash title="Get Data Provider"
cd ~/dev/safrs-react-admin
git clone https://github.com/thomaxxl/rav3-jsonapi-client # modified data provider used, installed in the project root
```

Then, to debug (with server running):

```bash title="Execute debug version of admin app"
npm install
npm run build

npm start
```

To make this the runtime used to create API Logic Projects:

```bash title="Update ApiLogicServer to use your admin app"
cp -a /build/. ../ApiLogicServer/api_logic_server_cli/create_from_model/admin/
```

&nbsp;

# Created API Logic Project Structure

For reference, projects are created with this structure:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png?raw=true"></figure>

To create using the source code (e.g, from an IDE), using the ```venv``` created from above:

```bash
(venv) val@Vals-MacBook-Pro-16 ApiLogicServer % python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project

(venv) val@Vals-MacBook-Pro-16 ApiLogicServer % python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project

Welcome to API Logic Server, 5.02.25

SQLAlchemy Database URI [default = nw.sqlite, ? for help]: 


Creating ApiLogicServer with options:
  --db_url=default = nw.sqlite, ? for help
  --project_name=~/Desktop/test_project   (pwd: /Users/val/dev/ApiLogicServer)
  --api_name=api
  --admin_app=True
  --react_admin=False
  --flask_appbuilder=False
  --from_git=
  --run=False
  --host=localhost
  --port=5656
  --not_exposed=ProductDetails_V
  --open_with=
  --use_model=
  --favorites=name description
  --non_favorites=id
  --extended_builder=
  --multi_api=False

ApiLogicServer 5.02.25 Creation Log:
0. Using Sample DB from: sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/database/nw-gold.sqlite
1. Delete dir: /Users/val/Desktop/test_project
2. Create Project copy /Users/val/dev/ApiLogicServer/api_logic_server_cli/project_prototype -> /Users/val/Desktop/test_project
.. ..Copy in nw customizations: logic, custom api, readme, tests, admin app
.. ..Copied sqlite db to: sqlite:////Users/val/Desktop/test_project/database/db.sqlite and updated db_uri in /Users/val/Desktop/test_project/config.py
.. .. ..Using nw sample db: /Users/val/dev/ApiLogicServer/api_logic_server_cli/database/nw-gold.sqlite
3. Create/verify database/models.py, then use that to create api/ and ui/ models
 a.  Create Models - create database/models.py, using sqlcodegen for database: sqlite:////Users/val/Desktop/test_project/database/db.sqlite
.. .. ..Create resource_list - dynamic import database/models.py, inspect each class in /Users/val/Desktop/test_project/database
.. .. ..setting cascade delete for sample database database/models.py
 b.  Create api/expose_api_models.py from models
 c.  Create ui/admin/admin.yaml from models
.. .. ..Create ui/admin copy safrs-react-admin: /Users/val/dev/ApiLogicServer/api_logic_server_cli/create_from_model/safrs-react-admin-npm-build -> /Users/val/Desktop/test_project/ui/safrs-react-admin
.. .. ..Write /Users/val/Desktop/test_project/ui/admin/admin.yaml
.. ..ui/basic_web_app creation declined
4. Final project fixup
 b.   Update api_logic_server_run.py with project_name=~/Desktop/test_project and api_name, host, port
 c.   Fixing api/expose_services - port, host
 d.   Updated customize_api_py with port=5656 and host=localhost
 e.   Updated python_anywhere_wsgi.py with /Users/val/Desktop/test_project


ApiLogicProject customizable project created.  Next steps:
==========================================================

Run API Logic Server:
  cd ~/Desktop/test_project;  python api_logic_server_run.py

Customize using your IDE:
  code ~/Desktop/test_project  # e.g., open VSCode on created project
  Establish your Python environment - see ../Quick-Start#project-execution


(venv) val@Vals-MacBook-Pro-16 ApiLogicServer % 
```

&nbsp;

# Creation Internals

The ApiLogicServer source code looks like this:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/apilogicserver-ide.png?raw=true"></figure>

Execution begins at ```ApiLogicServer/api_logic_server_cli/cli.py```.  It gathers command line arguments, and proceeds to ```def api_logic_server(<cmdline-args):```, which operates as described in the sections below.

### 1. Delete Dir
The target project directory is deleted.  This does not work on Windows, which requires the directory to not exist.

### 2. Create Project - copy or ```git clone```
The basic project structure is then created, either by a directory copy or ```git clone```.  By default, project is created from ```ApiLogicServer/prototype```.

#### 2a. Customize
With limited flexibility, you can provide your own ```from-git``` url/path.

#### NW Examples
For demonstration purposes, the system copies pre-defined logic and services so you can explore them.  These are copied from the ```api_logic_server_cli``` directory,  This is indicated by the following console log entry:

```
.. ..Append logic/declare_logic.py with pre-defined nw_logic, rpcs
```

### 3. Create/verify `database/models.py`, then use that to create api/ and ui/ models

The main driver instantiates `create_from_models/model_creation_services`, whose constructor calls `create_models`.  Described below, this provides access to the model, plus verious services to do things like return favorite fields, joins, etc.

The main driver then executes `invoke_creators` which calls the `create_from_models` modules to create api and ui models, based on the `create_from_models/model_creation_services` object.  Before writing `models.py`, import fixes are made in `fix_generated`.

Here is the key excerpt of the main driver in `api_logic_server_cli/cli.py`:

```
    print(f'3. Create/verify database/models.py, then use that to create api/ and ui/ models')
    model_creation_services = CreateFromModel(  ...)
    fix_database_models__inject_db_types(project_directory, db_types)
    invoke_creators(model_creation_services)  # creates api/expose_api_models, ui/admin & basic_web_app
```

### 3a. Create Models - create ```database/models.py``` 
Here is the doc of `create_from_model/model_creation_services#create_models`,
called to read the schema and create ```database/models.py```:

<pre>
        Create models.py (using sqlacodegen,  via expose_existing.expose_existing_callable).

        Called on creation of CreateFromModel.__init__.

        It creates the `models.py` file, and loads `self.resource_list` used by creators to iterate the model.

            1. It calls `expose_existing-callable.create_models_from_db`:
                * It returns the `models_py` text now written to the projects' `database/models.py`.
                * It uses a modification of [sqlacodgen](https://github.com/agronholm/sqlacodegen), by Alex Grönholm -- many thanks!
                    * An important consideration is disambiguating multiple relationships between the same w tables
                        * See `nw-plus` relationships between `Department` and `Employee`.
                        * [See here](../Sample-Database) for a database diagram.
                    * It transforms database names to resource names - capitalized, singular
                        * These (not table names) are used to create api and ui model

            2. It then calls `create_resource_list_from_safrs`, to create the `resource_list`
                * This is the meta data iterated by the creation modules to create api and ui model classes.
                * Important: models are sometimes _supplied_ (`use_model`), not generated, because:
                    * Many DBs don't define FKs into the db (e.g. nw.db).
                    * Instead, they define "Virtual Keys" in their model files.
                    * To leverage these, we need to get resource Metadata from model classes, not db

        :param abs_db_url:  the actual db_url (not relative, reflects sqlite [nw] copy)
        :param project: project directory

        """
</pre>

#### Create `resource_list` - dynamic import database/models.py, inspect each class
Called from `create_models`', this dynamically imports
the created (or, rebuild, the existing) `models.py`,
and creates teh `resource_list` used by the creator modules.

> create_resource_model_from_safrs is a complex process due to dynamic import of models.py - failures may manifest here.

#### If option: ```use_model```
SQL dialects and bugs can result in failures here.  The system therefore enables you to provide your own model, as described in [TroubleShooting](wiki/Troubleshooting#manual-model-repair).

If you elect this option, you should see the following in the console log:
```
.. ..Copy /Users/val/dev/ApiLogicServer/tests/models.py to /Users/val/dev/servers/sqlserver-types/database/models.py
```

#### Extensible generate from models
The ```models.py``` file provides `resource_list` metadata used to create APIs, a basic web app, and a react-admin app (steps 31, 3b and 3c), as shown below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/apilogicserver-ide-create-from-model.png?raw=true"></figure>

### 3b. Create ```api/expose_api_models.py``` (import / iterate models) 

The first creator to be invoked is `create_from_model/api_expose_api_models` to create `expose_api_models`.

It uses `model_creation_services.resource_list` to create `create_from_model/model_creation_services#create_models`.  It is straightforward.

The remaining steps make small updates to the created code to insert database names.

### 3c. Create ```ui/admin app``` (import / iterate models)

The main thing in `ui_admin_creator` is to create a ```admin.yaml``` file - an executable description of the pages and content.

### 3d. Create ```ui/basic_web_app``` with command: ```flask fab create-app```
The system then creates the basic web app.  The main thing here is to create the ```views.py``` file.

&nbsp;

# Docker Startup

You can review the dockerfile on `github`.  Note that the normal operation is to start a terminal session as the last step:

```bash
CMD ["bash"]
```

When bash sessions are started, Linux runs `.bashrc`.  This checks for environment variables which can be used to load an existing project from git, and run it.  (Note: this defeats the normal terminal startup).  For example, start Docker using `-e` arguments, like this:


```bash
docker run -it --name api_logic_server --rm --net dev-network \
-p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost \
-e APILOGICSERVER_GIT='https://github.com/valhuber/Tutorial-ApiLogicProject.git' \
-e APILOGICSERVER_FIXUP='/localhost/Project-Fixup.sh' \
apilogicserver/api_logic_server
```


Alternatively, you can start Docker specifying an initial command, like this:
```bash
docker run -it --name api_logic_server --rm --net dev-network \
-p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost \
apilogicserver/api_logic_server \
sh /home/api_logic_server/bin/run-project.sh https://github.com/valhuber/Tutorial-ApiLogicProject.git /localhost/Project-Fixup.sh
```

In both cases, the git load is performed by `bin/run-project.sh`, which you can explore on github.