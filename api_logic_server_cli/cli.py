# -*- coding: utf-8 -*-

'''
CLICK functions for API Logic Server CLI

Main code is api_logic_server.py (PR)
'''

from contextlib import closing

import yaml

temp_created_project = "temp_created_project"   # see copy_if_mounted

import socket
import subprocess
from os.path import abspath
from os.path import realpath
from pathlib import Path
from shutil import copyfile
import shutil
import importlib.util

from flask import Flask

import logging
import datetime
from typing import NewType
import sys
import os
import importlib
import click

def get_api_logic_server_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    return str(python_path)


# print("sys.path.append(get_api_logic_server_dir())\n",get_api_logic_server_dir())
sys.path.append(get_api_logic_server_dir())  # e.g, on Docker: export PATH="/home/api_logic_server/api_logic_server_cli"
api_logic_server_path = os.path.dirname(get_api_logic_server_dir())  # e.g: export PATH="/home/api_logic_server"
sys.path.append(api_logic_server_path)
from create_from_model.model_creation_services import ModelCreationServices
import create_from_model.api_logic_server_utils as create_utils
import api_logic_server_cli.create_from_model.uri_info as uri_info
import api_logic_server_cli.api_logic_server as PR  # ProjectRun (main class)

api_logic_server_info_file_name = get_api_logic_server_dir() + "/api_logic_server_info.yaml"

api_logic_server_info_file_dict = {}  # last-run (debug, etc) info
""" contains last-run info, debug switches to show args, etc """

if Path(api_logic_server_info_file_name).is_file():
    api_logic_server_info_file = open(api_logic_server_info_file_name)
    api_logic_server_info_file_dict = yaml.load(api_logic_server_info_file, Loader=yaml.FullLoader)
    api_logic_server_info_file.close()


last_created_project_name = api_logic_server_info_file_dict.get("last_created_project_name","")
default_db = "default = nw.sqlite, ? for help"
default_project_name = "ApiLogicProject"
default_fab_host = "localhost"
os_cwd = os.getcwd()
default_bind_key_url_separator = "-"  # admin app fails with "/" or ":" (json issues?)

if os.path.exists('/home/api_logic_server'):  # docker?
    default_project_name = "/localhost/ApiLogicProject"
    default_fab_host = "0.0.0.0"


def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = '/home/api_logic_server'
    path_result = os.path.isdir(path)  # this *should* exist only on docker
    env_result = "DOCKER" == os.getenv('APILOGICSERVER_RUNNING')
    assert path_result == env_result
    return path_result


'''  exploring no-args, not a clue
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='no_args', default_if_no_args=True)
def main():
    """
    wonder if this can just do something
    """
    click.echo("group execution (never happens)")

# @click.pass_context
@main.command()
@click.option('--config', default=None)
def no_args(config):
    print("no args!!")


@click.group()
@click.pass_context
@main.command("mainZ")
def mainZ(ctx):
    """
    Creates [and runs] logic-enabled Python database API Logic Projects.

\b
    Doc: https://apilogicserver.github.io/Docs

\b
    Examples:

\b
        ApiLogicServer tutorial                                # *** start here ***
        ApiLogicServer create-and-run --db_url= project_name=  # defaults to Northwind
        ApiLogicServer create                                  # prompts for project, db

    Then, customize created API Logic Project in your IDE
    """
    print("Never executed")
'''

@click.group()
@click.pass_context
def main(ctx):
    """
    Creates [and runs] logic-enabled Python database API Logic Projects.

\b
    Doc: https://apilogicserver.github.io/Docs

\b
    Examples:

\b
        ApiLogicServer tutorial                                # <=== Start Here
        ApiLogicServer create-and-run --db_url= project_name=  # defaults to Northwind
        ApiLogicServer create                                  # prompts for project name, db url

    Then, customize created API Logic Project in your IDE
    """
    # click.echo("main - called iff commands supplied")


