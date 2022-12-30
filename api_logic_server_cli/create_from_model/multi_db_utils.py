import os
from shutil import copyfile

from api_logic_server_cli.cli_args_project import Project
import create_from_model.api_logic_server_utils as create_utils


def get_windows_path_with_slashes(url: str) -> str:
    """ idiotic fix for windows (\ --> \\\\)

    https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file"""
    return url.replace('\\', '\\\\')


def update_config_and_copy_sqlite_db(project: Project, msg: str) -> str:
    """
    Parameters:

    :arg: msg print this, e.g., .. ..Adding Database [{self.bind_key}] to existing project
    :arg: project project setting object
    """

    project_directory_actual = os.path.abspath(project.project_directory)  # make path absolute, not relative (no /../)
    return_abs_db_url = project.abs_db_url

    if "sqlite" in project.abs_db_url:
        """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
        """
        # strip sqlite://// from sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/nw.sqlite
        db_loc = project.abs_db_url.replace("sqlite:///", "")
        target_db_loc_actual = project_directory_actual + '/database/db.sqlite'
        copyfile(db_loc, target_db_loc_actual)
        backup_db = project_directory_actual + '/database/db-backup.sqlite'
        copyfile(db_loc, backup_db)

        if os.name == "nt":  # windows
            # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
            target_db_loc_actual = get_windows_path_with_slashes(project_directory_actual + '\database\db.sqlite')
        # db_uri = f'sqlite:///{target_db_loc_actual}'
        return_abs_db_url = f'sqlite:///{target_db_loc_actual}'
        create_utils.replace_string_in_file(search_for="replace_db_url",
                            replace_with=return_abs_db_url,
                            in_file=f'{project.project_directory}/config.py')
        create_utils.replace_string_in_file(search_for="replace_db_url",
                            replace_with=return_abs_db_url,
                            in_file=f'{project.project_directory}/database/alembic.ini')

        print(f'.. ..Sqlite database setup {target_db_loc_actual}...')
        print(f'.. .. ..From {db_loc}')
        print(f'.. .. ..db_uri set to: {return_abs_db_url} in <project>/config.py')
    # add me to config
    db_uri = get_windows_path_with_slashes(project.abs_db_url)
    create_utils.replace_string_in_file(search_for="replace_db_url",
                        replace_with=db_uri,
                        in_file=f'{project.project_directory}/config.py')

    return return_abs_db_url