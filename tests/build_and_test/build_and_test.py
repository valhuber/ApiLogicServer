import subprocess, os, time, requests, sys, re, io
from typing import List
from shutil import copyfile
import shutil
from sys import platform
from subprocess import DEVNULL, STDOUT, check_call
from pathlib import Path
from dotmap import DotMap
import json

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

def print_byte_string(msg, byte_string):
    print(msg)
    for line in byte_string.decode('utf-8').split('\n'):
        print (line)

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
        "allocation failed" in result_stdout or \
        "error" in result_stderr or \
        "Cannot connect" in result_stderr or \
        "Traceback" in result_stderr:
        if 'alembic.runtime.migration' in result_stderr:
            pass
        else:
            print_byte_string("\n\n==> Command Failed - Console Log:", command_result.stdout)
            print_byte_string("\n\n==> Error Log:", command_result.stderr)
            raise ValueError("Traceback detected")

def run_command(cmd: str, msg: str = "", new_line: bool=False, 
    cwd: Path=None, show_output: bool=False) -> object:
    """ run shell command (waits)

    :param cmd: string of command to execute
    :param msg: optional message (no-msg to suppress)
    :param cwd: path to current working directory
    :param show_output print command result
    :return: dict print(ret.stdout.decode())
    """

    print(f'{msg}, with command: \n{cmd}')
    try:
        # result_b = subprocess.run(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT)
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True)
        if show_output:
            print_byte_string(f'{msg} Output:', result.stdout)
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
    return result

def start_api_logic_server(project_name: str, env_list = None):
    """ start server at path [with env], and wait a few moments """
    import stat

    install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
    path = install_api_logic_server_path.joinpath(project_name)
    print(f'\n\nStarting Server {project_name}... from  {install_api_logic_server_path}\venv\n')
    pipe = None
    if platform == "win32":
        start_cmd = ['powershell.exe', f'{str(path)}\\run.ps1 x']
    else:
        os.chmod(f'{str(path)}/run.sh', 0o777)
        # start_cmd = ['sh', f'{str(path)}/run x']
        start_cmd = [f'{str(path)}/run.sh', 'calling']
        print(f'start_api_logic_server() - start_cmd[0]: {start_cmd[0]}')

    try:
        my_env = os.environ.copy()
        if env_list is not None:
            for each_env_name, env_value in env_list:
                my_env[each_env_name] = env_value
        my_env['PYTHONHASHSEED'] = '0'
        pipe = subprocess.Popen(start_cmd, cwd=install_api_logic_server_path, env=my_env)  #, stderr=subprocess.PIPE)
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

def login(user: str='aneu'):
    """

    Login as <specified user>, password p

    Raises:
        Exception: if login fails

    Returns:
        _type_: header = {'Authorization': 'Bearer {}'.format(f'{token}')}
    """
    post_uri = 'http://localhost:5656/api/auth/login'
    post_data = {"username": user, "password": "p"}
    r = requests.post(url=post_uri, json = post_data)
    response_text = r.text
    status_code = r.status_code
    if status_code > 300:
        raise Exception(f'POST login failed - status_code = {status_code}, with response text {r.text}')
    result_data = json.loads(response_text)
    result_map = DotMap(result_data)
    token = result_map.access_token
    header = {'Authorization': 'Bearer {}'.format(f'{token}')}
    return header

