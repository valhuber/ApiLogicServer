# docker build -t apilogicserver/api_logic_server --rm .
# docker tag apilogicserver/api_logic_server apilogicserver/api_logic_server
# docker push apilogicserver/api_logic_server
#
# https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker
# docker run -it --name api_logic_server --rm -p 5000:5000 -v ~/dev/servers:/mnt/servers apilogicserver/api_logic_server
# sh ApiLogicServer.sh create --host=172.17.0.2 --project_name=docker_project  # create project on docker container
# cp docker_project /mnt/servers/. -r  # copy it to local machine
# python /mnt/servers/docker_project/api_logic_server_run.py 0.0.0.0

FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash api_logic_server
WORKDIR /home/api_logic_server
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER api_logic_server
COPY . .
# EXPOSE 5000:5000
# EXPOSE 8080
USER root
RUN chmod +x ApiLogicServer.sh
CMD ["ApiLogicServer.sh"]
USER api_logic_server
CMD ["bash"]