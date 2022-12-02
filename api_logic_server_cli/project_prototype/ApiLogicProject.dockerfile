# To build container for your ApiLogicProject:
#    create / customize your project as your normally would
#    edit this file: change your_account/your_repository as appropriate
#    in terminal (not in VSCode docker - docker is not installed there), cd to your project
#    build a container for your project with terminal commands:
# docker build -f ApiLogicProject.dockerfile -t your_account/your_repository --rm .
# docker tag your_account/your_repository your_account/your_repository:1.00.00
# docker push your_account/your_repository:1.00.00  # requires docker login 

# see - https://valhuber.github.io/ApiLogicServer/Working-With-Docker/

# run image directly...
# docker run -it --name your_repository --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_account/your_repository

# start the image, but open terminal (e.g., for exploring docker image)
# docker run -it --name your_repository --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_account/your_repository bash

# consider adding your version here
FROM apilogicserver/api_logic_server  

USER root

WORKDIR /home/api_logic_project  # user api_logic_server comes from apilogicserver/api_logic_server
USER api_logic_server
COPY . .

CMD [ "python", "./api_logic_server_run.py" ]