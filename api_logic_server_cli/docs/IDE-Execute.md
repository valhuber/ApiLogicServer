API Logic Projects are simply directories, without restrictions on their location.  You can open them directly in your IDE. (You can also execute them from a [Terminal Window](../Execute)). 

This page describes how to open your project, establish your Python environment, and execute your project.

## Open Project and Establish Python Environment

IDE instructions depend on whether you are using a local install, or Docker.  Select your desired configuration below, and see how to run, customize and debug your ApiLogicProject.

=== "VS Code Local -- Local Install"

Follow these instructions:

    __1. Open your project with VS Code__

    You can open the IDE yourself, or from the command line:

    ```
    cd ApiLogicServer

    # start VS Code either as an application, or via the command line
    #    .. macOS users may require: https://code.visualstudio.com/docs/setup/mac

    code ApiLogicProject  # using command line to open VS Code on project
    ```


    __2. Remote Container - Decline__

    Decline the option above to use the remote-container.   You can prevent this by deleting the `.devcontainer` folder.


    __3. Create Virtual Environment__

    You then create your virtual environment, activate it, and install the  ApiLogicServer runtime.  

    In VS Code: __Terminal > New Terminal Window__, and...

    ```
    python3 -m venv ./venv                       # windows: python -m venv venv
    # VS Code will recognize your `venv` and ask whether to establish it as your virtual environment.  Say yes.  
    source venv/bin/activate                     # windows: venv\Scripts\activate
    python3 -m pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
    ```

    > The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.

    For more information, see [Work with Environments](https://code.visualstudio.com/docs/python/environments#_work-with-environments), and [Project Environment](../Project-Env/).

    __4. Install Python Extension__

    You may be prompted for this (recent versions of VSCode might auto-detect language support):

    <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/4-install-python-extension.png"></figure>


=== "VS Code -- Docker Install"

    __1. Load your docker project__

    You've aleady created your project like this:

    ```bash
    cd ~/Desktop                # directory of API Logic Server projects on local host

    # [Install and] Start the API Logic Server docker container
    docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

    # (Now inside the container)
    ApiLogicServer create   # Return to accept default project name, db

    exit  # exit container to localhost
    ```

    !!! Container-exit
    
        Observe you __exit the Docker container__.  We'll start VSCode _locally_ below, where it will restart Docker as a Remote Container below.  _Local_ operation means your project files are accessed locally (not via `/localhost`), which enables local file operations such as git.

    &nbsp;

    The project creation above has created a project on your local computer.  You can open it in VSCode like this:

    ```bash title="Open VSCode on created API Logic Project"
    # start VS Code either as an application, or via the command line
    # macOS users may require: https://code.visualstudio.com/docs/setup/mac
    code ApiLogicProject  # loads VS Code; accept container suggestions, and press F5 to run (described below)
    ```

    __2. Remote Container - Accept__

    Created projects are pre-configured to support:

    * launch configurations for running `ApiLogicServer` and tests
    * Docker-based Python environments, per `.devcontainer`

    So, when you open the created project, VS Code recognizes that Docker configuration, and provides an option to **Reopen** the project in a [remote container](https://code.visualstudio.com/docs/remote/containers).  Accept this option.

    > If you already skipped this option, no worries.  Use __View > Command Palette > Remote-Containers: Reopen in Container__


    <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/open-in-container.png"></figure>

    __Note:__ when you Execute your application (below), you may need to update your Docker container - see [Working with Docker](../Working-With-Docker).

=== "PyCharm"

    __1. Do *not* create the `venv` outside PyCharm__

    __2. Open the ApiLogic Project__

    __3. Create a new Virtual Environment using PyCharm defaults__

    PyCharm will ask you to configure a Python Interpreter.  Do so as shown below.

    <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/PyCharm/PyCharm-create-venv.png"></figure>

    __4. `pip` install__

    Some versions of Pycharm automatically load your dependencies, others do not.  But it's simple to load them using the terminal window:

    ```bash
    source venv/bin/activate                    # windows: venv\Scripts\activate
    python -m pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
    ```
    > The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.

    __5. Run the pre-configured `run` launch configuration__

    Some versions of Pycharm may require that you update the Launch Configuration(s) to use your `venv`.

&nbsp;

---

## Execute - prebuilt Launch Configurations

Once you have established your Python environment, you are ready to run.  The `ApiLogicServer create` command has built launch configurations, so you can start your server like this:

### 1. Click **Run and Debug**
<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/run-debug.png"></figure>

### 2. Select Launch Configuation

Select the pre-built `ApiLogicServer` Launch Configuration (it should be the default).

* Use `Codespaces` if you are running in that environment)

### 3. Click Green Run Button

Press the green run button to start the server.

When you run, you may encounter the message below; if so:

1. Click Extensions (as shown)
2. Ensure Python support is installed and enabled

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/docker-install-python-extension.png"></figure>


### 4. Start the Browser

* If you are running Docker / VS Code, VS Code will suggest opening a Browser, or previewing it in the Editor (i.e., in VSCode).
* Otherwise open a browser at [http://localhost:5656](http://localhost:5656){:target="_blank" rel="noopener"}

### 5. Proceed to the Tutorial

The [Tutorial](../Tutorial) will walk you through the sample project.

&nbsp;

---

Notes:

* Be aware that we have seen some issue where the _simple browser_ fails to start; just use your normal browser  
* We have also seen that some systems are slow to load caches on first execution; browser refresh can often be helpful
* You may get a message: _"The Python path in your debug configuration is invalid."_  Open View > Command Pallet, type “Python Select Interpreter” and Select your `venv`.

&nbsp;

## Other Launch Configurations

The `ApiLogicServer create` command also creates launch configurations for executing tests, and running the [Behave Logic Report](../Behave-Logic-Report). 
