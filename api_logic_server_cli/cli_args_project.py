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
        """ '', nw, nw+, nw- """

        self.project_directory = None
        """ string - may have relative /../ """

        self.project_directory_actual = None
        """ string - no relative /../ """

        self.project_directory_path = None
        """ Path (project_directory_actual) """

        self.copy_to_project_directory = None
        self.merge_into_prototype = None
        """ used by codespaces - project_name = ./ """

        self.model_gen_bind_msg = False
        """ sqlacodegen/codegen msg printed """

        self.model_file_name = "models.py"
        """ name of models file being processed """

        running_at = Path(__file__)
        self.api_logic_server_dir_path = running_at.parent.absolute()  # ne abspath(f'{abspath(get_api_logic_server_dir())}'))



    def print_options(self):
        """ Creating ApiLogicServer with options: (or uri helo) """
        if self.db_url == "?":
            print_uri_info()
            exit(0)

        print_options = True
        if print_options:
            print(f'\n\nCreating ApiLogicServer with options:')
            print(f'  --db_url={self.db_url}')
            print(f'  --bind_key={self.bind_key}') 
            print(f'  --bind_url_separator={self.bind_url_separator}')
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
