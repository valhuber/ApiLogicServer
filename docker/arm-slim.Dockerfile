# docker build -f docker/arm-slim.Dockerfile -t apilogicserver/arm-slim --rm .
# docker tag apilogicserver/arm-slim apilogicserver/arm-slim:8.04.28
# docker push apilogicserver/arm-slim:8.04.28

# cd ~/dev/servers/install/ApiLogicServer/dockers
# docker run -it --name api_logic_server-arm-slim --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/arm-slim
# works, fast, 869MB

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