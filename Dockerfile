# docker build -t apilogicserver/api_logic_server --rm .
# docker tag apilogicserver/api_logic_server apilogicserver/api_logic_server:version3.01.00
# docker push apilogicserver/api_logic_server

# docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 --net dev-network -v ~/dev/servers:/local/servers apilogicserver/api_logic_server
#   docker run -it --name api_logic_server --rm -p 5000:5000 -p 8080:8080 --net dev-network -v ${PWD}:/local/servers apilogicserver/api_logic_server
#   docker image inspect apilogicserver/api_logic_server

# The software auto-prompts you for the next steps:
#   ApiLogicServer run --project_name=/local/servers/docker_project
#   ApiLogicServer run --project_name=/local/servers/docker_project --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels
#   python /local/servers/docker_project/api_logic_server_run.py
#   python /local/servers/docker_project/ui/basic_web_app/run.py

# shout out to Piotr Maślewski https://medium.com/swlh/dockerize-your-python-command-line-program-6a273f5c5544

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