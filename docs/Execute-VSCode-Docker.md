
Integrated Development Environments (IDEs) provide code editing and debugging, as well as many other services.  

The created Docker project is a standard Python project, [fully customizable](https://github.com/valhuber/ApiLogicServer#customize-the-created-project) with your existing IDE and other development tools.

> Significantly, you can utilize the Python environment from the Docker machine, __eliminating the need to install and configure Python__.   These procedures apply to local and Docker-based Python.

Pre-reqs:
* Docker (if elected)
* VS Code 1.61
* [VS Code Shell Command](https://code.visualstudio.com/docs/setup/mac)

The steps below explain how to load, run, verify and debug your projects.
The _load_ step differs depending on whether you are using Docker.

## Execute under VSCode / Docker

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