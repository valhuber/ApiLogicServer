[CodeSpaces](https://github.com/features/codespaces){:target="_blank" rel="noopener"} is a GitHub project that enables you to use VSCode in your Browser to develop on rapidly deployed docker containers.  It's quite remarkable.  


&nbsp;

## Create an API Logic Server Project for Codespaces

See the [procedure here](../Manage-GitHub).

&nbsp;

## Create New Projects from Codespaces (currently not working)

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

