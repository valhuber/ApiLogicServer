#!/bin/bash
export installrel="../../../../dev/servers/install"
export install=$(cd "$(dirname "${installrel}")"; pwd)/$(basename "${installrel}")
export ApiLogicServer=${install}/ApiLogicServer

if [ $# -eq 0 ]
    then
        echo ""
        echo "Creates venv at ${ApiLogicServer}"
        # ls ${ApiLogicServer}
        echo ""
        echo "  sh create-install.sh venv"
        # ls ${ApiLogicServer}
        echo ""
        exit 0
    fi

if [ "$1" = "venv" ]
    then
        read -p "Press [Enter] to remove / reinstall ${ApiLogicServer}/venv (deactivate first) > "

        rm -r ${ApiLogicServer}
        mkdir ${install}/ApiLogicServer
        python3 -m venv ${ApiLogicServer}/venv

        echo ""
        echo "venv created, now..."
        echo "  source ${ApiLogicServer}/venv/bin/activate  # ;a"
        echo "  python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ApiLogicServer==5.02.17"

        echo " "
    fi