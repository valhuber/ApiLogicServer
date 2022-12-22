When you create an ApiLogicProject, the system creates a project like this, pre-configured for Developer Oprations.  See the notes below.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/devops/devops.png?raw=true"></figure>

## 1. Dev Container

You can customize projects using a local install, or a container (see the Install Guide).  Container support includes the `.devcontainer` folder, and the `devops/docker/ForVSCode.dockerfile`.  You should not need to alter these.

In addition to desktop-based development, these enable Codespaces support (see the Express Eval).

&nbsp;

## 2. Deployment Container

A common approach to deployment is to create a container for your project.  The `build-container.dockerfile` is created for this purpose.

You will need to edit it to reflect your project and Docker account names.

&nbsp;

## 3.  Launch Configurations

These are created so you can run the API Logic Server, run tests, etc.  You should not need to modify these, but you may wish to extend them.

&nbsp;

## 4. Python `venv`

The creation process builds a standard `requirements.txt` file.  You can create your `venv` with this, and (if your IDE does not provide it) the `venv.sh/ps1` files to initialize your `venv`.

&nbsp;

## 5. GitHub

Your project includes a suggested `.gitignore` file (alter as desired).  You can use git in standard ways to push and pull changes.  Some IDEs support the initial GitHub creation (see [VSCode publish](https://stackoverflow.com/questions/46877667/how-to-add-a-new-project-to-github-using-vs-code){:target="_blank" rel="noopener"}, or you can use the `git_push_new_project.sh` file. 

&nbsp;

## 6. `env` support

Most deployment procedures discourage database names / passwords to be in project files and GitHub, instead preferring to specify these via `env` variables.  The `config.py` file is designed to use the environment variable `SQLALCHEMY_DATABASE_URI` if it is provided.
