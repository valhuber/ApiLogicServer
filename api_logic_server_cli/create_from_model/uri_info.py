import sys

uri_info = [
    'Examples:',
    '  ApiLogicServer create-and-run',
    '  ApiLogicServer create-and-run --db_url=sqlite:////Users/val/dev/todo_example/todos.db --project_name=todo',
    '  ApiLogicServer create-and-run --db_url=sqlite:///c:\ApiLogicServer\\nw.sqlite --project_name=nw',
    '  ApiLogicServer create-and-run --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels '
    '--project_name=/localhost/docker_db_project',
    '  ApiLogicServer create-and-run --db_url=mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?'
    'driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no',
    '  ApiLogicServer create-and-run --db_url=postgresql://postgres:p@10.0.0.234/postgres',
    '  ApiLogicServer create --project_name=my_schema --db_url=postgresql://postgres:p@localhost/my_schema',
    '  ApiLogicServer create --db_url=postgresql+psycopg2:'
    '//postgres:password@localhost:5432/postgres?options=-csearch_path%3Dmy_db_schema',
    '  ApiLogicServer create --project_name=Chinook \\',
    '    --host=ApiLogicServer.pythonanywhere.com --port= \\',
    '    --db_url=mysql+pymysql://ApiLogicServer:***@ApiLogicServer.mysql.pythonanywhere-services.com/ApiLogicServer\$Chinook',
    '',
    'Where --db_url is one of...',
    '   <default>                     Sample DB                    - https://apilogicserver.github.io/Docs/Sample-Database/',
    '   nw-                           Sample DB, no customizations - add later with perform_customizations.py',
    '   <SQLAlchemy Database URI>     Your own database            - https://docs.sqlalchemy.org/en/14/core/engines.html',
    '                                      Other URI examples:     - https://apilogicserver.github.io/Docs/Database-Connectivity//',
    ' ',
    'Docs: https://apilogicserver.github.io/Docs/'
]


def print_uri_info():
    """
    Creates and optionally runs a customizable Api Logic Project, Example

    URI examples, Docs URL
    """
    header = [
        '',
        'Creates and optionally runs a customizable Api Logic Project',
        ''
    ]

    for each_line in header:
        sys.stdout.write(each_line + '\n')
    for each_line in uri_info:
        sys.stdout.write(each_line + '\n')
    sys.stdout.write('\n')
