if [ $# -eq 0 ]
    then
        echo " "
        echo "Installs virtual environment (as venv)"
        echo " "
        echo " IMPORTANT - Mac/Linux only, not required for docker-based projects"
        echo " .. Windows: https://github.com/valhuber/ApiLogicServer/wiki/Quick-Start"
        echo " "
        echo "Usage:"
        echo "  cd ApiLogicProject  # your project directory"
        echo "  sh bin/venv.sh go"
        echo " "
        exit 0
    fi

set +x
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt