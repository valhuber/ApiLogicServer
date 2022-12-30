import os
from shutil import copyfile

from api_logic_server_cli.cli_args_project import Project
import create_from_model.api_logic_server_utils as create_utils


def get_windows_path_with_slashes(url: str) -> str:
    """ idiotic fix for windows (\ --> \\\\)
    https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
    """
    return url.replace('\\', '\\\\')


def update_config_and_copy_sqlite_db(project: Project, msg: str) -> str:
    """
    Parameters:

    :arg: msg print this, e.g., ".. ..Adding Database [{self.bind_key}] to existing project"
    :arg: project project setting object
    """
    print(msg)
    bind_key_upper = project.bind_key.upper()  # configs insist on all caps
    project_directory_actual = os.path.abspath(project.project_directory)  # make path absolute, not relative (no /../)
    return_abs_db_url = project.abs_db_url

    if "sqlite" in project.abs_db_url:
        """ sqlite - copy the db (relative fails, since cli-dir != project-dir)
        """
        # strip sqlite://// from sqlite:////Users/val/dev/ApiLogicServer/api_logic_server_cli/nw.sqlite
        db_loc = project.abs_db_url.replace("sqlite:///", "")
        target_db_loc_actual = project_directory_actual + f'/database/{project.bind_key}_db.sqlite'
        copyfile(db_loc, target_db_loc_actual)
        # backup_db = project_directory_actual + '/database/db-backup.sqlite'
        # copyfile(db_loc, backup_db)

        if os.name == "nt":  # windows
            # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
            target_db_loc_actual = get_windows_path_with_slashes(project_directory_actual + '\database\db.sqlite')
        # db_uri = f'sqlite:///{target_db_loc_actual}'
        return_abs_db_url = f'sqlite:///{target_db_loc_actual}'

        print(f'.. .. ..Sqlite database setup {target_db_loc_actual}...')
        print(f'.. .. .. ..From {db_loc}')

    # insert me to config
    db_uri = return_abs_db_url
    if os.name == "nt":  # windows
        # 'C:\\\\Users\\\\val\\\\dev\\\\servers\\\\api_logic_server\\\\database\\\\db.sqlite'
        target_db_loc_actual = get_windows_path_with_slashes(project_directory_actual + '\database\db.sqlite')
    CONFIG_URI = f'SQLALCHEMY_DATABASE_URI_{bind_key_upper}'

    config_insert = f"""
    {CONFIG_URI} = '{db_uri}'
    app_logger.debug(f'config.py - {CONFIG_URI}: {db_uri}')

    # as desired, use env variable: export SQLALCHEMY_DATABASE_URI='sqlite:////Users/val/dev/servers/docker_api_logic_project/database/db.sqliteXX'
    if os.getenv('{CONFIG_URI}'):
        {CONFIG_URI} = os.getenv('{CONFIG_URI}')
        app_logger.debug(f'.. overridden from env variable: {CONFIG_URI}')

"""
    # with open(f'{project.project_directory}/config.py', 'r') as file:
    #    config_data = file.read()
    create_utils.insert_lines_at(lines=config_insert,
                                at="# End Multi-Database URLs (from ApiLogicServer add-db...)",
                                file_name=f'{project.project_directory}/config.py')
    print(f'.. .. ..Config file updated for {CONFIG_URI}...')

    bind_insert = """
    from api import expose_api_models_<project.bind_key>
    from database import <project.bind_key>_models

    flask_app.config.update(SQLALCHEMY_BINDS = \\
        {'<project.bind_key>': flask_app.config['SQLALCHEMY_DATABASE_URI_<bind_key_upper>']})
    
    app_logger.info(f"\\n<project.bind_key> Config complete - database/<project.bind_key>_models.py"
        + f'\\n -- with bind: <project.bind_key>'
        + f'\\n -- len(database.<project.bind_key>_models.<project.bind_key>.metadata.tables) tables loaded')
    
    expose_api_models_<project.bind_key>.expose_models(safrs_api)

"""
    bind_insert = bind_insert.replace('<project.bind_key>', f'{project.bind_key}')
    bind_insert = bind_insert.replace('<bind_key_upper>', f'{bind_key_upper}')
    create_utils.insert_lines_at(lines=bind_insert,
                                at="# End Bind Databases",
                                file_name=f'{project.project_directory}/database/bind_databases.py')
    print(f'.. .. ..bind_databases updated for {CONFIG_URI}...')

    return return_abs_db_url