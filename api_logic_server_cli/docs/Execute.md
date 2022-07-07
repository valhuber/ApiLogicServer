You can execute API Logic Projects from a Terminal Window, or from an IDE.  IDE instructions depend on whether you are using a local install, or Docker.

Select your desired configuration below, and see how to run, customize and debug your ApiLogicProject.

  > Note: as of release 5.02.10, projects are created with a `venv_setup` directory which may be helpful in establishing and verifying your Python environment.  For more information, see the [Trouble Shooting Guide](../Troubleshooting#ide-issues).

&nbsp;

---

=== "Command Line"

      While you will probably want to run it from your IDE (see next section), you can also run from the command line as described below.

      __1. Start the Server__
      The `api_logic_server_run.py` file is executable.  The simplest way to run it is:

      ``` title="Either from Docker terminal, or from local terminal with `venv` set"
      ApiLogicServer run
      ```

      You can also run it directly:

      ``` bash title="Either from Docker terminal, or from local terminal with `venv` set"
      python api_logic_server_run.py       # options exist to override URL, port
      ```


      __2. Open in your Browser__
      The server should start, and suggest the URL for your Browser.  That will open a page like this where you can explore your data using the automatically created [Admin app](../Working-with-the-Admin-App), and explore the API with automatically generated Swagger:

      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/admin-home.png?raw=true"></figure>

=== "VS Code Local -- Local Install"

      __1. Create your project__

      ```
      cd ApiLogicServer          # your install folder
      source venv/bin/activate   # windows venv\Scripts\activate

      ApiLogicServer create   # Return to accept default project name, db

      ```

      __2. Open your project with VS Code__

      You can open the IDE yourself, or from the command line:

      ```
      cd ApiLogicServer

      # start VS Code either as an application, or via the command line
      #    .. macOS users may require: https://code.visualstudio.com/docs/setup/mac

      code ApiLogicProject  # using command line to open VS Code on project
      ```


      __3. Remote Container - Decline__
      Decline the option above to use the remote-container.   You can prevent this by deleting the `.devcontainer` folder.


      __4. Create Virtual Environment__
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

      __5. Install Python Extension__

      You may be prompted for this (recent versions of VSCode might auto-detect language support):

      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/4-install-python-extension.png"></figure>


      __6. Run the server__
      You are ready to run
      1. Run/Debug: `ApiLogicServer`

      > You may get a message: _"The Python path in your debug configuration is invalid."_  Open View > Command Pallet, type “Python Select Interpreter” and Select your `venv`.

      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/run-debug.png"></figure>

=== "VS Code -- Docker Install"

      Integrated Development Environments (IDEs) provide code editing and debugging, as well as many other services.  

      The created Docker project is a standard Python project, [fully customizable](https://github.com/valhuber/ApiLogicServer#customize-the-created-project) with your existing IDE and other development tools.

      > Significantly, you can utilize the Python environment from the Docker machine, __eliminating the need to install and configure Python__.   These procedures apply to local and Docker-based Python.

      Pre-reqs:

      * Docker (if elected)
      * VS Code 1.61
      * [VS Code Shell Command](https://code.visualstudio.com/docs/setup/mac)

      The steps below explain how to load, run, verify and debug your projects.
      The _load_ step differs depending on whether you are using Docker.

      **To Execute under Docker**

      __1. Load your docker project__

      Create and load your project like this:

      ```bash
      cd ~/Desktop                # directory of API Logic Server projects on local host

      # [Install and] Start the API Logic Server docker container
      docker run -it --name api_logic_server --rm -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server

      # (Now inside the container)
      ApiLogicServer create   # Return to accept default project name, db

      exit  # exit container to localhost
      ```

        > Observe you __exit the Docker container___.  We'll start VSCOde _locally_ below, where it will restart Docker as a Remote Container below.  _Local_ operation means your project files are accessed locally (not via `/localhost`), which enables local file operations such as git.

      ```bash
      # start VS Code either as an application, or via the command line
      # macOS users may require: https://code.visualstudio.com/docs/setup/mac
      code ApiLogicProject  # loads VS Code; accept container suggestions, and press F5 to run (described below)
      ```


      __2. Remote Container - Accept__

      Created projects are configured to support:

      * launch configurations for running `ApiLogicServer` and the `Basic Web App`
      * Docker-based Python environments, per `.devcontainer`

      So, when you open the created project, VS Code recognizes that Docker configuration, and provides an option to **Reopen** the project in a [remote container](https://code.visualstudio.com/docs/remote/containers).  Accept this option.


      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/open-in-container.png"></figure>

      __3. Run ApiLogicServer__

      Click __Run and debug > Run ApiLogicServer__.

      This will start the server, and offer to run the Browser on the Admin app.  For more information, [see here](https://github.com/valhuber/ApiLogicServer/blob/main/README.md#run).

      __4. Install Python Extension__

      When you run, you may encounter the message below; if so:

      1. Click Extensions (as shown)
      2. Ensure Python support is installed and enabled

      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/docker/VSCode/docker-install-python-extension.png"></figure>


      ## ApiLogicServer Container upgrades

      If you update your ApiLogicServer container to a new version, your existing projects may appear to be damaged.  You can fix them easily:

      1. Click the Dev Container button (in the lower left)
      1. Choose **Rebuild Container**

=== "PyCharm"

      __1. Create your project__

      ```
      cd ApiLogicServer          # your install folder
      source venv/bin/activate   # windows venv\Scripts\activate

      ApiLogicServer create   # Return to accept default project name, db

      ```


      __2. Do *not* create the `venv` outside PyCharm__


      __3. Open the ApiLogic Project__

      __4. Create a new Virtual Environment using PyCharm defaults__

      PyCharm will ask you to configure a Python Interpreter.  Do so as shown below.

      <figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/PyCharm/PyCharm-create-venv.png"></figure>


      __5. `pip` install__

      Some versions of Pycharm automatically load your dependencies, others do not.  But it's simple to load them using the terminal window:

      ```bash
      source venv/bin/activate          # windows: venv\Scripts\activate
      pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
      ```

      > The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.



      __6. Run the pre-configured `run` launch configuration__

      Some versions of Pycharm may require that you update the Launch Configuration(s) to use your `venv`.
