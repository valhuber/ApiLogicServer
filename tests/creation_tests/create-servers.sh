#!/bin/bash
export installrel="../../../../dev/servers/install"
export install=$(cd "$(dirname "${installrel}")"; pwd)/$(basename "${installrel}")
export ApiLogicServer=${install}/ApiLogicServer

if [ $# -eq 0 ]
   then
      echo ""
      echo "Creates servers at ${ApiLogicServer}"
      # ls ${ApiLogicServer}
      echo ""
      echo "  sh create-servers.sh create [all]"
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

      ApiLogicServer create --project_name=chinook_sqlite --db_url={install)/Chinook_Sqlite.sqlite}

      ApiLogicServer create --project_name=classicmodels \
         --db_url='mysql+pymysql://root:p@localhost:3306/classicmodels'

      ApiLogicServer create --project_name=postgres \
         --db_url=postgresql://postgres:p@localhost/postgres
    
      ApiLogicServer create --project_name=sqlserver \
         --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'


      if [ $# -gt 2 ]
         then
            read -p "Is this AMD??> "
            # docs, docker-commands using 17 trusted=no, local install requires 18, but...
            # sort fields must not use images, large text (eg, just use names for category, customer)

            ApiLogicServer create --project_name=sqlserver \
               --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no'

            ApiLogicServer create --project_name=sqlserver-types \
               --db_url='mssql+pyodbc://sa:Posey3861@localhost:1433/SampleDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no' \
               --extended_builder=  

         else
            echo "\n*** Short version - no MS SqlServer ***\n"       
      fi

      popd

      echo "\n\n******\nuse vsc to run api_logic_server_run.py (Launch Config: Python: Current File) "
   fi