@main.command("about")
@click.pass_context
def about(ctx):
    """
        Recent Changes, system information.
    """

    print(f'\tInstalled at {abspath(__file__)}\n')
    print(f'\thttps://apilogicserver.github.io/Docs/Tutorial/\n')

    def print_at(label: str, value: str):
        tab_to = 30 - len(label)
        spaces = ' ' * tab_to
        print(f'{label}: {spaces}{value}')

    print("\nPYTHONPATH..")
    for p in sys.path:
        print(".." + p)
    print("")
    print("api_logic_server_info...")
    for key, value in api_logic_server_info_file_dict.items():
        print_at(f'  {key}', value)
    print("")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = f"cannot get local ip from {hostname}"
        log.debug(f"{local_ip}")

    print_at('ApiLogicServer version', PR.__version__)
    print_at('ip (gethostbyname)', local_ip)
    print_at('on hostname', hostname)
    print_at('cwd', os. getcwd())
    print_at("Python version", create_utils.run_command(f'python --version', msg="no-msg"))
    print_at("Docker", is_docker())

    click.echo(
        click.style(PR.recent_changes)
    )


@main.command("welcome")
@click.pass_context
def welcome(ctx):
    """
        Just print version and exit.
    """


@main.command("tutorial")
@click.option('--create',
              default='tutorial',
              help="tutorial or fiddle")
@click.pass_context
def tutorial(ctx, create):
    """
    Creates (updates) Tutorial.

    Contains 3 projects: basic_flask, ApiLogicProject, ApiLogicProjectNoCustomizations
    
    example: 
    cd ApiLogicProject  # any empty folder, perhaps where ApiLogicServer is installed
    ApiLogicServer tutorial
    
    """
    project_name=os.getcwd()
    if project_name == get_api_logic_server_dir():  # for ApiLogicServer dev (from |> Run and Debug )
        project_name = str(Path(project_name).parent.parent.joinpath("Org-ApiLogicServer"))
    else:
        project_name = str(Path(project_name))

    project = PR.ProjectRun(command="tutorial", 
              project_name=project_name, 
              db_url="",
              execute=False
              )
    project.tutorial(msg="Creating:", create=create)
    log.info("")


@main.command("create")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")  # option text shown on create --help
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=False,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--multi_api/--no_multi_api',
              default=False, is_flag=True,
              help="Create multiple APIs")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--include_tables',
              default=f'',
              help="yml for include: exclude:")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def create(ctx, project_name: str, db_url: str, not_exposed: str, api_name: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           include_tables: str,
           multi_api: click.BOOL,
           infer_primary_key: click.BOOL):
    """
        Creates new customizable project (overwrites).
    """
    global command
    db_types = ""
    PR.ProjectRun(command="create", project_name=project_name, db_url=db_url, api_name=api_name,
                    not_exposed=not_exposed,
                    run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                    flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                    react_admin=react_admin, admin_app=admin_app,
                    favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                    extended_builder=extended_builder, include_tables=include_tables,
                    multi_api=multi_api, infer_primary_key=infer_primary_key)


@main.command("create-and-run")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=True,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
@click.option('--multi_api/--no_multi_api',
              default=False, is_flag=True,
              help="Create multiple APIs")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def create_and_run(ctx, project_name: str, db_url: str, not_exposed: str, api_name: str,
        from_git: str,
        # db_types: str,
        open_with: str,
        run: click.BOOL,
        admin_app: click.BOOL,
        flask_appbuilder: click.BOOL,
        react_admin: click.BOOL,
        use_model: str,
        host: str,
        port: str,
        swagger_host: str,
        favorites: str, non_favorites: str,
        extended_builder: str,
        multi_api: click.BOOL,
        infer_primary_key: click.BOOL):
    """
        Creates new project and runs it (overwrites).
    """
    global command  # TODO drop this global
    db_types = ""
    PR.ProjectRun(command="create-and-run", project_name=project_name, db_url=db_url, api_name=api_name,
                    not_exposed=not_exposed,
                    run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                    flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                    react_admin=react_admin, admin_app=admin_app,
                    favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                    extended_builder=extended_builder, multi_api=multi_api, infer_primary_key=infer_primary_key)


@main.command("rebuild-from-database")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=False,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context
def rebuild_from_database(ctx, project_name: str, db_url: str, api_name: str, not_exposed: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           infer_primary_key: click.BOOL):
    """
        Updates database, api, and ui from changed db.

\b
        ex
\b
        ApiLogicServer rebuild-from-database --project_name=~/dev/servers/ApiLogicProject --db_url=nw

    """
    db_types = ""
    PR.ProjectRun(command="rebuild-from-database", project_name=project_name, db_url=db_url, api_name=api_name,
                    not_exposed=not_exposed,
                    run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                    flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                    react_admin=react_admin, admin_app=admin_app,
                    favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                    extended_builder=extended_builder, multi_api=False, infer_primary_key=infer_primary_key)


