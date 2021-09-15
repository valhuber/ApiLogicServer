# docker build -t apilogicserver/api_logic_server --rm .
# docker tag apilogicserver/api_logic_server apilogicserver/api_logic_server:version3.0.2
# docker push apilogicserver/api_logic_server
#
# https://github.com/valhuber/ApiLogicServer/wiki/Working-with-Docker
#
# docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 --net dev-network -v ~/dev/servers:/local/servers apilogicserver/api_logic_server
#   docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 --net dev-network -v ${PWD}:/local/servers apilogicserver/api_logic_server
#
# The software auto-prompts you for the next steps:
#   ApiLogicServer create --project_name=/local/servers/docker_project --db_url=mysql+pymysql://root:p@mysql8.0:3306/classicmodels
#   python /local/servers/docker_project/api_logic_server_run.py
#   python /local/servers/docker_project/ui/basic_web_app/run.py
#
# Needs research - run defaults to 0.0.0.0 in api_logic_server_run, overridden to localhost in api/expose_api_models
#     So, why doesn't this work on windows?
#         python /local/servers/docker_project/api_logic_server_run.py localhost
#         Is it this?  https://docs.docker.com/desktop/windows/networking/
#
# docker commit mysql-testdbs
# docker tag mysql:8.0 apilogicserver/mysql8.0:version1.0.2
# docker push apilogicserver/mysql8.0:version1.0.2


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
RUN chmod +x ApiLogicServer
CMD ["ApiLogicServer"]
USER api_logic_server
CMD ["bash"]