#!/bin/bash
export installrel="../../../../dev/servers/install"
export install=$(cd "$(dirname "${installrel}")"; pwd)/$(basename "${installrel}")
export dockers=${install}/ApiLogicServer/dockers

echo ""
echo "Creates docker servers at ${dockers}"  # e.g., /Users/val/dev/servers/install/ApiLogicServer/dockers

if [ $# -eq 0 ]
    then
        echo ""
        echo "  sh create-dockers.sh [ go [all] ]"
        echo ""
        exit 0
    fi

echo ""
read -p "Press [Enter] for docker server creation at ${dockers}> "

set -x

mkdir ${dockers}
cp docker-commands.sh ${dockers}/.
ls ${dockers}
set +x

echo "\n\n****************"
echo "run this in docker: sh /localhost/docker-commands.sh [go]"
echo "   .. go for Sql/Server and Postgres (amd, not arm)"
echo "****************\n\n"

if [ $# -eq 2 ]

    then

        docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${dockers}:/localhost apilogicserver/api_logic_server
        # eg docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v /Users/val/dev/servers/install/ApiLogicServer/dockers:/localhost apilogicserver/api_logic_server 
        #    docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server
        # echo "running docker-commands"

        # docker exec api_logic_server docker-commands.sh only runs when docker completes
        # docker exec -it api_logic_server docker-commands.sh

    else

        docker run -it --name api_logic_server-arm-slim --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${dockers}:/localhost apilogicserver/arm-slim

fi