@main.command("add-db") 
@click.option('--db_url',
              default=f'todo',
              prompt="Database url",
              help="Connect new database here") # TODO
@click.option('--bind_key',
              default=f'Alt',
              prompt="Bind key",
              help="Add new bind key here") # TODO
@click.option('--bind_key_url_separator',
              default=default_bind_key_url_separator,
              help="bindkey / class name url separator")
@click.option('--project_name',
              default=f'',
              help="Project location")
@click.option('--api_name',
              default="api",
              help="api prefix name")
@click.pass_context # Kat
def add_db(ctx, db_url: str, bind_key: str, bind_key_url_separator: str, api_name: str, project_name: str):
    """
    Adds db (model, binds, api, app) to curr project.
    
    example: 

    cd existing_project

    ApiLogicServer add-db --db-url="todo" --bind-key="Todo"
    
    """
    if project_name == "":
        project_name=os.getcwd()
        if project_name == get_api_logic_server_dir():  # for ApiLogicServer dev (from |> Run and Debug )
            project_name = str(
                Path(project_name).parent.parent.joinpath("servers").joinpath("ApiLogicProject")
            )
    if db_url == "auth":
        bind_key = "authentication"
    PR.ProjectRun(command="add_db", 
              project_name=project_name, 
              api_name=api_name, 
              db_url=db_url, 
              bind_key=bind_key,
              bind_key_url_separator=bind_key_url_separator
              )
    print("DB Added")


@main.command("add-auth") 
@click.option('--bind_key_url_separator',
              default=default_bind_key_url_separator,
              help="bindkey / class name url separator")
@click.option('--project_name',
              default=f'',
              help="Project location")
@click.option('--api_name',
              default="api",
              help="api prefix name")
@click.pass_context
def add_security_cmd(ctx, bind_key_url_separator: str, api_name: str, project_name: str):
    """
    Adds authorization/authentication to curr project.
    
    example: 

    cd existing_project

    ApiLogicServer add-auth
    
    """
    if project_name == "":
        project_name=os.getcwd()
        if project_name == get_api_logic_server_dir():  # for ApiLogicServer dev (from |> Run and Debug )
            project_name = str(
                Path(project_name).parent.parent.joinpath("servers").joinpath("ApiLogicProject")
            )
    db_url = "auth"
    bind_key = "authentication"
    project = PR.ProjectRun(command="add_security", 
              project_name=project_name, 
              api_name=api_name, 
              db_url=db_url, 
              bind_key=bind_key,
              bind_key_url_separator=bind_key_url_separator,
              execute=False
              )
    project.project_directory, project.api_name, project.merge_into_prototype = \
        create_utils.get_project_directory_and_api_name(project)
    project.project_directory_actual = os.path.abspath(project.project_directory)  # make path absolute, not relative (no /../)
    project.project_directory_path = Path(project.project_directory_actual)
    models_py_path = project.project_directory_path.joinpath('database/models.py')
    project.abs_db_url, project.nw_db_status, project.model_file_name = create_utils.get_abs_db_url("0. Using Sample DB", project)
    is_nw = False
    if create_utils.does_file_contain(search_for="CategoryTableNameTest", in_file=models_py_path):
        is_nw = True
    project.add_sqlite_security(msg="Adding Security", is_nw=is_nw)
    log.info("")


@main.command("add-cust") 
@click.option('--bind_key_url_separator',
              default=default_bind_key_url_separator,
              help="bindkey / class name url separator")
@click.option('--project_name',
              default=f'',
              help="Project location")
@click.option('--api_name',
              default="api",
              help="api prefix name")
