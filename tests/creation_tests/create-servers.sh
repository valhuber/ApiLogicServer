#!/bin/bash
export installrel="../../../../dev/servers/install"
export install=$(cd "$(dirname "${installrel}")"; pwd)/$(basename "${installrel}")
export ApiLogicServer=${install}/ApiLogicServer

if [ $# -eq 0 ]
    then
        echo ""
        echo "Creates venv and servers at ${ApiLogicServer}"
        # ls ${ApiLogicServer}
        echo ""
        echo "  sh create-servers.sh [ venv | run ]"
        # ls ${ApiLogicServer}
        echo ""
        exit 0
    fi

if [ "$1" = "create" ]
    then
        read -p "Press [Enter] for server creation (venv required)> "

        set -x
        pushd ${ApiLogicServer}

        alias activate='ApiLogicServer/venv/bin/activate'
        source venv/bin/activate

        ApiLogicServer create --project_name=ApiLogicProject --db_url=

        ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no'

        ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'

        ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres

        popd

        echo "\n\n******\nuse vsc to run api_logic_server_run.py (Launch Config: Python: Current File) "
    fi

if [ "$1" = "venv" ]
    then
        read -p "Press [Enter] to remove / reinstall ${ApiLogicServer}/venv (deactivate first) > "

        rm -r ${ApiLogicServer}/venv
        python3 -m venv ${ApiLogicServer}/venv

        echo ""
        echo "venv created, now..."
        echo "  source ${ApiLogicServer}/venv/bin/activate  # ;a"
        echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ApiLogicServer==4.03.03"

        echo " "
    fi