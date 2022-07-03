While you will probably want to run it from your IDE (see next section), you can also run from the command line as described below.

__1. Start the Server__
The `api_logic_server_run.py` file is executable.  The simplest way to run it is:
```
ApiLogicServer run        # in Docker Terminal, or with venv active
```

__2. Open in your Browser__
The server should start, and suggest the URL for your Browser.  That will open a page like this where you can explore your data using the automatically created [Admin app](https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App), and explore the API with automatically generated Swagger:

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/ui-admin/admin-home.png?raw=true"></figure>
</details>

<details>
  <summary>VS Code - local install</summary>

&nbsp;&nbsp; 

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
python3 -m venv ./venv            # windows: python -m venv venv
# VS Code will recognize your `venv` and ask whether to establish it as your virtual environment.  Say yes.  
source venv/bin/activate          # windows: venv\Scripts\activate
pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
```

> The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.

For more information, see [Work with Environments](https://code.visualstudio.com/docs/python/environments#_work-with-environments)

__5. Install Python Extension__

You may be prompted for this (recent versions of VSCode might auto-detect language support):

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/docker/VSCode/4-install-python-extension.png"></figure>


__6. Run the server__
You are ready to run
1. Run/Debug: `ApiLogicServer`

> You may get a message: _"The Python path in your debug configuration is invalid."_  Open View > Command Pallet, type “Python Select Interpreter” and Select your `venv`.

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/docker/VSCode/run-debug.png"></figure>