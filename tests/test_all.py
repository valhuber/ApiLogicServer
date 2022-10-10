import subprocess, os, sys
from pathlib import Path
# import api_logic_server_cli.create_from_model.api_logic_server_utils as create_utils


def find_valid_python_name() -> str:
    '''
        sigh.  On *some* macs, python fails so we must use python3.
        
        return 'python3' in this case
    '''
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


def run_command(cmd: str, env=None, msg: str = "", new_line: bool=False, cwd: Path=None) -> str:
    """ run shell command

    :param cmd: string of command to execute
    :param env:
    :param msg: optional message (no-msg to suppress)
    :return:
    """

    from subprocess import DEVNULL, STDOUT, check_call

    if cmd.startswith('python'):
        valid_python_name = find_valid_python_name()
        cmd = cmd.replace("python", valid_python_name)
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    if msg == "no-msg":
        log_msg = ""
    else:
        print(f'{log_msg} {cmd}')
    if new_line:
        print("")

    result_b = None
    try:
        result_b = subprocess.check_output(
            cmd,
            shell=True,
            cwd=cwd,
            stderr=subprocess.STDOUT) # , stderr=subprocess.STDOUT)  # causes hang on docker
        result = str(result_b)  # b'pyenv 1.2.21\n' 
        result = result[2: len(result) - 3]
        tab_to = 20 - len(cmd)
        spaces = ' ' * tab_to
        if msg == "no-msg":
            pass
        elif result != "" and result != "Downloaded the skeleton app, good coding!":
            pass
            print(f'{log_msg} {cmd}')  #  result: {spaces}{result}')]
    except:
        print(f'\n\n*** Failed on {cmd}')
        raise
    return result

api_logic_server_path_str = get_api_logic_server_path()
# os.chdir(api_logic_server_path_str)

run_command(f'echo "start"; pwd; ls; echo "end"', msg="\nMulti-Cmd Lines")

# run_command(f'python3 setup.py sdist bdist_wheel', msg="\nBuild Wheel", cwd=get_api_logic_server_path())

install_api_logic_server_path = get_servers_install_path().joinpath("ApiLogicServer")
if os.path.exists(install_api_logic_server_path):
    delete_dir(dir_path=str(install_api_logic_server_path), msg="delete install ")
os.mkdir(install_api_logic_server_path)

run_command(f'python3 -m venv venv; source venv/bin/activate; python3 -m pip install /Users/val/dev/ApiLogicServer',
    cwd=install_api_logic_server_path,
    msg="\nCreate venv")

run_command(f'source venv/bin/activate; ApiLogicServer create --project_name=ApiLogicProject --db_url=',
    cwd=install_api_logic_server_path,
    msg="\nCreate venv")

server = subprocess.Popen(['python3','ApiLogicProject/api_logic_server_run.py'])
print(f'\n\nserver running - server: {str(server)}\n')