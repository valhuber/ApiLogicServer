# To build container for your ApiLogicProject:
#    create / customize your project as your normally would
#    edit this file: change your_repo/your_project as appropriate
#    in terminal (not in VSCode docker - docker is not installed there), cd to your project
#    build a container for your project with terminal commands:
# docker build -f ApiLogicProject.dockerfile -t your_repo/your_project --rm .
# docker tag your_repo/your_project your_repo/your_project:1.00.00
# docker login; docker push your_repo/your_project:1.00.00

# see - https://valhuber.github.io/ApiLogicServer/Working-With-Docker/

# run project directly...
# docker run -it --name your_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_repo/your_project

# start the image, but open terminal (e.g., for exploring docker image)
# docker run -it --name your_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_repo/your_project bash

# consider adding your version here
FROM apilogicserver/api_logic_server  

USER root

WORKDIR /home/api_logic_project  # user api_logic_server comes from apilogicserver/api_logic_server
USER api_logic_server
COPY . .

CMD [ "python", "./api_logic_server_run.py" ]