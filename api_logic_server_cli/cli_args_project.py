from api_logic_server_cli.cli_args import ProjectArgs
from os.path import abspath
from pathlib import Path
import os

class Project(ProjectArgs):
    
    def __init__(self):
        
        super(Project, self).__init__()

        self.os_cwd = os.getcwd()
        self.abs_db_url = None
        self.nw_db_status = None
        self.project_directory = None
        self.copy_to_project_directory = None

        running_at = Path(__file__)
        self.api_logic_server_dir_path = running_at.parent.absolute()  # ne abspath(f'{abspath(get_api_logic_server_dir())}'))


        """
        def __init__(self, project_name: str, db_url: str, api_name: str,
                     host: str, port: str, swagger_host: str, not_exposed: str,
                     from_git: str, db_types: str, open_with: str, run: bool, use_model: str, admin_app: bool,
                     flask_appbuilder: bool, favorites: str, non_favorites: str, react_admin: bool,
                     extended_builder: str, multi_api: bool, infer_primary_key: bool):
        self.project_name = project_name
        self.db_url = db_url
        self.api_name = api_name
        self.host = host
        self.port = port
        self.swagger_host = swagger_host
        self.not_exposed = not_exposed
        self.from_git = from_git
        self.db_types = db_types
        self.open_with = open_with
        self.run = run
        self.use_model = use_model
        self.admin_app = admin_app
        self.flask_appbuilder = flask_appbuilder
        self.favorites = favorites
        self.non_favorites = non_favorites
        self.react_admin = react_admin
        self.extended_builder = extended_builder
        self.multi_api = multi_api
        self.infer_primary_key = infer_primary_key

        self.os_cwd = os.getcwd()
        self.abs_db_url = ""
        self. nw_db_status = ""

        running_at = Path(__file__)
        self.api_logic_server_dir_path = running_at.parent.absolute()  # ne abspath(f'{abspath(get_api_logic_server_dir())}'))
        """


    def print_options(self):
        """ Creating ApiLogicServer with options: (or uri helo) """
        if self.db_url == "?":
            print_uri_info()
            exit(0)

        print_options = True
        if print_options:
            print(f'\n\nCreating ApiLogicServer with options:')
            print(f'  --db_url={self.db_url}')
            print(f'  --project_name={self.project_name}   (pwd: {self.os_cwd})')
            print(f'  --api_name={self.api_name}')
            print(f'  --admin_app={self.admin_app}')
            print(f'  --react_admin={self.react_admin}')
            print(f'  --flask_appbuilder={self.flask_appbuilder}')
            print(f'  --from_git={self.from_git}')
            #        print(f'  --db_types={self.db_types}')
            print(f'  --run={self.run}')
            print(f'  --host={self.host}')
            print(f'  --port={self.port}')
            print(f'  --swagger_host={self.swagger_host}')
            print(f'  --not_exposed={self.not_exposed}')
            print(f'  --open_with={self.open_with}')
            print(f'  --use_model={self.use_model}')
            print(f'  --favorites={self.favorites}')
            print(f'  --non_favorites={self.non_favorites}')
            print(f'  --extended_builder={self.extended_builder}')
            print(f'  --multi_api={self.multi_api}')
            print(f'  --infer_primary_key={self.infer_primary_key}')
