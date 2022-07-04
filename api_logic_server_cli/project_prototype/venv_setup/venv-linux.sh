#!/bin/bash

if [ $# -eq 0 ]
    then
        echo " "
        echo "Installs virtual environment (as venv)"
        echo " "
        echo " IMPORTANT - Linux only, not required for docker-based projects"
        echo " .. Windows: https://valhuber.github.io/ApiLogicServer/Project-Env/"
        echo " "
        echo "Usage:"
        echo "  cd ApiLogicProject     # your project directory"
        echo "  sh bin/venv.sh go      # for python3, or..."
        echo "  sh bin/venv.sh python  # for python"
        echo " "
        exit 0
    fi

if [ "$1" = "python" ]
    then
        python -m venv venv
        . venv/bin/activate  # Mac uses  uses source venv/bin/activate
        python -m pip install -r requirements.txt
    else
        python3 -m venv venv
        . venv/bin/activate  # Mac uses  uses source venv/bin/activate
        python3 -m pip install -r requirements.txt
fi
