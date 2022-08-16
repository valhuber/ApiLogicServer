# docker build -f docker/Dockerfile-main-arm-1-step-slim.Dockerfile -t apilogicserver/api_logic_server-arm-slim --rm .
# docker tag apilogicserver/api_logic_server-arm-slim apilogicserver/api_logic_server-arm-slim:5.03.35
# docker push apilogicserver/api_logic_server-arm-slim:5.03.35

# shout outs...
#   Thmomas Pollet  https://github.com/thomaxxl/safrs-react-admin -- safrs, safrs-react-admin
#   Max Tardiveau   https://www.galliumdata.com/
#   Shantanu        https://forum.astronomer.io/t/how-to-pip-install-pyodbc-in-the-dockerfile/983
#   Piotr Maślewski https://medium.com/swlh/dockerize-your-python-command-line-program-6a273f5c5544

# python:3.9-slim-bullseye (Debian Linux 11) is 846MB, with SqlServer (here) is 1.16G

# docker run -it --name api_logic_server-arm-slim --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server-arm-slim
# docker run -it --name api_logic_server-arm-slim --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server-arm-slim:5.03.35
# docker run -it --name api_logic_server-arm-slim --user root --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server-arm-slim:5.03.35

# if builds fails, check for renamed targets by breaking up Run commands

FROM python:3.10.4-slim-bullseye

USER root
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

RUN useradd --create-home --shell /bin/bash api_logic_server
WORKDIR /home/api_logic_server
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
USER api_logic_server
COPY . .
# EXPOSE 5000:5000
# EXPOSE 8080
USER root
RUN chmod +x bin/ApiLogicServer \
    && chmod a+rwx -R api_logic_server_cli/api_logic_server_info.yaml \
    && chmod +x bin/py
# CMD ["ApiLogicServer"]
USER api_logic_server

ENV APILOGICSERVER_RUNNING=DOCKER

# RUN chmod a+rwx -R api_logic_server_cli/api_logic_server_info.yaml
CMD ["bash"]