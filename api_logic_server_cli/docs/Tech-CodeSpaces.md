[CodeSpaces](https://github.com/features/codespaces){:target="_blank" rel="noopener"} is a GitHub project that enables you to use VSCode in your Browser to develop on rapidly deployed docker containers.  It's quite remarkable.  

Api Logic Server has been explored under CodeSpaces, and is starting to run.  This is a __work in progress.__

Here is the [test project](https://github.com/valhuber/Tutorial-ApiLogicProject#readme){:target="_blank" rel="noopener"}.

&nbsp;

## Configuring the project

Here are some instructions you can use to explore API Logic Server running under CodeSpaces.

__1. Signup for CodeSpaces__ - use [this link](https://github.com/features/codespaces/signup){:target="_blank" rel="noopener"}, where you already have a GitHub account

__2. Get the Tutorial Project__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-tutorial-repo.png
?raw=true"></figure> 

__3. Configure a Port__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port.png?raw=true"></figure>

__4. Configure the `Codespaces-ApiLogicServer` launch configuration__ (see above)

__5. Start the Server__ using the provided Launch Configuration = `Codespaces-ApiLogicServer`

__6. Open the Browser__

Click the globe, below.  This should start your Browser, and the links on the left (Customer etc) should return data.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-port.png?raw=true"></figure>


&nbsp;

## Creating New Projects

The example above illustrated a way to explore Codespaces without any local install, by loading a project already on GitHub.  You can also create your own project - 2 ways are described below.

### Local Creation

As described in the (Getting Started Guide)[../Install-Express], you can create projects, store them in GitHub, and load them as described above.

### Create from Codespaces (currently not working)

We also explored creating a new project from the Codespaces example itself.  You can create projects under Codespaces just as you do for local installs:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-project-from-codespaces.png?raw=true"></figure>

Problems occur, however, when you try to [add existing project to git](https://gist.github.com/alexpchin/102854243cd066f8b88e):

```
git init
git add .
git commit -m 'First commit'
git remote add origin https://github.com/PoseyDev/MyProject.git
git remote -v
git remote set-url origin "https://PoseyDev@github.com/PoseyDev/MyProject.git"
git push origin master
      remote: Permission to PoseyDev/MyProject.git denied to PoseyDev.
      fatal: unable to access 'https://github.com/PoseyDev/MyProject.git/': The requested URL returned error: 403
```

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/push-403.png?raw=true"></figure>

Git config status:
```
git config --list
      credential.helper=/.codespaces/bin/gitcredential_github.sh
      user.name=PoseyDev
      user.email=54030760+PoseyDev@users.noreply.github.com
      gpg.program=/.codespaces/bin/gh-gpgsign
      core.repositoryformatversion=0
      core.filemode=true
      core.bare=false
      core.logallrefupdates=true
      remote.origin.url=https://PoseyDev@github.com/PoseyDev/MyProject.git
      remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
      api_logic_server@codespaces-966cb8:/workspaces/MyProject$
```


## Status - Running, still experimental

On 7/24/2022, the Admin App is working, cURL is working, and Swagger is working.  While still experimental, this looks very promising.
