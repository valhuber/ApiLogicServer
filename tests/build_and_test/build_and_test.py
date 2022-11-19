import subprocess, os, time, requests, sys, re, io
from shutil import copyfile
import shutil
from sys import platform
from subprocess import DEVNULL, STDOUT, check_call
from pathlib import Path

class DotDict(dict):
    """ APiLogicServer dot.notation access to dictionary attributes """
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

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
    api_logic_server_path = file_path.parent.parent.parent
    return api_logic_server_path

def get_servers_install_path() -> Path:
    """ Path: /Users/val/dev/servers/install """
    api_logic_server_path = get_api_logic_server_path()
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
    URL = "http://localhost:5656/stop"
    PARAMS = {'msg': msg}
    try:
        r = requests.get(url = URL, params = PARAMS)
    except:
        print("..")

def print_run_output(msg, input):
    print(f'\n{msg}')
    print_lines = input.split("\\n")
    for each_line in print_lines:
        print(each_line)

def check_command(command_result):
    result_stdout = ""
    result_stderr = ''
    if command_result is not None:
        if command_result.stdout is not None:
            result_stdout = str(command_result.stdout)
        if command_result.stderr is not None:
            result_stderr = str(command_result.stderr)

    if "Trace" in result_stderr or \
        "Error" in result_stderr or \
        "error" in result_stderr or \
        "Traceback" in result_stderr:
        print("\n\n==> Command Failed - Console Log:")
        for line in command_result.stdout.decode('utf-8').split('\n'):
            print (line)
        print("\n\n==> Error Log:")
        for line in command_result.stderr.decode('utf-8').split('\n'):
            print (line)
        raise ValueError("Traceback detected")

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
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True)
        check_command(result)
        """
        if "Traceback" in result_stderr:
            print_run_output("Traceback detected - stdout", result_stdout)
            print_run_output("stderr", result_stderr)
            raise ValueError("Traceback detected")
        """
    except:
        print(f'\n\n*** Failed on {cmd}')
        raise
    return result_b

def start_api_logic_server(project_name: str):
    """ start server at path, and wait a few moments """
    import stat

    install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
    path = install_api_logic_server_path.joinpath(project_name)
    print(f'\n\nStarting Server {project_name}... from  ${install_api_logic_server_path}\venv\n')
    pipe = None
    if platform == "win32":
        start_cmd = ['powershell.exe', f'{str(path)}\\run.ps1 x']
    else:
        os.chmod(f'{str(path)}/run.sh', 0o777)
        # start_cmd = ['sh', f'{str(path)}/run x']
        start_cmd = [f'{str(path)}/run.sh', 'calling']
        # start_cmd = [f'{str(path)}/run.sh']
        print(f'sh {str(path)}/run.sh x')

    try:
        pipe = subprocess.Popen(start_cmd, cwd=install_api_logic_server_path)  #, stderr=subprocess.PIPE)
    except:
        print(f"\nsubprocess.Popen failed trying to start server.. with command: \n {start_cmd}")
        # what = pipe.stderr.readline()
        raise
    print(f'\n.. Server started - server: {project_name}\n')
    print("\n.. Waiting for server to start...")
    time.sleep(10) 

    URL = "http://localhost:5656/hello_world?user=ApiLogicServer"
    try:
        r = requests.get(url = URL)
        print("\n.. Proceeding...\n")
    except:
        print(f".. Ping failed on {project_name}")
        raise

def does_file_contain(in_file: str, search_for: str) -> bool:
    with open(in_file, 'r') as file:
        file_data = file.read()
        result = file_data.find(search_for)
    return result > 0

