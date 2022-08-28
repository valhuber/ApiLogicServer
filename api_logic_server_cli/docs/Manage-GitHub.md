API Logic Projects are standard, and so are their GitHb / IDE operations.  A typical flow is illustrated below.

&nbsp;

## Create an API Logic Server Project

```bash title="Create Project (here using Docker)"
val@Vals-MBP-16 dockers % cd ~/dev/servers/install/ApiLogicServer/dockers; docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server


Welcome to API Logic Server, 5.03.27

     $ printenv       for OS context       information -- Debian GNU/Linux 11 \n \l
     $ ApiLogicServer for API Logic Server information
 
api_logic_server@bc1bc88dc6ce:~$ ApiLogicServer create

Welcome to API Logic Server, 5.03.27

Project to create [/localhost/ApiLogicProject]: 
SQLAlchemy Database URI [default = nw.sqlite, ? for help]: 
... logging
api_logic_server@bc1bc88dc6ce:~$ exit  # exit, to facilitate use of Desktop tools (git cli, IDE, etc)
```

## Save API Logic Project to GitHub

Create a project on your GitHub account (here called `ApiLogicProject`) in the usual manner.

1. Create your project on GitHub

        *  Don't add files yet to avoid merge
2. Exit the Docker container as shown above
3. Initialize your project for git and push it in the usual manner:

``` bash title="Save Created API Logic Server Project to GitHub"
git init
# git branch -m main
git add --all
git commit -m 'First commit'
git remote add origin https://github.com/valhuber/ApiLogicProject.git
git remote -v
git push origin main
```

## Customize the Project

Use your IDE (or Code Editor) to customize the project.  Standard GitHub operations are provided in most IDEs, and work with API Logic Server Projects.

### Using your IDE

This is described under the [Express Install](../Install-Express).

### Using Codespaces

[CodeSpaces](https://github.com/features/codespaces){:target="_blank" rel="noopener"} is a GitHub project that enables you to use VSCode in your Browser to develop on rapidly deployed docker containers.  It's quite remarkable.  It is entirely interoperable with VSCode operations on your local machine.

Here are some instructions you can use to explore API Logic Server running under CodeSpaces.

__1. No signup required__ - use your GitHub account

__2. Load the ApiLogicProject from GitHub__

To access this GitHub project with Codespaces

1. [__Open this page _in a new window___](https://github.com/ApiLogicServer/ApiLogicServer-Explore), and 
2. Click __Open > Codespaces__ as shown below:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-on-codespaces.jpg
?raw=true"></figure> 


> You will now see the sample project - running in VSCode, _in the Browser._  But that's just what you _see..._

> Behind the scenes, Codespaces has requisitioned a cloud machine, and loaded your project - with a _complete development environment_ - Python, your dependencies, git, etc.  

> You are attached to this machine in your Browser, running VSCode.

> :trophy: Pretty remarkable.

__3. Add and Configure a Port__

* Referring to the diagram below, make the port __public__

__4. Start the Server__

* Use the pre-defined Launch Configuration

__5. Start the Browser__

* Click the globe, as shown above.  This should start your Browser, and the links on the left (Customer etc) should return data.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port-launch-simple.jpg?raw=true"></figure>

<details markdown>
<summary>If errors, use this procedure</summary>

The above procedure is simplified, based on some assumptions about Codespaces.  If the Browser fails to launch, try the following for explicit specification of the forwarded port:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port-launch.png?raw=true"></figure>

__4. Configure the pre-created `Codespaces-ApiLogicServer` launch configuration__ (see above)

__5. Start the Server__ using the provided Launch Configuration = `Codespaces-ApiLogicServer`

__6. Open the Browser__

Click the globe, as shown above.  This should start your Browser, and the links on the left (Customer etc) should return data.

</details>