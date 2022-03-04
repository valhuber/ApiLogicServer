#!/bin/bash
export install="../../../../dev/servers/install"
export ApiLogicServer=${install}/ApiLogicServer
if [ $# -eq 0 ]
    then
        echo ""
        echo "Removes / reinstalls venv at ${ApiLogicServer}"
        # ls ${ApiLogicServer}
        echo ""
        echo "  sh rebuild_servers_install.sh [ go ]"
        # ls ${ApiLogicServer}
        echo ""
        exit 0
    fi

read -p "Press [Enter] to prepare for re-install> "

set -x
# alias activate='ApiLogicServer/venv/bin/activate'

rm -r ${ApiLogicServer}/venv
python3 -m venv ${ApiLogicServer}/venv

set +x
echo ""

echo "venv created at ${ApiLogicServer}"
ls ${install}
echo "Next Steps:"
echo "   cd ${ApiLogicServer}"
echo "   source venv/bin/activate  # ;a"
echo "   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ApiLogicServer==4.03.01"

echo " "
