#!/usr/bin/env python
"""
quick view of python environment

sudo chmod +x py.py
./py.py
in .zshrc: python py.py

"""

import os, sys
import subprocess


def show(cmd: str):
    try:
        result_b = subprocess.check_output(cmd, shell=True)
        result = str(result_b)  # b'pyenv 1.2.21\n'
        result = result[2: len(result)-3]
        tab_to = 20 - len(cmd)
        spaces = ' ' * tab_to
        print(f'{cmd}: {spaces}{result}')
    except Exception as e:
        # print(f'Failed: {cmd} - {str(e)}')
        pass


def python_status():
    print("\nPython Status here, 1.0\n")
    # show("pyenv --version")  # does not exist in docker...
    # show("pyenv global")
    # show("pyenv version-name")
    # show("virtualenv --version")
    show("python --version")
    print("PYTHONPATH..")
    for p in sys.path:
        print(".." + p)
    print("")
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f'hostname: {hostname}, local_ip (gethostbyname): {local_ip}')
    print("")

if __name__ == '__main__':
    python_status()