def multi_database_tests():
    """
    NW-, plus todo and security
    """

    print(f'Multi-Database Tests')

    current_path = Path(os.path.abspath(__file__))
    install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
    api_logic_project_path = install_api_logic_server_path.joinpath('MultiDB')

    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=MultiDB --db_url=nw-',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate MultiDB at: {str(install_api_logic_server_path)}')

    result_create = run_command(f'{set_venv} && ApiLogicServer add-db --db_url=todo --bind_key=todo --project_name=MultiDB',
        cwd=install_api_logic_server_path,
        msg=f'\nAdd ToDoDB at: {str(install_api_logic_server_path)}')

    # declare_security
    result_create = run_command(f'{set_venv} && ApiLogicServer add-auth --project_name=MultiDB',
        cwd=install_api_logic_server_path,
        msg=f'\nAdd AuthDB at: {str(install_api_logic_server_path)}')

    env = [("SECURITY_ENABLED", "true")]
    start_api_logic_server(project_name='MultiDB', env_list=env)  # , env='export SECURITY_ENABLED=true')
    # verify 1 Category row (validates multi-db <auth>, and security)
    get_uri = "http://localhost:5656/api/Category/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=id"
    r = requests.get(url=get_uri, headers=login())
    response_text = r.text
    result_data = json.loads(response_text) 
    assert len(result_data["data"]) == 1, "MultiDB: Did not find 1 expected result row"

    stop_server(msg="MultiDB\n")

def rebuild_tests():
    print(f'Rebuild tests')

    current_path = Path(os.path.abspath(__file__))
    install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
    api_logic_project_path = install_api_logic_server_path.joinpath('Rebuild')
    admin_merge_yaml_path = api_logic_project_path.joinpath('ui').joinpath('admin').joinpath('admin-merge.yaml')
    new_model_path = current_path.parent.parent.joinpath('rebuild_tests').joinpath('models.py')
    """ same as models, but adds class: CategoryNew """
    models_py_path = api_logic_project_path.joinpath('database').joinpath('models.py')

    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=Rebuild --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Rebuild at: {str(install_api_logic_server_path)}')
    if admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml exists on create')

    result_create = run_command(f'{set_venv} && ApiLogicServer rebuild-from-database --project_name=Rebuild --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    if not admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml does not exist on rebuild-from-database')
    if does_file_contain(in_file=admin_merge_yaml_path, search_for="new_resources:"):
        pass
    else:
        raise ValueError('System Error - admin-merge.yaml does not contain "new_resources: " ')

    copyfile(new_model_path, models_py_path)
    result_create = run_command(f'{set_venv} && ApiLogicServer rebuild-from-model --project_name=Rebuild --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    if not admin_merge_yaml_path.is_file():
        raise ValueError('System Error - admin-merge.yaml does not exist on rebuild-from-model')
    if does_file_contain(in_file=models_py_path, search_for="CategoryNew"):
        pass
    else:
        raise ValueError('System Error - admin-merge.yaml does not contain "new_resources: " ')

    result_create = run_command(f'alembic revision --autogenerate -m "Added Tables and Columns"',
        cwd=models_py_path.parent,
        msg=f'\nalembic revision')
    result_create = run_command(f'alembic upgrade head',
        cwd=models_py_path.parent,
        msg=f'\nalembic upgrade head')

    print(f'..rebuild tests compete')


def verify_include_models( project_name : str ='include_exclude',
                          check_for: List[str] = [], verify_found : bool = True):
    """
    Searches project's model.py file to insure each entry in check_classes is/is not present

    Args:
        project_name (str, optional): dir name of project. Defaults to 'include_exclude'.
        check_classes (List[str], optional): list of strings to search for. Defaults to [].
        verify_found (bool): check_for must exist or must *not* exist

    Raises:
        f: verify_include_models - expected string not found: {check_for}

    Returns:
        bool: True means all found
    """
    model_file_str = str(get_servers_install_path().joinpath(f'ApiLogicServer/{project_name}/database/models.py'))
    for each_term in check_for:
        is_in_file = does_file_contain(in_file = model_file_str, search_for=each_term)
        if verify_found and not is_in_file:
            raise Exception(f"{project_name} - expected string not found {each_term} ")
        if verify_found == False and is_in_file == True:
            raise Exception(f"{project_name}  - unexpected string found: {each_term} ")


def delete_build_directories(install_api_logic_server_path):
    if os.path.exists(install_api_logic_server_path):
        # rm -r ApiLogicServer.egg-info; rm -r build; rm -r dist
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('ApiLogicServer.egg-info')), msg="\ndelete egg ")
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('build')), msg="delete build ")
        delete_dir(dir_path=str(get_api_logic_server_path().joinpath('dist')), msg="delete dist ")
    try:
        os.mkdir(install_api_logic_server_path, mode = 0o777)
        os.mkdir(install_api_logic_server_path.joinpath('dockers'), mode = 0o777)
    except:
        print(f"Unable to create directory {install_api_logic_server_path} -- Windows dir exists?")

