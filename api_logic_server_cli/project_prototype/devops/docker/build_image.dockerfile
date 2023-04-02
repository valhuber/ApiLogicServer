# To build image for your ApiLogicProject, see build_image.sh

# consider adding your version here
FROM apilogicserver/api_logic_server  

USER root

# user api_logic_server comes from apilogicserver/api_logic_server
WORKDIR /home/api_logic_project
USER api_logic_server
COPY ../../ .

CMD [ "python", "./api_logic_server_run.py" ]