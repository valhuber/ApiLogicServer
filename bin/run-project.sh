#!/bin/bash

echo " "
echo "run-project: $1"
if [ -z "$2" ]; then
    echo ".. project-fixup script not supplied"
else
    echo ".. project-fixup script: $2"
fi
echo " "

# docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server sh /home/api_logic_server/bin/run-project.sh https://github.com/valhuber/Tutorial-ApiLogicProject.git /localhost/Project-Fixup.sh
# docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost   -e APILOGICSERVER_GIT='https://github.com/valhuber/Tutorial-ApiLogicProject.git' -e APILOGICSERVER_FIXUP='/localhost/Project-Fixup.sh' apilogicserver/api_logic_server

git clone $1 ApiLogicProject

echo " "
pwd;  ls
echo " "


cd ApiLogicProject
pwd; ls
echo " "

if [ -z "$2" ]; then
    echo " "
else
    if test -e $2; then
        echo “Starting project-fixup script: $2”
        sh $2
    else
        echo "ERROR: project-fixup script does not exist"
        exit 1
    fi
fi

echo " "
python api_logic_server_run.py