def docker_creation_tests(api_logic_server_tests_path):
    """ start docker, cp docker_coammands.sh, create projects at dev/servers/install/ApiLogicServer/dockers """
    """
        Yay!
        docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v /Users/val/dev/servers/install/ApiLogicServer/dockers:/localhost apilogicserver/arm-slim sh -c "export PATH=$PATH:/home/api_logic_server/bin && /bin/sh /localhost/docker-commands.sh"

        this runs:
        docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v /Users/val/dev/servers/install/ApiLogicServer/dockers:/localhost apilogicserver/arm-slim /home/api_logic_server/bin/ApiLogicServer welcome
        docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v /Users/val/dev/servers/install/ApiLogicServer/dockers:/localhost apilogicserver/arm-slim ls /localhost/
    """
    """
    run_command docker build -f docker/api_logic_server.Dockerfile -t apilogicserver/api_logic_server --rm .
    """
    import platform
    machine = platform.machine()
    api_logic_server_home_path = api_logic_server_tests_path.parent
    build_cmd = 'docker build -f docker/arm-slim.Dockerfile -t apilogicserver/arm-slim --rm .'
    if machine != "arm64":
        build_cmd = 'docker build -f docker/api_logic_server.Dockerfile -t apilogicserver/api_logic_server --rm .'
    build_container = run_command(build_cmd,
        cwd=api_logic_server_home_path,
        msg=f'\nBuild ApiLogicServer Docker Container at: {str(api_logic_server_home_path)}')
    print('built container')
    src = api_logic_server_tests_path.joinpath('creation_tests').joinpath('docker-commands.sh')
    dest = get_servers_install_path().joinpath('ApiLogicServer').joinpath('dockers')
    shutil.copy(src, dest)
    build_projects_cmd = (
        f'docker run -it --name api_logic_server --rm '
        f'--net dev-network -p 5656:5656 -p 5002:5002 ' 
        f'-v {str(dest)}:/localhost apilogicserver/arm-slim ' 
        f'sh -c "export PATH=$PATH:/home/api_logic_server/bin && /bin/sh /localhost/docker-commands.sh"'
    )
    if machine != "arm64":
        build_projects_cmd = (
            f'docker run -it --name api_logic_server --rm '
            f'--net dev-network -p 5656:5656 -p 5002:5002 ' 
            f'-v /Users/val/dev/servers/install/ApiLogicServer/dockers:/localhost apilogicserver/api_logic_server ' 
            f'sh -c "export PATH=$PATH:/home/api_logic_server/bin && /bin/sh /localhost/docker-commands.sh"'
        )
    build_projects = run_command(build_projects_cmd,
        cwd=api_logic_server_home_path,
        msg=f'\nBuilding projects from Docker container at: {str(api_logic_server_home_path)}')
    print('built projects from container')

