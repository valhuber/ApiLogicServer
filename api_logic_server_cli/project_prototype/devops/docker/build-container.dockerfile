# To build container for your ApiLogicProject:
#    create / customize your project as your normally would
#    edit this file: change your_account/your_repository as appropriate
#    in terminal (not in VSCode docker - docker is not installed there), cd to your project
#    build a container for your project with terminal commands:
# docker build -f devops/docker/build-container.dockerfile -t your_account/your_repository --rm .
#       e.g., docker build -f devops/docker/build-container.dockerfile -t apilogicserver/docker_api_logic_project --rm . 
# docker tag your_account/your_repository your_account/your_repository:1.00.00
# docker push your_account/your_repository:1.00.00  # requires docker login 
# ... consider repeating the prior 2 commands for :latest

# see - https://valhuber.github.io/ApiLogicServer/Working-With-Docker/

# run image directly...
# docker run -it --name docker_api_logic_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_account/your_repository

# start the image, but open terminal (e.g., for exploring docker image)
# docker run -it --name your_repository --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_account/your_repository bash
#        e.g, docker run -it --name docker_api_logic_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/docker_api_logic_project:latest bash

# run on cloud-based docker, provide start arg (at end) e.g.
# docker run -it --name docker_api_logic_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/docker_api_logic_project python api_logic_server_run.py --flask_host=172.18.0.5

# consider adding your version here
FROM apilogicserver/api_logic_server  

USER root

# user api_logic_server comes from apilogicserver/api_logic_server
WORKDIR /home/api_logic_project
USER api_logic_server
COPY ../../ .

CMD [ "python", "./api_logic_server_run.py" ]