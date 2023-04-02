#!/bin/bash

# To build container for your ApiLogicProject:
#    create / customize your project as your normally would
#    edit this file: change your_account/your_repository as appropriate
#    in terminal (not in VSCode docker - docker is not installed there), cd to your project
#    build a container for your project: `sh build_container.sh`

projectname="apilogicserver_project_name_lower"  # lower case, only
repositoryname="apilogicserver"
version="1.0.0"

debug() {
  debug="disabled"
  # echo "$1"
}

debug "\n"
debug "build_image here 1.0"
if [ $# -eq 0 ]; then
  echo "\nBuilds docker image for API Logic Project\n"
  echo "  cd devops/docker"
  echo "  sh build_container.sh [ . | <docker-id> ]"
  echo "    . means use defaults:"
  echo "        ${repositoryname}/${projectname}:${version}"
  echo "    <docker-id> means use explicit args: <repository-name> <project-name> <version> eg,"
  echo "        sh build_image.sh myrepository myproject 1.0.1"
  echo " "
  exit 0
fi

echo " "
if [ "$1" = "." ]; then
  debug "..using defaults"
else
  debug "using arg overrides"
  repositoryname="$1"
  projectname="$2"
  version="$3"
fi

docker build -f build_image.dockerfile -t ${repositoryname}/${projectname} --rm .

status=$?
if [ $status -eq 0 ]; then
  echo "\nImage built successfully.. test (omit bash to run directly):\n"
  echo "  docker run -it --name ${projectname} --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost ${repositoryname}/${projectname}:${version} bash"
  echo "\nNext steps:"
  echo "  docker tag ${repositoryname}/${projectname} ${repositoryname}/${projectname}:${version}"
  echo "  docker push ${repositoryname}/${projectname}:${version}  # requires docker login"\"
  echo " "
  echo "  docker tag ${repositoryname}/${projectname} ${repositoryname}/${projectname}:latest"
  echo "  docker push ${repositoryname}/${projectname}:latest"
  echo " "
  echo "Image ready to deploy; e.g. on Azure: https://apilogicserver.github.io/Docs/DevOps-Containers-Deploy"
else
  echo "command unsuccessful\n"
  exit 1
fi
echo " "
exit 0