def validate_nw():
    """
    With NW open, verifies:
    * Behave test
    * order nested
    * get_cats RPC
    """

    get_uri = "http://localhost:5656/order_nested_objects?Id=10643"
    r = requests.get(url=get_uri, headers=login())
    response_text = r.text
    result_data = json.loads(response_text) 
    assert result_data['data']['Id'] == 10643, \
        "order endpoint failed to find 10643"
    assert result_data['data']['OrderDetailListAsDicts'][1]['data']['ProductName'] == 'Chartreuse verte', \
        "OrderDetail does not contain 'Chartreuse verte'"


    get_uri = "http://localhost:5656/filters_cats"
    r = requests.get(url=get_uri, headers=login())
    response_text = r.text
    result_data = json.loads(response_text) 
    assert len(result_data['result']) == 4, \
        "Failed to get 4 filters_cats rows"

    post_uri = "http://localhost:5656/api/CategoriesEndPoint/get_cats"
    post_data = {}
    headers = login('u1')
    r = requests.post(url=post_uri, headers=headers, json=post_data)
    response_text = r.text
    status_code = r.status_code
    if status_code > 300:
        raise Exception(f'POST CategoriesEndPoint/get_cats failed - status_code = {status_code}, with response text {r.text}')
    result_data = json.loads(response_text)
    assert len(result_data['result']) == 1, \
        "Failed to get 1 CategoriesEndPoint/get_cats row - security ok?"
    assert result_data['result'][0]['Id'] == 1, \
        "Failed to get Id=1 from CategoriesEndPoint/get_cats"

    try:
        api_logic_project_behave_path = api_logic_project_path.joinpath('test').joinpath('api_logic_server_behave')
        api_logic_project_logs_path = api_logic_project_behave_path.joinpath('logs').joinpath('behave.log')
        result_behave = run_command(f'{python} behave_run.py --outfile={str(api_logic_project_logs_path)}',
            cwd=api_logic_project_behave_path,
            msg="\nBehave Test Run",
            show_output=True)
        if result_behave.returncode != 0:
            raise Exception("Behave Run Error")
        print("\nBehave tests run - now run report..\n")
        result_behave_report = run_command(f"{python} behave_logic_report.py run --prepend_wiki='reports/Behave Logic Report Intro.md' --wiki='reports/Behave Logic Report.md'",
            cwd=api_logic_project_behave_path,
            msg="\nBehave Logic Report",
            show_output=True)  # note: report lost due to rebuild tests
        if result_behave.returncode != 0:
            raise Exception("Behave Report Error")
    except:
        print(f'\n\n** Behave Test failed\nHere is log from: {str(api_logic_project_logs_path)}\n\n')
        f = open(str(api_logic_project_logs_path), 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()
        exit(result_behave.returncode)

    
    print("\nBehave tests & report - Success...\n")


def validate_opt_locking():
    """
    Verify optimistic locking

    1. Missing CheckSum
    2. Improper Checksum
    3. Proper Checksum
    4. Place_Order tests critical case - attribute order correct with aliased attrs

    Does not work, presumably due to see.  Tests moved to behave
    """
    dup_behave_tests = False  # they don't really work...
    if dup_behave_tests:
        patch_uri = "http://localhost:5656/api/Category/1/"
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Description": "x"
                    },
                    "type": "Category",
                    "id": "1"
                }
            }
        r = requests.patch(url=patch_uri, json=patch_args, headers=login())
        response_text = r.text
        result_data = json.loads(response_text) 
        assert "x cannot be" in response_text, "Opt Locking Failed: Missing Checksum test"

        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Description": "x",
                        "S_CheckSum": "Mismatch Checksum test"
                    },
                    "type": "Category",
                    "id": "1"
                }
            }
        r = requests.patch(url=patch_uri, json=patch_args, headers=login())
        response_text = r.text
        result_data = json.loads(response_text) 
        assert "Sorry, row altered by another" in response_text, "Opt Locking Failed: Mismatch Checksum test"

        patch_uri = "http://localhost:5656/api/Category/1/"
        patch_args = \
            {
                "data": {
                    "attributes": {
                        "Description": "x",
                        "S_CheckSum": "-2378822108675121962"
                    },
                    "type": "Category",
                    "id": "1"
                }
            }
        r = requests.patch(url=patch_uri, json=patch_args, headers=login())
        response_text = r.text
        result_data = json.loads(response_text) 
        assert "x cannot be" in response_text, "Opt Locking Failed: Matching Checksum test"

    return


