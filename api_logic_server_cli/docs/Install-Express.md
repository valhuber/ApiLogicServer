In most cases, Python and Python Projects are simple and fast to install, as described below.  If you encounter issues, open the [Detailed Install](../Install).

Follow these instructions to:

1. Install API Logic Server
2. Create the sample Tutorial API Logic Server Project
3. Open it in your IDE
4. Prepare the projects' Python environment


## Create an install directory

You can create this anywhere, such as your home folder or Desktop.

```bash title="Create an install directory"
mkdir ApiLogicServer      # a directory of projects on your local machine
```

## Use Local Install, or Docker

You can install API Logic Server locally using `pip`, or use Docker.  If you already have docker, it can eliminate many of the sometimes-tricky Python install issues.

Open the appropriate section below.

=== "Local Install"

    __Verify Pre-reqs: Python 3.8+__

    Ensure you have these pre-reqs:

    ```bash title="Verify 3.8 - 3.10"
    python --version  # on macs, you may need to use Python3
    ```

    If you need to install Python (it can be tricky), see [these notes](../Tech-Install-Python).
    &nbsp;

    __Install API Logic Server in a Virtual Environment__

    Then, install API Logic Server in the usual manner:

    ```bash title="Install API Logic Server in a Virtual Environment"
    python -m venv venv                  # may require python3 -m venv venv
    venv\Scripts\activate                # mac/linux: source venv/bin/activate
    python -m pip install ApiLogicServer
    ```

    If you are using SqlServer, you also need to [install `pyodbc`](../Install-pyodbc).

    __Create the Tutorial Project__

    ```bash title="Create Tutorial"
    ApiLogicServer create      # accept default project_name, db_url (sample tutorial)
    ```
    __Open the Project in VSCode__

    1. Open Folder `ApiLogicServer/ApiLogicProject` in VSCode
        * Decline options for Containers
    2. Establish your Virtual Environment - open __Terminal > New Terminal__, and

    ```bash title="Install API Logic Server in a Virtual Environment"
    python -m venv venv                  # may require python3 -m venv venv
    venv\Scripts\activate                # mac/linux: source venv/bin/activate
    python -m pip install -r requirements.txt  # accept "new Virtual environment"
    ```


=== "Docker"

    __Start Docker__
    ```bash title="Start (might install) API Logic Server Docker"
      docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server
    ```

    > Windows: use __Powershell__ (`PWD` is not supported in Command Line)

    __Create the Tutorial Project__

    You are now running a terminal window in the Docker machine.  Create the Tutorial project:
      ```bash title="Create Tutorial"
      $ ApiLogicServer create --project_name=/localhost/ApiLogicProject --db_url=
      $ exit  # return to local host 
      ```
    __Open the Project in VSCode__

    1. Open Folder `ApiLogicServer/ApiLogicProject` in VSCode
        * Accept option to "Reopen in Container"

            > If you already skipped this option, no worries.  Use __View > Command Palette > Remote-Containers: Reopen in Container__


&nbsp;

---


## Next Steps - Tutorial

You're all set - the Tutorial is created, installed and ready to run:

1. Start the Server using the pre-built Launch Configuration [as shown here](../IDE-Execute/#execute-prebuilt-launch-configurations)
2. Open the Admin App in your Browser
3. Proceed to [Explore the Tutorial](../Tutorial).
