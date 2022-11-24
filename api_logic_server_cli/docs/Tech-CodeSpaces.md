[CodeSpaces](https://github.com/features/codespaces){:target="_blank" rel="noopener"} is a GitHub project that enables you to use VSCode in your Browser to develop on rapidly deployed docker containers.  It's quite remarkable.  

# Making API Logic Server work with Codespaces

This page describes the _(internal)_ journey to make Codespaces work.  It is intended to provide feedback to the Codespaces team, and perhaps to others trying to make projects works with Codespaces.

> To _use_ Codespaces, see the [procedure here](../Manage-GitHub).

TL;DR:

With a fair amount of help, I can now create executable API Logic Server Projects with [minimal configuration]().  Open items are:

1. Ability to push created project to new git repo (this is the biggest item)

2. Cleaner way to compute the Host Address

3. Cleaner way to create ___public___ Ports

&nbsp;

## Creating containerized projects

[Containerized API Logic Project creation](../Tech-Docker/#creating-containerized-api-logic-server-projects-for-vscode) was already provided, so I was able to create projects and open them in Codespaces with no additional work.

&nbsp;

## Host and Port Configuration

API Logic Server creates web apps, so is senstive to Host and Port designations.  

&nbsp;

### First Try: _Manual_ Host and Port Configuration

After some investigation and help from forums, I was able to define Run Configurations to make API Logic Server Projects run, like this:

```json
        {
            "name": "Codespaces-ApiLogicServer",
            "type": "python",
            "request": "launch",
            "program": "api_logic_server_run.py",
            "redirectOutput": true,
            "justMyCode": false,
            "args": [
                "--flask_host=localhost", "--port=5656", "--verbose=True",
                "--swagger_host=valhuber-tutorial-apilogicproject-jjr5qwg72vxg-5656.githubpreview.dev", 
                "--swagger_port=443", "--http_type=https"
            ],
            "console": "integratedTerminal"
        },
```

I regarded this as barely adequate, far too fiddly to be considered friendly.  So, I looked for ways to automate this, so you could run with the standard Run Configuration, either in Codespaces or locally:

```json
        {
            "name": "ApiLogicServer",
            "type": "python",
            "request": "launch",
            "program": "api_logic_server_run.py",
            "redirectOutput": true,
            "justMyCode": false,
            "args": ["--flask_host=localhost", "--port=5656", "--swagger_host=localhost", "--verbose=False"],
            "console": "integratedTerminal"
        },
```

&nbsp;

### Automated Host Address / Port Configuration

For this, I updated [api_logic_server_run.py](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/api_logic_server_run.py){:target="_blank" rel="noopener"} (the python file that starts the server):

```python
    use_codespace_defaulting = True  # experimental support to run default launch config
    if use_codespace_defaulting and os.getenv('CODESPACES') and swagger_host == 'localhost':
        app_logger.info('\n Applying Codespaces default port settings')
        swagger_host = os.getenv('CODESPACE_NAME') + '-5656.githubpreview.dev'
        swagger_port = 443
        http_type = 'https'
```

Good progress, enabling users to run locally or in Codespaces with the same Run Configuration (shown above).  But it still required users to _create_ the port, so I wanted to automate that...

&nbsp;

### Automated Port Creation

The Codecpaces team showed me how to create ports in the [.devcontainer/devcontainer.json](https://github.com/ApiLogicServer/ApiLogicProject/blob/main/.devcontainer/devcontainer.json){:target="_blank" rel="noopener"}, adding lines like:

```json
	"portsAttributes": {
		"5656": {
			"label": "AdminApp"
		}
	},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	"forwardPorts": [5656],
```

A big step forward, but it failed because the Port was not ___public___.

&nbsp;

#### Make the created port _public_

[This link](https://github.com/orgs/community/discussions/4068){:target="_blank" rel="noopener"} describes how to work around missing setting for creating public ports.  

This approach relies upon the `gh` CLI.  Adding this to the `devcontainer` installs the `gh` CLI,

```json	
	"features": {
		"github-cli": "latest"
	  },

	"postAttachCommand": "/bin/bash .devcontainer/setup.sh"
```

This enables us to [/bin/bash .devcontainer/setup.sh](https://github.com/ApiLogicServer/ApiLogicProject/blob/main/.devcontainer/setup.sh):

```bash
gh codespace ports visibility 5656:public -c $CODESPACE_NAME
```

As noted in form, this may be subject to race conditions, so I also updated the [`.bashrc`](https://github.com/valhuber/ApiLogicServer/blob/main/.bashrc) built by ApiLogicServer:

```bash
if [[ -z "${CODESPACES}" ]]; then
  LOAD_GIT="Not Codespaces"
else
  echo "Now: gh codespace ports visibility 5656:public -c $CODESPACE_NAME"
  gh codespace ports visibility 5656:public -c $CODESPACE_NAME
fi
```

Not pretty, but API Logic Server users would not see this.

@nbsp;

## Outstanding Items

### Create New Projects from Codespaces (currently not working)

We also explored creating a new project from the Codespaces example itself.  You can create projects under Codespaces just as you do for local installs:

```bash title="Create new project in Codespaces"
cd ..   # back to the Workspaces folder
ApiLogicServer create --db_url= --project_name=fromcs
```

Problems occur, however, when you try to [add existing project to git](https://gist.github.com/alexpchin/102854243cd066f8b88e):

1. Create `fromcs` on GitHub (leave it empty to avoid merges)
2. Attempt to push:

```bash title="Push to git (fails)"
cd fromcs        # created above
git init
git branch -m main  # as required... git projects often created with this as default branch (vs. say, master)
git add .
git commit -m 'First commit'
git remote add origin https://github.com/valhuber/fromcs.git
git remote -v
git remote set-url origin "https://valhuber@github.com/valhuber/fromcs.git"
git push origin main  # may need to be master
      remote: Permission to valhuber/fromcs.git denied to valhuber.
      fatal: unable to access 'https://github.com/valhuber/fromcs.git/': The requested URL returned error: 403```

Git config status:
```bash title="git config --list"
api_logic_server@codespaces-9f8d7a:/workspaces/fromcs$ git config --list
      credential.helper=/.codespaces/bin/gitcredential_github.sh
      user.name=Val Huber
      user.email=valjhuber@gmail.com
      gpg.program=/.codespaces/bin/gh-gpgsign
      core.repositoryformatversion=0
      core.filemode=true
      core.bare=false
      core.logallrefupdates=true
      remote.origin.url=https://github.com/valhuber/fromcs.git
      remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
      api_logic_server@codespaces-9f8d7a:/workspaces/fromcs$ 
```

&nbsp;

### Stable Host

&nbsp;

### Cleaner Public Port Creation