def validate_sql_server_types():
    """
    Verify sql server types and extended builder
    See https://valhuber.github.io/ApiLogicServer/Project-Builders/
    """
    post_uri = "http://localhost:5656/api/udfEmployeeInLocation/udfEmployeeInLocation"
    args = {
        "location": "Sweden"
    }
    r = requests.post(url=post_uri, json=args)
    response_text = r.text
    result_data = json.loads(response_text) 
    assert len(result_data["result"]) == 2, "TVF/udfEmployeeInLocation: Did not find 2 expected result rows"
    # TODO - why once assert "Sweden" == result_data["result"][0]["Location"], "TVF/udfEmployeeInLocation: Result row 1 does not contain Sweden"
    bad_response = False
    if bad_response:
        print(f'\nTODO - TVF: why once assert "Sweden" == result_data["result"][0]["Location"], "TVF/udfEmployeeInLocation: Result row 1 does not contain Sweden"\n')
    else:
        assert "Sweden" == result_data["result"][0]["Location"], "TVF/udfEmployeeInLocation: Result row 1 does not contain Sweden"

    get_uri = "http://localhost:5656/api/DataType/?fields%5BDataType%5D=Key%2Cchar_type%2Cvarchar_type&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=id"
    r = requests.get(url=get_uri)
    response_text = r.text
    result_data = json.loads(response_text) 
    assert len(result_data["data"]) == 1, "TVF/DataTypes: Did not find 1 expected result row"
    return


# ***************************
#        MAIN CODE
# ***************************

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
program_dir = str(current_path)
os.chdir(program_dir)  # so admin app can find images, code

python = find_valid_python_name()  # geesh - allow for python vs python3

personal_env_path = Path(current_path).joinpath("env.py")
""" personal env (excluded in .gitignore)"""
if os.path.exists(personal_env_path):
    from env import Config  
elif platform == "darwin":  # no personal path, use platform defaults
    from env_mac import Config
elif platform == "win32":
    from env_win import Config
elif platform.startswith("linux"):
    from env_linux import Config
else:
    print("unknown platform")

set_venv = Config.set_venv
db_ip = Config.docker_database_ip

install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")   # eg /Users/val/dev/servers/install/ApiLogicServer
api_logic_project_path = install_api_logic_server_path.joinpath('ApiLogicProject')
api_logic_server_tests_path = Path(os.path.abspath(__file__)).parent.parent

api_logic_server_cli_path = get_api_logic_server_path().\
                            joinpath("api_logic_server_cli").joinpath('api_logic_server.py')  # eg, /Users/val/dev/ApiLogicServer/api_logic_server_cli/api_logic_server.py

with io.open(str(api_logic_server_cli_path), "rt", encoding="utf8") as f:
    api_logic_server_version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

print(f"\n\n{__file__} 1.1 running")
print(f'  Builds / Installs API Logic Server to install_api_logic_server_path: {install_api_logic_server_path}')
print(f'  Creates Sample project (nw), starts server and runs Behave Tests')
print(f'  Rebuild tests')
print(f'  Creates other projects')
print(f'  Creates Docker projects (wip)')
print('\n')

if not os.path.isdir(install_api_logic_server_path):
    os.makedirs(install_api_logic_server_path)

# stop_server(msg="BEGIN TESTS\n")  # just in case server left running

debug_script = False
if debug_script:
    import platform as platform
    machine = platform.machine()
    api_logic_server_install_path = os.path.abspath(install_api_logic_server_path.parent)
    result_venv = run_command(f'pwd && {set_venv} && pip freeze',
        cwd=api_logic_server_install_path,
        msg=f'\nInstall ApiLogicServer at: {str(api_logic_server_install_path)}')
    print(result_venv.stdout.decode())  # should say pyodbc==4.0.34

