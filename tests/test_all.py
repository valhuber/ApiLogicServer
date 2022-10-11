import subprocess, os, time
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


def run_command(cmd: str, msg: str = "", new_line: bool=False, cwd: Path=None) -> str:
    """ run shell command (waits)

    :param cmd: string of command to execute
    :param msg: optional message (no-msg to suppress)
    :param cwd: path to current working directory
    :return:
    """

    print(f'{msg}, with command: \n{cmd}')
    result_b = None
    try:
        result_b = subprocess.check_output(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT)
        result = str(result_b)  # b'pyenv 1.2.21\n' 
        result = result[2: len(result) - 3]
        spaces = ' ' * (20 - len(cmd))
        # print(f'{msg} {cmd}')  #  result: {spaces}{result}')]
    except:
        print(f'\n\n*** Failed on {cmd}')
        raise
    return result


# ***************************
# MAIN CODE
# ***************************

python = find_valid_python_name()  # geesh - allow for python vs python3

do_install_api_logic_server = True
do_create_api_logic_project = True
do_run_api_logic_project = True
do_test_api_logic_project = True
do_other_sqlite_databases = True
do_docker_databases = True

install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
api_logic_project_path = install_api_logic_server_path.joinpath('ApiLogicProject')

print("test_all 1.0 running")
print(f'  Builds / Installs API Logic Server to api_logic_project_path: {api_logic_project_path}')
print(f'  Creates Sample project (nw), starts server and runs Behave Tests')
print(f'  Creates other projects')

if do_install_api_logic_server:
    if os.path.exists(install_api_logic_server_path):
        delete_dir(dir_path=str(install_api_logic_server_path), msg="delete install ")
    os.mkdir(install_api_logic_server_path)

    run_command(f'{python} -m venv venv; source venv/bin/activate; python3 -m pip install /Users/val/dev/ApiLogicServer',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall ApiLogicServer at: {str(install_api_logic_server_path)}')

    run_command(
        f'source venv/bin/activate; {python} -m pip install pyodbc',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall pyodbc')


if do_create_api_logic_project:
    run_command(f'source venv/bin/activate; ApiLogicServer create --project_name=ApiLogicProject --db_url=',
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
        run_command(f'{python} behave_run.py --outfile={str(api_logic_project_logs_path)}',
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
    run_command('source venv/bin/activate; ApiLogicServer create --project_name=chinook_sqlite --db_url={install}/Chinook_Sqlite.sqlite',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate chinook_sqlite at: {str(install_api_logic_server_path)}')

if do_docker_databases:
    run_command(
        "source venv/bin/activate; ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate MySQL classicmodels at: {str(install_api_logic_server_path)}')
    
    run_command(
        "source venv/bin/activate; ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Postgres postgres (nw) at: {str(install_api_logic_server_path)}')

    run_command(
        "source venv/bin/activate; ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate SqlServer NORTHWND at: {str(install_api_logic_server_path)}')
 
    """
      ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'

      ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres
    
      ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'
"""

print("\n\nEND TESTS\n")