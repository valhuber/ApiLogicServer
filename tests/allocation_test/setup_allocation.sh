#!/bin/bash
export target="../../../servers/install/ApiLogicServer"
export project=${target}/Allocation
# ls $target
# ls $project  ../../../servers/install/ApiLogicServer/Allocation-test

if [ $# -eq 0 ]
    then
        echo " "
        echo "\nRebuilds Allocation at ${project}, from dev env (no venv)"
        echo " "
        echo " IMPORTANT - cd ApiLogicServer/tests/allocation folder"
        echo " "
        echo "  sh setup-allocation.sh [ create | x ]"
        echo " "
        exit 0
  else
    if [ "$1" = "create" ]
        then
            echo "\n\nRebuilds Allocation at ${project}, from dev env (no venv)"
            read -p "Press [Enter] to proceed> "
            echo ""

            set -x
            python ../../api_logic_server_cli/cli.py  create --project_name=${project} --db_url=sqlite:///allocation.sqlite

            python3 -m venv ${project}/venv
            alias activate='${project}/venv/bin/activate'
            $activate
            set +x
            echo "now running: pip install -r ${project}/requirements.txt"
            pip install -r ${project}/requirements.txt

            echo "\n\nNow running: pip install -r ${project}/requirements.txt"
            set -x
            pwd
            cp -rf Allocation-src/* ${project}
            rm ${project}/Dockerfile

            echo "\nProject / venv created, Logic copied from Allocation-src, Starting server...\n"
            set +x
        fi
        echo "\n\n*******************************"
        echo "\nStarting server... ${project}/api_logic_server_run.py"
        echo " "
        echo ".. Test: cd ${project}/test;  sh test.sh \n"
        echo "\*******************************\n\n"
        set -x
        ls ${project}
        pushd ${project}
        python api_logic_server_run.py
        popd
        set +x
        echo "Server stopped"
    fi