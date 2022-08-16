# docker build -f docker/Dockerfile-main-arm.Dockerfile -t apilogicserver/api_logic_server-arm --rm .
# docker tag apilogicserver/api_logic_server apilogicserver/api_logic_server-arm:5.03.32
# docker push apilogicserver/api_logic_server-arm:5.03.32

# shout outs...
#   Thmomas Pollet  https://github.com/thomaxxl/safrs-react-admin -- safrs, safrs-react-admin
#   Max Tardiveau   https://www.galliumdata.com/
#   Shantanu        https://forum.astronomer.io/t/how-to-pip-install-pyodbc-in-the-dockerfile/983
#   Piotr Maślewski https://medium.com/swlh/dockerize-your-python-command-line-program-6a273f5c5544

# python:3.9-slim-bullseye (Debian Linux 11) is 638MB, with SqlServer (here) is 1.04G

# if builds fails, check for renamed targets by breaking up Run commands

FROM python:3.10.4-slim-bullseye

USER root
RUN apt-get update \
  && apt-get install -y curl \
  && apt-get install -y git \
  && apt-get -y install gcc gnupg2 \
  && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt install -y \
		libltdl7 libodbc1 odbcinst odbcinst1debian2 unixodbc wget \
  && wget http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/multiarch-support_2.27-3ubuntu1.5_amd64.deb \
  && apt-get install ./multiarch-support_2.27-3ubuntu1.5_amd64.deb \
  && wget https://packages.microsoft.com/debian/10/prod/pool/main/m/msodbcsql17/msodbcsql17_17.8.1.1-1_amd64.deb \
  && ACCEPT_EULA=Y dpkg -i msodbcsql17_17.8.1.1-1_amd64.deb;

# TODO RUN wget https://packages.microsoft.com/debian/10/prod/pool/main/m/mssql-tools/mssql-tools_17.8.1.1-1_amd64.deb;

RUN apt-get -y install unixodbc-dev \
  && apt-get -y install python3-pip \
  && pip install pyodbc

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