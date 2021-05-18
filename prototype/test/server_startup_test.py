import os
import sys
import util

server_tests_enabled = False  # use True to invoke server_tests on server startup

util.log("server_tests 1.0")


def server_tests(host, port, version):
    """ called by api_logic_server_run.py, for any tests on server start (see default sample)
        args
            host - server host
            port - server port
            version - ApiLogicServer version
    """
    util.log(f'\n\ntest.server_startup_test version {version} -- server_tests("{host}", "{port}"')
    pass
