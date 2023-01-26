# VSCode uses this file to create a development container, for you to customize and test API Logic Projects.
#
# Per .devcontainer/devcontainer.json, VSCode will offer to open your API Logic Server Project in this docker container
#    Same as: View > Command > Remote-Containers: Open Folder in Container.
#
# https://valhuber.github.io/ApiLogicServer/Working-With-Docker/
#
FROM apilogicserver/api_logic_server_x
USER api_logic_server
CMD ["bash"]