@click.pass_context
def add_cust(ctx, bind_key_url_separator: str, api_name: str, project_name: str):
    """
    Adds customizations to northwind project.
    
    example: 
    cd existing_project
    ApiLogicServer add-cust
    
    """
    if project_name == "":
        project_name=os.getcwd()
        if project_name == get_api_logic_server_dir():  # for ApiLogicServer dev (from |> Run and Debug )
            project_name = str(
                Path(project_name).parent.parent.joinpath("servers").joinpath("NW_NoCust")
            )
    db_url = "auth"
    bind_key = "authentication"
    project = PR.ProjectRun(command="add_cust", 
              project_name=project_name, 
              api_name=api_name, 
              db_url=db_url,
              execute=False
              )
    project.project_directory, project.api_name, project.merge_into_prototype = \
        create_utils.get_project_directory_and_api_name(project)
    project.project_directory_actual = os.path.abspath(project.project_directory)  # make path absolute, not relative (no /../)
    project.project_directory_path = Path(project.project_directory_actual)
    models_py_path = project.project_directory_path.joinpath('database/models.py')
    project.abs_db_url, project.nw_db_status, project.model_file_name = create_utils.get_abs_db_url("0. Using Sample DB", project)
    is_nw = False
    if create_utils.does_file_contain(search_for="CategoryTableNameTest", in_file=models_py_path):
        is_nw = True
    else:
        raise Exception("Customizations are northwind-specific - this does not appear to be a northwind database")
    project.add_nw_customizations()


@main.command("rebuild-from-model")
@click.option('--project_name',
              default=f'{default_project_name}',
              prompt="Project to create",
              help="Create new directory here")
@click.option('--db_url',
              default=f'{default_db}',
              prompt="SQLAlchemy Database URI",
              help="SQLAlchemy Database URL - see above\n")
@click.option('--api_name',
              default=f'api',
              help="Last node of API Logic Server url\n")
@click.option('--from_git',
              default="",
              help="Template clone-from project (or directory)")
@click.option('--run', is_flag=True,
              default=False,
              help="Run created project")
@click.option('--open_with',
              default='',
              help="Open created project (eg, charm, atom)")
@click.option('--not_exposed',
              default="ProductDetails_V",
              help="Tables not written to api/expose_api_models")
@click.option('--admin_app/--no_admin_app',
              default=True, is_flag=True,
              help="Creates ui/react app (yaml model)")
@click.option('--flask_appbuilder/--no_flask_appbuilder',
              default=False, is_flag=True,
              help="Creates ui/basic_web_app")
