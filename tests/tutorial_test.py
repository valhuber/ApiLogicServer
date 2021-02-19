import logging
import os
import subprocess
import sys
from pathlib import Path
import json

import sqlalchemy

from logic_bank_utils import util as logic_bank_utils

from logic_bank.rule_bank import rule_bank_withdraw
from logic_bank.rule_type.parent_check import ParentCheck

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="ApiLogicServer", my_file=__file__)
print("\n" + did_fix_path + "\n\n" + sys_env_info + "\n\n")


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def setup_logging():
    logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
    logic_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
    handler.setFormatter(formatter)
    logic_logger.addHandler(handler)

    do_engine_logging = False
    engine_logger = logging.getLogger('engine_logger')  # for internals
    if do_engine_logging:
        engine_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
        handler.setFormatter(formatter)
        engine_logger.addHandler(handler)


def get_project_dir() -> str:
    """
    :return: ApiLogicServer dir, eg, /Users/val/dev/ApiLogicServer
    """
    path = Path(__file__)
    parent_path = path.parent
    parent_path = parent_path.parent
    return parent_path


def run_command(cmd: str, env=None, msg: str = "") -> str:
    """ run shell command

    :param cmd: string of command to execute
    :param msg: optional message
    :return:
    """
    log_msg = ""
    if msg != "Execute command:":
        log_msg = msg + " with command:"
    # print(f'{log_msg} {cmd}')

    use_env = env
    if env is None:
        project_dir = get_project_dir()
        python_path = str(project_dir) + "/venv/lib/python3.9/site_packages"
        use_env = os.environ.copy()
        # print("\n\nFixing env for cmd: " + cmd)
        if hasattr(use_env, "PYTHONPATH"):
            use_env["PYTHONPATH"] = python_path + ":" + use_env["PYTHONPATH"]  # eg, /Users/val/dev/ApiLogicServer/venv/lib/python3.9
            # print("added PYTHONPATH: " + str(use_env["PYTHONPATH"]))
        else:
            use_env["PYTHONPATH"] = python_path
            # print("created PYTHONPATH: " + str(use_env["PYTHONPATH"]))
    use_env_debug = False  # not able to get this working
    if use_env_debug:
        result_b = subprocess.check_output(cmd, shell=True, env=use_env)
    else:
        result_b = subprocess.check_output(cmd, shell=True)
    result = str(result_b)  # b'pyenv 1.2.21\n'
    result = result[2: len(result) - 3]
    tab_to = 20 - len(cmd)
    spaces = ' ' * tab_to
    debug = False
    if debug:
        print(f'\n\n{log_msg} {cmd} \n\nresult: {spaces}{result}')
    return result

setup_logging()

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(basedir)

"""
    Test 1 - Basic Read Test
"""
msg = "Test 1 - Basic GET Test"
print(f'\n{msg}')

cmd = 'curl -X GET "http://localhost:5000/Order\
?include=\
&fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CAmountTotal\
&page%5Boffset%5D=0\
&page%5Blimit%5D=2\
&sort=Id%2CCustomerId%2CEmployeeId\
&filter%5BCustomerId%5D=ALFKI"\
 -H  "accept: application/vnd.api+json" \
 -H  "Content-Type: application/vnd.api+json"'

result = run_command(cmd=cmd, msg=msg)
result_line_breaks = result.replace("\\n", " ")

# print (f'\n\nresult: {result_line_breaks}')
try:
    # force error result_line_breaks[3:4] = "jjj"
    result_dict = json.loads(result_line_breaks)
    result_dot = DotDict(result_dict)
    row_container = DotDict(result_dot.data[1])
    row = DotDict(row_container.attributes)
    print (f'\n\nresult row: {row}')
except:
    e = sys.exc_info()[0]
    print(f'ERROR: msg - {e}')
    exit(1)


"""
    Test 2 - Patch: Logic Enabled Updates
"""
msg = "Patch: Logic Enabled Updates"
print(f'\n{msg}')

msg = "Test 2 - PATCH seeking 'exceeds credit' constraint"
cmd = '\
curl -vX PATCH "http://localhost:5000/Customer/ALFKI/"\
 -H  "accept: application/vnd.api+json"\
 -H  "Content-Type: application/json"\
 -d \'\
{\"data\": {\
     \"attributes\": {\
        \"CreditLimit\": 100\
     },\
  \"type\": \"Customer\",\
  \"id\": \"ALFKI\"\
  }\
}\'\
'

result = run_command(cmd=cmd, msg=msg)
result_line_breaks = result.replace("\\n", " ")

# print (f'\n\nresult: {result_line_breaks}')
try:
    # force error result_line_breaks[3:4] = "jjj"
    if "exceeds credit" in result:
        print(f'{msg} SUCCESS - "exceeds credit" detected')
    else:
        print(f'ERROR: {msg} did not contain "exceeds credit"')
        exit(1)
except:
    e = sys.exc_info()[0]
    print(f'ERROR: {msg} - {e}')
    exit(1)

print("\nSuccessful Exit")
