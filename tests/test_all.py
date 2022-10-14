from doctest import debug_script
from re import A
import subprocess, os, time, requests
from shutil import copyfile
import shutil
from sys import platform
from subprocess import DEVNULL, STDOUT, check_call
from pathlib import Path
# import api_logic_server_cli.create_from_model.api_logic_server_utils as create_utils


def find_valid_python_name() -> str:
    '''
        sigh.  On *some* macs, python fails so we must use python3.
        
        return 'python3' in this case (alert - python works if in venv!)
    '''
    find_by = "os"  # "exec", "os"
    if find_by == "exec":
        python3_worked = False
        try:
            result_b = subprocess.check_output('python --version', shell=True, stderr=subprocess.STDOUT)
        except Exception as e:
            python3_worked = False
            try:
                result_b = subprocess.check_output('python3 --version', shell=True, stderr=subprocess.STDOUT)
            except Exception as e1:
                python3_worked = False
            python3_worked = True
        if python3_worked:
            return "python3"
        else:
            return "python"
    elif find_by == "os":
        if platform == "darwin":
            return 'python3'
        else:
            return 'python'

def get_api_logic_server_path() -> Path:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    file_path = Path(os.path.abspath(__file__))
    api_logic_server_path = file_path.parent.parent
    api_logic_server_path_str = str(api_logic_server_path)
    return api_logic_server_path

def get_servers_install_path() -> Path:
    """ Path: /Users/val/dev/servers/install """
    api_logic_server_path = os.path.abspath(get_api_logic_server_path())
    dev_path = Path(api_logic_server_path).parent
    rtn_path = dev_path.joinpath("servers").joinpath("install")
    return rtn_path

def delete_dir(dir_path, msg):
    """
    :param dir_path: delete this folder
    :return:
    """
    # credit: https://linuxize.com/post/python-delete-files-and-directories/
    # and https://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
    import errno, os, stat, shutil

    def handleRemoveReadonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise
    if msg != "":
        print(f'{msg} Delete dir: {dir_path}')
    use_callback = False
    if use_callback:
        shutil.rmtree(dir_path, ignore_errors=False, onerror=handleRemoveReadonly)
    else:
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            if "No such file" in e.strerror:
                pass
            else:
                print("Error: %s : %s" % (dir_path, e.strerror))

