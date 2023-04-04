
param(
    [Parameter()]
    [String]$IDE
)

Write-Output "IDE specified as: $IDE"

if($IDE -eq "") {
    Write-Output " "
    Write-Output "Installs dev version of ApiLogicServer and safrs-react-admin (version 7.0.15)"
    Write-Output "   .. vscode option creates venv, and starts vscode on workspace "
    Write-Output " "
    Write-Output " IMPORTANT - run this from empty folder"
    Write-Output "   .. will create the ApiLogicServer directory for you "
    Write-Output " "
    Write-Output "  ./Install-ApiLogicServer-Dev.ps1 [ vscode | charm | x ]"
    Write-Output " "
    Exit
}
ls
Write-Output " "
$Ready= Read-Host -Prompt "Verify directory is empty, and [Enter] install dev version of ApiLogicServer for IDE $IDE"
Set-PSDebug -Trace 0

# get sra runtime as build folder
curl https://github.com/thomaxxl/safrs-react-admin/releases/download/0.1.2/safrs-react-admin-0.1.2.zip -LO
echo "unzipping sra to build.."

Expand-Archive -LiteralPath safrs-react-admin-0.1.2.zip -DestinationPath . | out-null


Set-PSDebug -Trace 1
mkdir servers    # good place to create ApiLogicProjects
mkdir Org-ApiLogicServer  # build app-fiddle here
git clone https://github.com/valhuber/ApiLogicServer ApiLogicServer
git clone https://github.com/thomaxxl/safrs-react-admin safrs-react-admin
# git clone https://github.com/valhuber/Docs-ApiLogicServer Docs-ApiLogicServer
cd Org-ApiLogicServer
git clone https://github.com/ApiLogicServer/Docs
cd ..

pushd Org-ApiLogicServer/docs
python -m venv venv
python -m pip install -r requirements.txt

popd

cd ApiLogicServer
cp -r ../build api_logic_server_cli/create_from_model/safrs-react-admin-npm-build

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
