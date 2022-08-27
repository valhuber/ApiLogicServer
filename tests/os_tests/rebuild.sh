#!/bin/bash

echo ""
echo "removes / reinstalls venv"
read -p "Press [Enter] to prepare for re-install> ", answer
echo ""

set -x
alias activate='ApiLogicServer/venv/bin/activate'

rm -r ApiLogicServer/venv
python3 -m venv ApiLogicServer/venv
# $activate
set +x

# source ApiLogicServer/venv/bin/activate

# pip install -r requirements.txt
echo ""

echo now
echo "cd ApiLogicServer; source venv/bin/activate"
echo "python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ApiLogicServer==4.01.07"

echo " "