def recursive_overwrite(src: Path, dest: Path, ignore=None):
    """
    copyTree, with overwrite
    thanks: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all

    :param src: from path
    :param dest: destinatiom path
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
        shutil.copyfile(src, dest)

def stop_server(msg: str):
    pass
    URL = "http://localhost:5656/kill"
    PARAMS = {'msg': msg}
    try:
        r = requests.get(url = URL, params = PARAMS)
    except:
        print("..")

    # print("\nServer Stopped")

def run_command(cmd: str, msg: str = "", new_line: bool=False, cwd: Path=None) -> str:
    """ run shell command (waits)

    :param cmd: string of command to execute
    :param msg: optional message (no-msg to suppress)
    :param cwd: path to current working directory
    :return: dict print(ret.stdout.decode())
    """

    print(f'{msg}, with command: \n{cmd}')
    result_b = None
    try:
        # result_b = subprocess.run(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT)
        result_b = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True)
        result = str(result_b)  # b'pyenv 1.2.21\n' 
        result = result[2: len(result) - 3]
        spaces = ' ' * (20 - len(cmd))
        # print(f'{msg} {cmd}')  #  result: {spaces}{result}')]
    except:
        print(f'\n\n*** Failed on {cmd}')
        raise
    return result_b  # print(ret.stdout.decode())


# ***************************
# MAIN CODE
# ***************************

python = find_valid_python_name()  # geesh - allow for python vs python3
set_venv = '. venv/bin/activate'
'''typical source "venv/bin/activate" does not persist over cmds, see...
   https://github.com/valhuber/ubuntu-script-venv/blob/main/use-in-script.sh '''
if platform == "win32":
    set_venv = "venv\\Scripts\\activate"

default_setting = True  # simplify enable / disable most
do_install_api_logic_server = default_setting
do_create_api_logic_project = default_setting
do_run_api_logic_project = default_setting
do_test_api_logic_project = default_setting
do_other_sqlite_databases = default_setting
do_docker_databases = default_setting
do_allocation_test = default_setting

install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
api_logic_project_path = install_api_logic_server_path.joinpath('ApiLogicProject')
api_logic_server_tests_path = Path(os.path.abspath(__file__)).parent

print("\n\ntest_all 1.0 running")
print(f'  Builds / Installs API Logic Server to api_logic_project_path: {api_logic_project_path}')
print(f'  Creates Sample project (nw), starts server and runs Behave Tests')
print(f'  Creates other projects')

stop_server(msg="BEGIN TESTS\n")

debug_venv = True
if debug_script:
    api_logic_server_install_path = os.path.abspath(install_api_logic_server_path.parent)
    result_venv = run_command(f'pwd && {set_venv} && pip freeze',
        cwd=api_logic_server_install_path,
        msg=f'\nInstall ApiLogicServer at: {str(api_logic_server_install_path)}')
    print(result_venv.stdout.decode())  # should say pyodbc==4.0.34

if do_install_api_logic_server:
    if os.path.exists(install_api_logic_server_path):
        delete_dir(dir_path=str(install_api_logic_server_path), msg="delete install ")
    try:
        os.mkdir(install_api_logic_server_path, mode = 0o777)
    except:
        print("Windows dir exists?")

    api_logic_server_home_path = api_logic_server_tests_path.parent
    result_build = run_command(f'{python} setup.py sdist bdist_wheel',
        cwd=api_logic_server_home_path,
        msg=f'\nBuild ApiLogicServer at: {str(api_logic_server_home_path)}')

    result_install = run_command(f'{python} -m venv venv && {set_venv} && {python} -m pip install {str(api_logic_server_home_path)}',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall ApiLogicServer at: {str(install_api_logic_server_path)}')

    result_pyodbc = run_command(
        f'{set_venv} && {python} -m pip install pyodbc',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall pyodbc')


if do_create_api_logic_project:
    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')

if do_run_api_logic_project:
    print(f'\n\nStarting Server...\n')
    try:
        server = subprocess.Popen([f'{python}','api_logic_server_run.py'],
                                cwd=api_logic_project_path)
    except:
        print("Popen failed")
        raise
    print(f'\nServer running - server: {str(server)}\n')

if do_test_api_logic_project:
    try:
        print("\nWaiting for server to start...")
        time.sleep(10) 
        print("\nProceeding with Behave tests...\n")
        api_logic_project_behave_path = api_logic_project_path.joinpath('test').joinpath('api_logic_server_behave')
        api_logic_project_logs_path = api_logic_project_behave_path.joinpath('logs').joinpath('behave.log')
        result_behave = run_command(f'{python} behave_run.py --outfile={str(api_logic_project_logs_path)}',
            cwd=api_logic_project_behave_path,
            msg="\nBehave Test Run")
    except:
        print(f'\n\n** Behave Test failed\nHere is log from: {str(api_logic_project_logs_path)}\n\n')
        f = open(str(api_logic_project_logs_path), 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()
    print("\nBehave tests - Success... (note - server still running)\n")

if do_other_sqlite_databases:
    string = '''big long 
    string'''
    run_command('{set_venv} && ApiLogicServer create --project_name=chinook_sqlite --db_url={install}/Chinook_Sqlite.sqlite',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate chinook_sqlite at: {str(install_api_logic_server_path)}')

if do_docker_databases:
    run_command(
        "{set_venv} && ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate MySQL classicmodels at: {str(install_api_logic_server_path)}')
    
    run_command(
        "{set_venv} && ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Postgres postgres (nw) at: {str(install_api_logic_server_path)}')

    run_command(
        "{set_venv} && ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate SqlServer NORTHWND at: {str(install_api_logic_server_path)}')

stop_server(msg="END NW TESTS\n")

if do_allocation_test:
    allocation_path = api_logic_server_tests_path.joinpath('allocation_test').joinpath('allocation.sqlite')
    allocation_url = f'sqlite:///{allocation_path}'
    run_command(f'{set_venv} && ApiLogicServer create --project_name=Allocation --db_url={allocation_url}',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Allocation at: {str(install_api_logic_server_path)}')
    pass

    src = api_logic_server_tests_path.joinpath('allocation_test').joinpath('Allocation-src')
    allocation_project_path = install_api_logic_server_path.joinpath('Allocation')
    recursive_overwrite(src = src,
                        dest = str(allocation_project_path))
    print(f'\n\nStarting Server...\n')
    try:
        server = subprocess.Popen([f'{python}','api_logic_server_run.py'],
                                cwd=allocation_project_path)
    except:
        print("Popen failed")
        raise
    print(f'\nServer [Allocation] running - server: {str(server)}\n')

    try:
        print("\nWaiting for server to start...")
        time.sleep(10) 
        print("\nProceeding with Allocation tests...\n")
        allocation_tests_path = allocation_project_path.joinpath('test')
        run_command(f'sh test.sh',
            cwd=allocation_tests_path,
            msg="\nBehave Test Run")
    except:
        print(f'\n\n** Allocation Test failed\n\n')
    print("\nAllocation tests - Success... (note - server still running)\n")

stop_server(msg="END ALLOCATION TEST\n")