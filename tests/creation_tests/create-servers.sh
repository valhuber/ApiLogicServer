#!/bin/bash
export install="../../../../dev/servers/install"
export ApiLogicServer=${install}/ApiLogicServer
if [ $# -eq 0 ]
    then
        echo ""
        echo "Creates servers at ${ApiLogicServer}"
        # ls ${ApiLogicServer}
        echo ""
        echo "  sh rebuild_servers_install.sh [ go ]"
        # ls ${ApiLogicServer}
        echo ""
        exit 0
    fi

read -p "Press [Enter] for server creation> "

set -x
pushd ${ApiLogicServer}

alias activate='ApiLogicServer/venv/bin/activate'
source venv/bin/activate
ApiLogicServer create --project_name=ApiLogicProject --db_url=

ApiLogicServer create --project_name=sqlserver --db_url='mssql+pyodbc://sa:posey386!@localhost:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no'

ApiLogicServer create --project_name=classicmodels --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'

ApiLogicServer create --project_name=postgres --db_url=postgresql://postgres:p@localhost/postgres

ApiLogicServer create --project_name=Allocation --db_url=sqlite:////Users/val/dev/ApiLogicServer/tests/allocation/allocation.sqlite

echo "\n\n******\nuse vsc to run api_logic_server_run.py (Launch Config: Python: Current File) "
