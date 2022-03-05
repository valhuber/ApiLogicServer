#!/bin/bash
export target="../../../servers/install/ApiLogicServer"
export project=${target}/Allocation-test
# ls $target
# ls $project  ../../../servers/install/ApiLogicServer/Allocation-test

if [ $# -eq 0 ]
    then
        echo " "
        echo "\nRebuilds Allocation at ${project}, from dev env (no venv)"
        echo " "
        echo " IMPORTANT - ApiLogicServer/tests/allocation folder"
        echo " "
        echo "  sh setup-allocation.sh [ create | x ]"
        echo " "
        exit 0
    else
        pushd ../allocation
        sh setup_allocation.sh $1
        popd
    fi