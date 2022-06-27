#!/usr/bin/env python
"""
copy nw customizations over created nw- project
"""

import os, sys
import subprocess
from pathlib import Path
import shutil


docker_api_logic_server = '/home/api_logic_server'
verbose = False

def is_docker() -> bool:
    """ running docker?  dir exists: /home/api_logic_server """
    path = docker_api_logic_server 
    return os.path.isdir(path)


def print_at(label: str, value: str):
    tab_to = 28 - len(label)
    spaces = ' ' * tab_to
    print(f'{label}: {spaces}{value}')


def get_api_logic_project_path() -> Path:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    running_at = Path(__file__)
    python_path = running_at.parent.absolute()
    # parent_path = python_path.parent.absolute()
    return python_path


def recursive_overwrite(src, dest, ignore=None):
    """
    copyTree, with overwrite
    thanks: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
    """
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        is_not_noise = "test/" not in str(dest)
        if is_not_noise and verbose:
            print(f'..{str(dest)}')
        shutil.copyfile(src, dest)


def backup_file(proj_dir: Path, folder: str, file: str):
    src = proj_dir.joinpath(folder).joinpath(file + ".py")
    dest = proj_dir.joinpath(folder).joinpath(file + "_original.py")
    if Path.exists(dest):
        print(f'..skipping file already copied: {folder}/{file}.py')
    else:
        print(f'..{folder}/{file}.py')
        shutil.copyfile(src=src, dst=dest)


def perform_customizations():
    print(" ")
    print("\nPerform Customizations here, 1.03\n")
    global verbose

    dir = get_api_logic_project_path()
    do_test_env = False
    if do_test_env:
        test_env = "/workspaces/../home/api_logic_server/"
        if os.path.exists(test_env):
            dir = test_env
    sys.path.append(dir)  # e.g, on Docker -- export PATH=" /home/app_user/api_logic_server_cli"

    if is_docker():
        sys.path.append(docker_api_logic_server)

    try:
        import api_logic_server_cli.cli as cli
        import api_logic_server_cli.create_from_model.api_logic_server_utils as create_utils
    except Exception as e:
        cli = None
        pass
    if cli is None:
        print(f'*** ApiLogicServer not found - is venv set? ***\n')
        exit(1)
    print_at('ApiLogicServer version', cli.__version__)
    print_at("API Logic Project", dir)
    print_at("API Logic Server CLI", cli.__file__)
    cli_path = Path(cli.__file__).parent

    if sys.argv[1:]:
        print(" ")
        if sys.argv[1].startswith('v'):
            verbose = True
    else:
        print("\nUse argument 'go' to apply customizations\n\n")
        exit(0)

    print("\nCreating '_original' backups (for purposes of comparison) for the following key customization files:")
    backup_file(proj_dir=dir, folder="api", file="customize_api")
    backup_file(proj_dir=dir, folder="database", file="customize_models")
    backup_file(proj_dir=dir, folder="logic", file="declare_logic")

    if verbose:
        print("\nCopying NW customization files (test files omitted from this list)...") 
    else:
        print("\nCopying...")
    nw_dir = cli_path.joinpath('project_prototype_nw')
    recursive_overwrite(nw_dir, dir)

    home_js_file = dir.joinpath('ui').joinpath('admin').joinpath('home.js')
    create_utils.replace_string_in_file(search_for="api_logic_server_api_name",
                        replace_with=f'api',
                        in_file=home_js_file)

    print("\n*** Customizations applied - explore the files above")
    print("\n*** See Tutorial: https://github.com/valhuber/ApiLogicServer/blob/main/README.md#sample-tutorial---api-logic-server\n\n")


if __name__ == '__main__':
    perform_customizations()
