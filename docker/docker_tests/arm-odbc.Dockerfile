# docker build -f docker/arm-odbc.Dockerfile -t apilogicserver/arm-odbc --rm .
# docker tag arm-fideops apilogicserver/arm-odbc:5.03.32
# docker push apilogicserver/arm-fideops:5.03.32

# shout outs... fidesops
#   https://github.com/ethyca/fidesops/blob/main/Dockerfile

# cd ~/dev/servers/install/ApiLogicServer/dockers; 
# docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/arm-odbc
# works, slow

# python:3.9-slim-bullseye (Debian Linux 11) is 638MB, with SqlServer (here) is 1.13G

# if builds fails, check for renamed targets by breaking up Run commands

FROM --platform=linux/amd64 python:3.9.13-slim-bullseye as backend

# Install auxiliary software
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    make \
    vim \
    curl \
    g++ \
    gnupg \
    gcc \
    python3-wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ARG SKIP_MSSQL_INSTALLATION
RUN echo "ENVIRONMENT VAR:  SKIP_MSSQL_INSTALLATION $SKIP_MSSQL_INSTALLATION"

# SQL Server (MS SQL)
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN if [ "$SKIP_MSSQL_INSTALLATION" != "true" ] ; then apt-get install -y --no-install-recommends apt-transport-https && apt-get clean && rm -rf /var/lib/apt/lists/* ; fi
RUN if [ "$SKIP_MSSQL_INSTALLATION" != "true" ] ; then curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - ; fi
RUN if [ "$SKIP_MSSQL_INSTALLATION" != "true" ] ; then curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/msprod.list ; fi
RUN if [ "$SKIP_MSSQL_INSTALLATION" != "true" ] ; then apt-get update ; fi
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN if [ "$SKIP_MSSQL_INSTALLATION" != "true" ] ; then apt-get -y --no-install-recommends install \
    unixodbc-dev \
    msodbcsql17 \
    mssql-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* ; fi





###############################
## API Logic Server Setup    ##
###############################

#RUN apt-get -y install unixodbc-dev \
#  && apt-get -y install python3-pip \
#  && pip install pyodbc

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