def replace_string_in_file(search_for: str, replace_with: str, in_file: str):
    with open(in_file, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace(search_for, replace_with)
    with open(in_file, 'w') as file:
        file.write(file_data)

def rebuild_tests():
    print(f'Rebuild tests')
    current_path = Path(os.path.abspath(__file__))
    install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
    api_logic_project_path = install_api_logic_server_path.joinpath('ApiLogicProject')
    admin_merge_yaml_path = api_logic_project_path.joinpath('ui').joinpath('admin').joinpath('admin-merge.yaml')
    new_model_path = current_path.parent.parent.joinpath('rebuild_tests').joinpath('models.py')
    models_py_path = api_logic_project_path.joinpath('database').joinpath('models.py')

    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    if admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml exists on create')

    result_create = run_command(f'{set_venv} && ApiLogicServer rebuild-from-database --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    if not admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml does not exist on rebuild-from-database')
    if does_file_contain(in_file=admin_merge_yaml_path, search_for="new_resources:"):
        pass
    else:
        raise ValueError('System Error - admin-merge.yaml does not contain "new_resources: " ')

    copyfile(new_model_path, models_py_path)
    result_create = run_command(f'{set_venv} && ApiLogicServer rebuild-from-model --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    if not admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml does not exist on rebuild-from-model')
    if does_file_contain(in_file=models_py_path, search_for="CategoryNew"):
        pass
    else:
        raise ValueError('System Error - admin-merge.yaml does not contain "new_resources: " ')

    print(f'..rebuild tests compete')

# ***************************
#        MAIN CODE
# ***************************

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
program_dir = str(current_path)
os.chdir(program_dir)  # so admin app can find images, code

python = find_valid_python_name()  # geesh - allow for python vs python3

if platform == "darwin":
    from env_mac import Config
elif platform == "win32":
    from env_win import Config
elif platform.startswith("linux"):
    from env_linux import Config
else:
    print("unknown platform")

set_venv = Config.set_venv
db_ip = Config.docker_database_ip

install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
api_logic_project_path = install_api_logic_server_path.joinpath('ApiLogicProject')
api_logic_server_tests_path = Path(os.path.abspath(__file__)).parent.parent

api_logic_server_cli_path = get_api_logic_server_path().\
                            joinpath("api_logic_server_cli").joinpath('cli.py')
with io.open(str(api_logic_server_cli_path), "rt", encoding="utf8") as f:
    api_logic_server_version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

print(f"\n\n{__file__} 1.0 running")
print(f'  Builds / Installs API Logic Server to install_api_logic_server_path: {install_api_logic_server_path}')
print(f'  Creates Sample project (nw), starts server and runs Behave Tests')
print(f'  Rebuild tests')
print(f'  Creates other projects')

# stop_server(msg="BEGIN TESTS\n")  # just in case server left running

debug_script = False
if debug_script:
    api_logic_server_install_path = os.path.abspath(install_api_logic_server_path.parent)
    result_venv = run_command(f'pwd && {set_venv} && pip freeze',
        cwd=api_logic_server_install_path,
        msg=f'\nInstall ApiLogicServer at: {str(api_logic_server_install_path)}')
    print(result_venv.stdout.decode())  # should say pyodbc==4.0.34

if Config.do_install_api_logic_server:
    if os.path.exists(install_api_logic_server_path):
        # rm -r ApiLogicServer.egg-info; rm -r build; rm -r dist
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('ApiLogicServer.egg-info')), msg="delete egg ")
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('build')), msg="delete build ")
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('dist')), msg="delete dist ")
        delete_dir(dir_path=str(install_api_logic_server_path), msg="delete install ")
    try:
        os.mkdir(install_api_logic_server_path, mode = 0o777)
        os.mkdir(install_api_logic_server_path.joinpath('dockers'), mode = 0o777)
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
        f'{set_venv} && {python} -m pip install pyodbc==4.0.34',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall pyodbc')

if Config.do_create_api_logic_project:
    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')

if Config.do_run_api_logic_project:
    start_api_logic_server(project_name="ApiLogicProject")

if Config.do_test_api_logic_project:
    try:
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
    print("\nBehave tests - Success...\n")
    stop_server(msg="*** NW TESTS COMPLETE ***\n")

if Config.do_rebuild_tests:
    rebuild_tests()

if Config.do_other_sqlite_databases:
    run_command('{set_venv} && ApiLogicServer create --project_name=chinook_sqlite --db_url={install}/Chinook_Sqlite.sqlite',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate chinook_sqlite at: {str(install_api_logic_server_path)}')

if Config.do_allocation_test:
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

    start_api_logic_server(project_name="Allocation")

    try:
        print("\nProceeding with Allocation tests...\n")
        allocation_tests_path = allocation_project_path.joinpath('test')
        run_command(f'sh test.sh',
            cwd=allocation_tests_path,
            msg="\nBehave Test Run")
    except:
        print(f'\n\n** Allocation Test failed\n\n')
    print("\nAllocation tests - Success...\n")
    stop_server(msg="*** ALLOCATION TEST COMPLETE ***\n")

if Config.do_docker_mysql:
    result_docker_mysql_classic = run_command(
        f"{set_venv} && ApiLogicServer create --project_name=classicmodels --db_url=mysql+pymysql://root:p@{db_ip}:3306/classicmodels",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate MySQL classicmodels at: {str(install_api_logic_server_path)}')
    check_command(result_docker_mysql_classic)
    start_api_logic_server(project_name='classicmodels')
    stop_server(msg="classicmodels\n")
    
if Config.do_docker_sqlserver:
    result_docker_sqlserver = run_command(
        f"{set_venv} && ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:Posey3861@{db_ip}:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate SqlServer NORTHWND at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='sqlserver')
    stop_server(msg="sqlserver\n")
    
if Config.do_docker_postgres:
    result_docker_postgres = run_command(
        f"{set_venv} && ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@{db_ip}/postgres",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Postgres postgres (nw) at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='postgres')
    print(f'\nServer [Postgres] running\n')

print("\n\nSUCCESS -- END OF TESTS (be sure to test Postgres, and stop the server")

print(f"\n\nRelease {api_logic_server_version}?\n")
print(f'cd {str(get_api_logic_server_path())}')
print(f"python3 -m twine upload  --username vhuber --password PypiPassword --skip-existing dist/*  \n\n")
