
param(
    [Parameter()]
    [String]$IDE
)

Write-Output "IDE specified as: $IDE"

if($IDE -eq "") {
    echo " "
    echo "Installs dev version of ApiLogicServer and safrs-react-admin (version 4.01.08)"
    echo " "
    echo " IMPORTANT - run this from empty folder"
    echo " "
    echo "  ./Install-ApiLogicServer-Dev.ps1 [ vscode | charm | x ]"
    echo " "
    Exit
}
ls
echo " "
$Ready= Read-Host -Prompt "Verify directory is empty, and [Enter] install dev version of ApiLogicServer for IDE $IDE"
Set-PSDebug -Trace 0
mkdir servers    # good place to create ApiLogicProjects
git clone https://github.com/valhuber/ApiLogicServer ApiLogicServer
git clone https://github.com/thomaxxl/safrs-react-admin safrs-react-admin
git clone https://github.com/valhuber/Docs-ApiLogicServer Docs-ApiLogicServer

pushd Docs-ApiLogicServer
python -m venv venv
python -m pip install -r requirements.txt
popd

cd ApiLogicServer
cp -r ../safrs-react-admin/build api_logic_server_cli/create_from_model/safrs-react-admin-npm-build

if ($IDE -eq "vscode") {
    python -m venv venv
    # pwd
    # ls
    venv\Scripts\activate
    python -m pip install -r requirements.txt
    code .vscode/workspace.code-workspace
    Set-PSDebug -Trace 0
    echo ""
    echo "Workspace opened; use pre-created Launch Configurations:"
    echo "  * Run 1 - Create ApiLogicProject, then..."
    echo "  * Run 2 - RUN ApiLogicProject"
} elseif ($IDE -eq "pycharm") {
    charm .
    Set-PSDebug -Trace 0
    echo "  * Python Interpreter > Add New Environment (default, to create venv)"
    echo "     IMPORTANT - NOT DOCKER"
    echo "  * then open requirements.txt - PyCharm should **Install Requirements**"
    echo "     If this fails, use a terminal to run pip install -r requirements.txt"
} else {
    echo "No IDE started"
}
echo ""
echo "IDEs are preconfigured with run/launch commands to create and run the sample"
echo ""
echo "ApiLogicServer/react-admin contains shell burn-and-rebuild-react-admin"
echo ""
exit 0
