
param(
    [Parameter()]
    [String]$IDE
)

Write-Output "IDE specified as: $IDE"

if($IDE -eq "") {
    Write-Output " "
    Write-Output "Installs dev version of ApiLogicServer and safrs-react-admin (version 4.01.08)"
    Write-Output " "
    Write-Output " IMPORTANT - run this from empty folder"
    Write-Output " "
    Write-Output "  ./Install-ApiLogicServer-Dev.ps1 [ vscode | charm | x ]"
    Write-Output " "
    Exit
}
ls
Write-Output " "
$Ready= Read-Host -Prompt "Verify directory is empty, and [Enter] install dev version of ApiLogicServer for IDE $IDE"
Set-PSDebug -Trace 0
mkdir servers    # good place to create ApiLogicProjects
git clone https://github.com/valhuber/ApiLogicServer ApiLogicServer
git clone https://github.com/thomaxxl/safrs-react-admin safrs-react-admin
git clone https://github.com/valhuber/Docs-ApiLogicServer Docs-ApiLogicServer

pushd Docs-ApiLogicServer
Expand-Archive -LiteralPath safrs-react-admin-builds/safrs-react-admin-npm-build.zip -DestinationPath safrs-react-admin-builds/safrs-react-admin-npm-build


python -m venv venv
python -m pip install -r requirements.txt

popd

cd ApiLogicServer
cp -r ../Docs-ApiLogicServer/safrs-react-admin-builds/safrs-react-admin-npm-build/safrs-react-admin-npm-build api_logic_server_cli/create_from_model/safrs-react-admin-npm-build

if ($IDE -eq "vscode") {
    python -m venv venv
    # pwd
    # ls
    venv\Scripts\activate
    python -m pip install -r requirements.txt
    code .vscode/ApiLogicServerDev.code-workspace
    Set-PSDebug -Trace 0
    Write-Output ""
    Write-Output "Workspace opened; use pre-created Launch Configurations:"
    Write-Output "  * Run 1 - Create ApiLogicProject, then..."
    Write-Output "  * Run 2 - RUN ApiLogicProject"
} elseif ($IDE -eq "pycharm") {
    charm .
    Set-PSDebug -Trace 0
    Write-Output "  * Python Interpreter > Add New Environment (default, to create venv)"
    Write-Output "     IMPORTANT - NOT DOCKER"
    Write-Output "  * then open requirements.txt - PyCharm should **Install Requirements**"
    Write-Output "     If this fails, use a terminal to run pip install -r requirements.txt"
} else {
    Write-Output "No IDE started"
}
Write-Output ""
Write-Output "IDEs are preconfigured with run/launch commands to create and run the sample"
Write-Output ""
Write-Output "ApiLogicServer/react-admin contains shell burn-and-rebuild-react-admin"
Write-Output ""
exit 0
