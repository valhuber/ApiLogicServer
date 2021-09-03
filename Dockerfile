# docker build -t apilogicserver/api_logic_server --rm .
# docker tag apilogicserver/api_logic_server apilogicserver/api_logic_server
# docker push apilogicserver/api_logic_server
#
# https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker
#
# docker run -it --name api_logic_server --rm -p 5000:5000 -v ~/dev/servers:/local/servers apilogicserver/api_logic_server
# The software auto-prompts you for the next steps:
#     sh ApiLogicServer.sh create --project_name=docker_project  # create project on docker container (for fab)
#     python /local/servers/docker_project/api_logic_server_run.py


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