if Config.do_install_api_logic_server:
    delete_dir(dir_path=str(install_api_logic_server_path), msg=f"delete install: {install_api_logic_server_path} ")
    delete_build_directories(install_api_logic_server_path)

    api_logic_server_home_path = api_logic_server_tests_path.parent
    result_build = run_command(f'{python} setup.py sdist bdist_wheel',
        cwd=api_logic_server_home_path,
        msg=f'\nBuild ApiLogicServer at: {str(api_logic_server_home_path)}')

    result_install = run_command(f'{python} -m venv venv && {set_venv} && {python} -m pip install {str(api_logic_server_home_path)}',
        cwd=install_api_logic_server_path,
        msg=f'\nInstall ApiLogicServer at: {str(install_api_logic_server_path)}')

    delete_build_directories(install_api_logic_server_path)

    if platform == "win32":
        print("not for windows")  # https://github.com/mkleehammer/pyodbc/issues/1010
    else:
        result_pyodbc = run_command(
            f'{set_venv} && {python} -m pip install pyodbc==4.0.34',
            cwd=install_api_logic_server_path,
            msg=f'\nInstall pyodbc')

if len(sys.argv) > 1 and sys.argv[1] == 'build-only':
    print("\nBuild/Install successful\n\n")
    exit (0)

