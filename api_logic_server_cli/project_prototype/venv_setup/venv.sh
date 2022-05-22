#!/bin/xxx

if [ $# -eq 0 ]
    then
        echo " "
        echo "Installs virtual environment (as venv)"
        echo " "
        echo " IMPORTANT - Mac only, not required for docker-based projects"
        echo " .. Windows: https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start"
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
    else
        python3 -m venv venv
fi

source venv/bin/activate   # ubuntu/linux uses . venv/bin/activate 
pip install -r requirements.txt
