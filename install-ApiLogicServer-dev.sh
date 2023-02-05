#!/bin/bash

contains()
  # echo contains check $1 in $2
  case "$1" in
    (*"$2"*) true;;
    (*) false;;
  esac

ostype=$(uname -a)
if contains "Ubuntu" $ostype; then
  ostype="ubuntu"
fi
# if contains "ubuntu" $ostype; then
#   echo $ostype contains ubuntu
# fi

if [ $# -eq 0 ]
  then
    echo " "
    # echo "shell: $SHELL"
    echo "Installs dev version of ApiLogicServer and safrs-react-admin on $ostype (version 7.0.15)"
    echo "   .. vscode option creates venv, and starts vscode on workspace"
    echo " "
    echo " IMPORTANT - run this from empty folder"
    echo "   .. will create the ApiLogicServer directory for you"
    echo " "
    echo "  sh Install-ApiLogicServer-Dev [ vscode | charm | x ]"
    echo " "
    exit 0
  else
    ls
    echo " "
    read -p "Verify directory is empty, and [Enter] install *dev* version of ApiLogicServer for $1> "
    set -x
    mkdir servers    # good place to create ApiLogicProjects
    mkdir Org-ApiLogicServer  # app-fiddle is built here

    # get sra runtime as build folder
    curl https://github.com/thomaxxl/safrs-react-admin/releases/download/0.1.2/safrs-react-admin-0.1.2.zip -LO
    echo "unzipping sra to build.."
    set +x
    unzip safrs-react-admin-0.1.2.zip
    set -x
    
    git clone https://github.com/valhuber/ApiLogicServer
    git clone https://github.com/thomaxxl/safrs-react-admin
    # git clone https://github.com/valhuber/Docs-ApiLogicServer
    cd Org-ApiLogicServer
    git clone https://github.com/ApiLogicServer/Docs

    cd Docs
    python3 -m venv venv       # may require python -m venv venv
    if contains "ubuntu" $ostype; then
      echo $ostype contains ubuntu
      . venv/bin/activate
    else
      echo $ostype does not contain ubuntu
      source venv/bin/activate   # windows venv\Scripts\activate
    fi
    
    cd ..
    cd ..

    cd ApiLogicServer
    pwd
    echo "\ncopying build (sra - safrs-react-admin) --> ApiLogicServer"
    cp -r ../build api_logic_server_cli/create_from_model/safrs-react-admin-npm-build
    #
    #
    # read -p "Installed - ready to launch IDE..."
    if [ "$1" = "vscode" ]
      then
        python3 -m venv venv       # may require python -m venv venv
        # pwd
        # ls
        . venv/bin/activate
        # read -p "venv created; do optional pre-installs now $1> "
        python3 -m pip install -r requirements.txt    # you may need to use pip3, or restart your terminal session
        code .vscode/ApiLogicServerDev.code-workspace
        set +x
        echo ""
        echo "Workspace opened; use pre-created Launch Configurations:"
        echo "  * Run 1 - Create ApiLogicProject, then..."
        echo "  * Run 2 - RUN ApiLogicProject"
    elif [ "$1" = "charm" ]
    then
        charm .
        set +x
        echo "  * Python Interpreter > Add New Environment (default, to create venv)"
        echo "     IMPORTANT - NOT DOCKER"
        echo "  * then open requirements.txt - PyCharm should **Install Requirements**"
        echo "     If this fails, use a terminal to run pip install -r requirements.txt"
    else
      set +x
    fi
    echo ""
    echo "IDEs are preconfigured with run/launch commands to create and run the sample"
    echo ""
    echo "ApiLogicServer/react-admin contains shell burn-and-rebuild-react-admin"
    echo ""
    exit 0
fi
