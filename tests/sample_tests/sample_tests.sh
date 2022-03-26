#!/bin/bash
export target="../../../servers"
export project=${target}/ApiLogicProject
if [ $# -eq 0 ]
    then
        echo " "
        echo "\n Runs logic audit test - using shell scripts for testing"
        echo "   1. Run Launch-Config to start the server: 2 - Debug ApiLogicProject"
        echo " "
        echo " This runs:"
        echo "   1. ${project}/test/server_test.sh "
        echo "   2. ${project}/test/server_test.py "
        echo " "
        echo " Example:"
        echo "  sh sample_tests.sh [ go ]"
        echo " "
        exit 0
    fi

pushd ${project}/test
sh basic/server_test.sh go
python basic/server_test.py go
popd

pwd

exit 0
