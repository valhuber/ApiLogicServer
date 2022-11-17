""" test configuration variables. """


class Config:
    """ api_logic_server_test configuration  """


    # ***********************
    #   what tests to run
    # ***********************

    default_setting = True  # simplify enable / disable most

    do_install_api_logic_server = default_setting   # verify build wheel and local install
    
    do_create_api_logic_project = default_setting   # create the default project
    do_run_api_logic_project = default_setting      # start the server 
    do_test_api_logic_project = default_setting     # run the behave tests (test logic, api)

    do_allocation_test = default_setting            # create / run / test allocation project

    do_other_sqlite_databases = default_setting     # classic models

    do_docker_mysql = default_setting               # requires docker database be running
    do_docker_postgres = default_setting            # requires docker database be running
    do_docker_sqlserver = default_setting           # requires docker database be running



    # ***********************
    #   platform specific
    # ***********************

    set_venv = '. venv/bin/activate'
    '''typical source "venv/bin/activate" does not persist over cmds, see...
        https://github.com/valhuber/ubuntu-script-venv/blob/main/use-in-script.sh '''

    docker_database_ip = 'localhost'
    ''' for virtual machine access, set this to host IP '''