if Config.do_create_api_logic_project:
    result_create = run_command(f'{set_venv} && ApiLogicServer create --project_name=ApiLogicProject --db_url=',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate ApiLogicProject at: {str(install_api_logic_server_path)}')
    result_create = run_command(f'{set_venv} && ApiLogicServer tutorial',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Tutorial at: {str(install_api_logic_server_path)}')

if Config.do_run_api_logic_project:  # so you can start and set breakpoint, then run tests
    start_api_logic_server(project_name="ApiLogicProject")
    
if Config.do_test_api_logic_project:
    validate_opt_locking()
    validate_nw()
    stop_server(msg="*** NW TESTS COMPLETE ***\n")

if Config.do_multi_database_test:
    multi_database_tests()

if Config.do_rebuild_tests:
    rebuild_tests()

if Config.do_other_sqlite_databases:
    chinook_path = get_api_logic_server_path().joinpath('api_logic_server_cli').joinpath('database').joinpath('Chinook_Sqlite.sqlite')
    chinook_url = f'sqlite:///{chinook_path}'
    run_command(f'{set_venv} && ApiLogicServer create --project_name=chinook_sqlite --db_url={chinook_url}',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate chinook_sqlite at: {str(install_api_logic_server_path)}')
    run_command(f'{set_venv} && ApiLogicServer create --project_name=classicmodels_sqlite --db_url=classicmodels',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate classicmodels.sqlite at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='classicmodels_sqlite')
    stop_server(msg="classicmodels_sqlite\n")
    run_command(f'{set_venv} && ApiLogicServer create --project_name=todo_sqlite --db_url=todo',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate todo.sqlite at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='todo_sqlite')
    stop_server(msg="todo\n")

if Config.do_include_exclude:
    filter_path = str(get_api_logic_server_path().joinpath('api_logic_server_cli/database'))

    run_command(f'{set_venv} && ApiLogicServer create --project_name=include_exclude_nw --db_url=nw- --include_tables={filter_path}/table_filters_tests_nw.yml',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate include_exclude_typical at: {str(install_api_logic_server_path)}')
    verify_include_models( project_name='include_exclude_nw',
                          check_for = ["Location"],
                          verify_found=False)
    start_api_logic_server(project_name='include_exclude_nw') 
    stop_server(msg="include_exclude_nw\n")

    run_command(f'{set_venv} && ApiLogicServer create --project_name=include_exclude_nw_1 --db_url=nw- --include_tables={filter_path}/table_filters_tests_nw_1.yml',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate include_exclude_typical at: {str(install_api_logic_server_path)}')
    verify_include_models( project_name='include_exclude_nw_1',
                          check_for = ["Location", "OrderDetailList"],
                          verify_found=False)
    start_api_logic_server(project_name='include_exclude_nw_1')
    stop_server(msg="include_exclude_nw_1\n")

    run_command(f'{set_venv} && ApiLogicServer create --project_name=include_exclude --db_url=table_filters_tests --include_tables={filter_path}/table_filters_tests.yml',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate include_exclude at: {str(install_api_logic_server_path)}')
    verify_include_models( project_name='include_exclude',
                          check_for = ["class I", "class I1", "class J", "class X"])
    start_api_logic_server(project_name='include_exclude')
    stop_server(msg="include_exclude\n")

    run_command(f'{set_venv} && ApiLogicServer create --project_name=include_exclude_typical --db_url=table_filters_tests --include_tables={filter_path}/table_filters_tests_typical.yml',
        cwd=install_api_logic_server_path,
        msg=f'\nCreate include_exclude_typical at: {str(install_api_logic_server_path)}')
    verify_include_models( project_name='include_exclude_typical',
                          check_for = ["class X", "class X1"])
    start_api_logic_server(project_name='include_exclude_typical')
    stop_server(msg="include_exclude_typical\n")


if Config.do_allocation_test:
    allocation_project_path = install_api_logic_server_path.joinpath('Allocation')
    run_command(f'{set_venv} && ApiLogicServer create --project_name=Allocation --db_url=allocation',
            cwd=install_api_logic_server_path,
            msg=f'\nCreate Allocation at: {str(install_api_logic_server_path)}')    
    start_api_logic_server(project_name="Allocation")

    try:
        print("\nProceeding with Allocation tests...\n")
        allocation_tests_path = allocation_project_path.joinpath('test')
        run_command(f'sh test.sh',
            cwd=allocation_tests_path,
            msg="\nAllocation Test")
    except:
        print(f'\n\n** Allocation Test failed\n\n')
        exit(1)
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
        f"{set_venv} && ApiLogicServer create --project_name=TVF --extended_builder=* --db_url='mssql+pyodbc://sa:Posey3861@{db_ip}:1433/SampleDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate SqlServer TVF at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='TVF')
    validate_sql_server_types()
    stop_server(msg="TVF\n")

    result_docker_sqlserver = run_command(
        f"{set_venv} && ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:Posey3861@{db_ip}:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate SqlServer NORTHWND at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='sqlserver')
    stop_server(msg="sqlserver\n")
    """
url above works, but this run config fails:
        {
            "name": "SQL Server Types",
            "type": "python",
            "request": "launch",
            "cwd": "${workspaceFolder}/api_logic_server_cli",
            "program": "cli.py",
            "redirectOutput": true,
            "argsExpansion": "none",
            "args": ["create",
                "--project_name=../../servers/sqlserver-types",
fails           "--db_url=mssql+pyodbc://sa:Posey3861@localhost:1433/SampleDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no",

works            --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'",
    """

if Config.do_docker_postgres:
    result_docker_postgres = run_command(
        f"{set_venv} && ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@{db_ip}/postgres",
        cwd=install_api_logic_server_path,
        msg=f'\nCreate Postgres postgres (nw) at: {str(install_api_logic_server_path)}')
    start_api_logic_server(project_name='postgres')
    stop_server(msg="postgres\n")

if Config.do_docker_creation_tests:
    docker_creation_tests(api_logic_server_tests_path)

print("\n\nSUCCESS -- END OF TESTS")

print(f"\n\nRelease {api_logic_server_version}?\n")
print(f'cd {str(get_api_logic_server_path())}')
print(f"{python} setup.py sdist bdist_wheel")
print(f"{python} -m twine upload  --username vhuber --password PypiPassword --skip-existing dist/*  \n\n")
