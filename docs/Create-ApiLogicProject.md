# Project Creation

Use this procedure __for Docker installs:__

```
cd ApiLogicServer  # directory of API Logic Server projects on local host

# Start (install if required) the API Logic Server docker container

docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

$ ApiLogicServer create --project_name=/localhost/ApiLogicProject --db_url=
```

The procedure is similar __for local installs:__
```
cd ApiLogicServer          # your install folder
source venv/bin/activate   # windows venv\Scripts\activate
ApiLogicServer create      # accept default project name, db
```

In either case, the `create` command builds an `ApiLogicProject` - a directory, shown here in VSCode:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/generated-project.png?raw=true"></figure>

  > The procedures above will create the sample project, which we recommend to start with.  You will then want to create a project with your own database.  For that, you will require a [SQLAlchemy URI](https://docs.sqlalchemy.org/en/14/core/engines.html).  You can see some examples:

```bash
ApiLogicServer examples   # prints a list of url examples
```