@click.option('--react_admin/--no_react_admin',
              default=False, is_flag=True,
              help="Creates ui/react_admin app")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.option('--use_model',
              default="",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.option('--extended_builder',
              default=f'',
              help="your_code.py for additional build automation")
@click.option('--infer_primary_key/--no_infer_primary_key',
              default=False, is_flag=True,
              help="Infer primary_key for unique cols")
@click.pass_context # Kat
def rebuild_from_model(ctx, project_name: str, db_url: str, api_name: str, not_exposed: str,
           from_git: str,
           # db_types: str,
           open_with: str,
           run: click.BOOL,
           admin_app: click.BOOL,
           flask_appbuilder: click.BOOL,
           react_admin: click.BOOL,
           use_model: str,
           host: str,
           port: str,
           swagger_host: str,
           favorites: str, non_favorites: str,
           extended_builder: str,
           infer_primary_key: click.BOOL):
    """
        Updates database, api, and ui from changed models.
    """
    db_types = ""
    PR.ProjectRun(command="rebuild-from-model", project_name=project_name, db_url=db_url, api_name=api_name,
                    not_exposed=not_exposed,
                    run=run, use_model=use_model, from_git=from_git, db_types=db_types,
                    flask_appbuilder=flask_appbuilder,  host=host, port=port, swagger_host=swagger_host,
                    react_admin=react_admin, admin_app=admin_app,
                    favorites=favorites, non_favorites=non_favorites, open_with=open_with,
                    extended_builder=extended_builder, multi_api=False, infer_primary_key=infer_primary_key)


@main.command("run")
@click.option('--project_name',
              default=f'{last_created_project_name}',
              prompt="Project to run",
              help="Project to run")
@click.option('--host',
              default=f'localhost',
              help="Server hostname (default is localhost)")
@click.option('--port',
              default=f'5656',
              help="Port (default 5656, or leave empty)")
@click.option('--swagger_host',
              default=f'localhost',
              help="Swagger hostname (default is localhost)")
@click.pass_context
def run_api(ctx, project_name: str, host: str="localhost", port: str="5656", swagger_host: str="localhost"):
    """
        Runs existing project.


\b
        Example

\b
            ApiLogicServer run --project_name=/localhost/ApiLogicProject
            ApiLogicServer run --project_name=    # runs last-created project
    """
    global command
    command = "run-api"
    proj_dir = project_name
    if proj_dir == "":
        proj_dir = last_created_project_name
    else:
        proj_dir = os.path.abspath(f'{create_utils.resolve_home(project_name)}')
    run_file = f'{proj_dir}/api_logic_server_run.py '  # alert: sending args makes it hang: {host} {port} {swagger_host}
    create_utils.run_command(f'python {run_file}', msg="Run Created ApiLogicServer Project", new_line=True)
    print("run complete")


@main.command("create-ui")
@click.option('--use_model',
              default="models.py",
              help="See ApiLogicServer/wiki/Troubleshooting")
@click.option('--favorites',
              default="name description",
              help="Columns named like this displayed first")
@click.option('--non_favorites',
              default="id",
              help="Columns named like this displayed last")
@click.pass_context
def create_ui(ctx, use_model: str,
              favorites: str, non_favorites: str,
              ):
    """
        Creates models.yaml from models.py (internal).


\b
        Example

\b
            ApiLogicServer create-ui --use_model=~/dev/ApiLogicServer/tests/models-nw-plus.py
    """
    global command
    command = "create-ui"
    admin_out = resolve_home(use_model.replace("py","yaml"))
    project_directory, ignore = os.path.split(resolve_home(use_model))
    print(f'1. Loading existing model: {use_model}')
    model_creation_services = ModelCreationServices(  # fills in rsource_list for ui_admin_creator
        use_model=use_model,
        favorite_names=favorites, non_favorite_names=non_favorites,
        project_directory=project_directory,
        command=command,
        version=PR.__version__)

    print(f'2. Creating yaml from model')
    creator_path = abspath(f'{abspath(get_api_logic_server_dir())}/create_from_model')
    spec = importlib.util.spec_from_file_location("module.name", f'{creator_path}/ui_admin_creator.py')
    creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(creator)
    admin_yaml_dump = creator.create(model_creation_services)

    print(f'3. Writing yaml: {admin_out}')
    with open(admin_out, 'w') as yaml_file:
        yaml_file.write(admin_yaml_dump)


@main.command("examples")
@click.pass_context
def examples(ctx):
    """
    Example commands, including SQLAlchemy URIs.
    """
    uri_info.print_uri_info()


log = logging.getLogger(__name__)


def print_args(args, msg):
    print(msg)
    for each_arg in args:
        print(f'  {each_arg}')
    print(" ")


def check_ports():
    try:
        rtn_hostname = socket.gethostname()
        rtn_local_ip = socket.gethostbyname(rtn_hostname)
    except:
        rtn_local_ip = f"cannot get local ip from {rtn_hostname}"
        print(f"{rtn_local_ip}")
    port_check = False
    if port_check or is_docker():
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 5656  # Reserve a port for your service.
        port_is_available = True
        try:
            s.bind((host, port))  # Bind to the port
        except:
            port_is_available = False
        if not port_is_available:
            msg = "\nWarning - port 5656 does not appear to be available\n" \
                  "  Version 3.30 has changed port assignments to avoid port conflicts\n" \
                  "  For example, docker start:\n" \
                  "    docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server \n" \
                  "Ports are sometimes freed slowly, you may need to re-issue this command.\n\n"
            log.warning(msg)
            # sys.exit(msg)
        s.close()
    return rtn_hostname, rtn_local_ip


def start():               # target of setup.py
    sys.stdout.write("\nWelcome to API Logic Server " + PR.__version__ + "\n\n")
    hostname, local_ip = check_ports()  #  = socket.gethostname()
    # sys.stdout.write("    SQLAlchemy Database URI help: https://docs.sqlalchemy.org/en/14/core/engines.html\n")
    main(obj={})


command = "not set"
if __name__ == '__main__':  # debugger & python command line start here
    # eg: python api_logic_server_cli/cli.py create --project_name=~/Desktop/test_project
    # unix: python api_logic_server_cli/cli.py create --project_name=/home/ApiLogicProject

    print(f'\nWelcome to API Logic Server, {PR.__version__}\n')  #  at {local_ip} ')
    hostname, local_ip = check_ports()
    commands = sys.argv
    if len(sys.argv) > 1 and sys.argv[1] not in ["version", "sys-info", "welcome"] and \
            "show-args" in api_logic_server_info_file_dict:
        print_args(commands, f'\nCommand Line Arguments:')
    main()

