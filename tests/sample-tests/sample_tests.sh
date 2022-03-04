#!/bin/bash
export target="../../../servers"
export project=${target}/ApiLogicProject
if [ $# -eq 0 ]
    then
        echo " "
        echo "\n Runs logic audit test - using shell scripts for testing"
        echo " "
        echo " IMPORTANT:"
        echo "   1. Server running on localhost:5656 "
        echo "   2. This runs ${project}/test/server_test.sh "
        echo " "
        echo "  sh sample_tests.sh [ go ]"
        echo " "
        exit 0
    fi

pushd ${project}/test
sh server_test.sh go
popd

pwd

exit 0
