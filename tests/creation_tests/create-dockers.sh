#!/bin/bash
export installrel="../../../../dev/servers/install"
export install=$(cd "$(dirname "${installrel}")"; pwd)/$(basename "${installrel}")
export dockers=${install}/ApiLogicServer/dockers

echo ""
echo "Creates docker servers at ${dockers}"

if [ $# -eq 0 ]
    then
        echo ""
        echo "  sh create-dockers.sh [ go ]"
        echo ""
        exit 0
    fi

echo ""
read -p "Press [Enter] for docker server creation at ${dockers}> "

set -x

mkdir ${dockers}
cp docker-commands.sh ${dockers}/.
set +x

echo "\n\n****************"
echo "run this in docker: sh /localhost/docker-commands.sh"
echo "****************\n\n"

docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${dockers}:/localhost apilogicserver/api_logic_server

# echo "running docker-commands"

# docker exec api_logic_server docker-commands.sh only runs when docker completes
# docker exec -it api_logic_server docker-commands.sh