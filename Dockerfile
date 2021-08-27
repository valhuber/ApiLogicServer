# docker build -t api_logic_server --rm .
# docker tag api_logic_server apilogicserver/api_logic_server
# docker push apilogicserver/api_logic_server
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