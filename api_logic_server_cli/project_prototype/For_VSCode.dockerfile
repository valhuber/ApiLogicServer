# VSCode uses this file to create a development container, for you to customize and test API Logic Projects.
#
# Per .devcontainer/devcontainer.json, VSCode will offer to open your API Logic Server Project in this docker container
#    Same as: View > Command > Remote-Containers: Open Folder in Container.
#
# https://github.com/valhuber/ApiLogicServer/wiki/Testing#working-with-docker
#
FROM apilogicserver/api_logic_server
USER api_logic_server
CMD ["bash"]
