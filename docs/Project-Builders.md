

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

1.  Acquire [this sql/server docker database](../Testing#northwind---sqlserver--docker)
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

![](https://github.com/valhuber/apilogicserver/wiki/images/extended_builder/activate.png?raw=true)


This example illustrates the extended builder approach; the resultant services runs as shown below.

> It does not deal with many data types.

It generates Swagger, with arguments:

![](https://github.com/valhuber/apilogicserver/wiki/images/extended_builder/swagger.png?raw=true)

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
