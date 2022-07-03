# Why Docker: Reduce Install Confusion

Docker provides significant well-known advantages for development and deployment:</summary>

* simplified __development__ by eliminating an otherwise complex Python install

* popular runtime __deployment__ platform, based on a standard Linux base

* __isolation__ - in both cases, Docker applications encapsulate their environment, eliminating external dependencies.  Likewise, Docker applications will not affect other applications running on the same hardware

ApiLogicServer is therefore provided in a docker image, as described in the [readme](https://github.com/valhuber/ApiLogicServer/blob/main/README.md).  This page provides miscellaneous operational procedures to support Docker.

&nbsp;

## Install - `docker run` arguments
Once you've [installed Docker](../Testing#working-with-docker) itself, the `docker run` command above installs the ApiLogicServer docker (if it's not already there), and starts it, opening a terminal window on the Docker container.  Notes:
* the `v ${PWD}:/localhost` argument is what enables the ApiLogicServer to create / access the project on your local host
   * Windows - Powershell must be used (due to the `$(PWD)` syntax)
   * if you use Command Prompt, specify the local directory completely 
   
The **arguments** mean:
* **-it** - launch a terminal window for the Docker container
* **--name api_logic_server** - the name of the image on your local host
* **-rm** - remove the container once it stops (your project files are not lost - they are on your local host)
* **-p 5656:5656** - maps local (host) part to Docker port 
* **-v ${PWD}:/localhost** - maps a local directory to a mount name for Docker.  This is where a directory will be created for your new project.  
   * `${PWD}` is your current folder.  
      * You could also provide a specific folder, e.g., `~/dev/servers` (Unix), or `C:\Users\val\dev\servers` (windows)
   * `/localhost`is the mounted volume reference from inside the Docker container
* **`apilogicserver/api_logic_server`** - the name of the image to pull from Docker Hub.  
   * This will fetch the image first time, and will run it locally on subsequent runs
   * The image is not automatically refreshed -- install ApiLogicServer updates as described below

You may also wish to add a parameter for networking:
* **--net my-network** - attaches to my-network

On your Docker container, you can **inspect** your environment:
```
python py.py
```

Open a new terminal window on your **local host**, and find your docker IP address:

```
docker inspect api_logic_server  # you will find the ip, e.g., 172.17.0.2
```

</details>

## Connect to Dockerized Databases

One of the great things about Docker is the ability to install popular databases, with no hassle.  Follow the procedures described in [Testing](../Testing).

&nbsp;

## Docker and API Logic Projects

&nbsp;

### Create Docker Hub from API Logic Project

You can build a container for your ApiLogicProject:

1. Create / customize your project as your normally would
2. Edit `ApiLogicProject.dockerfile`: change your_repo/your_project as appropriate
3. In terminal (not in VSCode docker - docker is not installed there), cd to your project
4. Build a container for your project with terminal commands:

```bash
docker build -f ApiLogicProject.dockerfile -t your_repo/your_project --rm .
docker tag your_repo/your_project your_repo/your_project:1.00.00
docker login; docker push your_repo/your_project:1.00.00
```

To run your project container directly...

```bash
docker run -it --name your_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_repo/your_project

# start the image, but open terminal (e.g., for exploring docker image)
docker run -it --name your_project --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost your_repo/your_project bash
```

&nbsp;

### Start docker and load/run API Logic Project from `GitHub`

The `api_logic_server` image supports startup arguments so you can control the `api_logic_server` container, by running a startup script.  You can run your own script, or use the pre-supplied script (`/home/api_logic_server/bin/run-project.sh`) to load/run a git project.  For example:

```bash
docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost apilogicserver/api_logic_server sh /home/api_logic_server/bin/run-project.sh https://github.com/valhuber/Tutorial-ApiLogicProject.git /localhost/Project-Fixup.sh
```

will load the pre-built sample project from git, and run it.  Prior to execution it runs `/localhost/Project-Fixup.sh`, which in this case resets ui/admin files, like this:

```bash
#!/bin/bash

echo " "
echo "Project-Fixup script running"
pwd; ls
echo " "

cp ui/admin/admin_custom_nw.yaml ui/admin/admin.yaml
```

Instead of using a startup script, you can also use environment variables to achieve the same effect:

```bash
docker run -it --name api_logic_server --rm --net dev-network -p 5656:5656 -p 5002:5002 -v ${PWD}:/localhost   -e APILOGICSERVER_GIT='https://github.com/valhuber/Tutorial-ApiLogicProject.git' -e APILOGICSERVER_FIXUP='/localhost/Project-Fixup.sh' apilogicserver/api_logic_server
```

&nbsp;

# Appendix: General Docker Procedures

The sections below outline learnings from a beginners use of Docker (me).  If they save you time, we're both happy.

## Docker Installation

It's simple on a Mac, running _natively._  Other configurations may cause drama:

* Virtualization - under virtualization (e.g., VMWare Fusion - running windows under Mac), it is _much_ slower.
* Bootcamp - I was not able to make it work -- Windows thought the firmware did not support virtualization (on a large Intel-based Macbook Pro)

On the Fusion Windows, it *seemed* that I needed Windows _Pro_ (not _Home_).  There are various sites that
discuss Windows Home.  I was not willing to fiddle with that, so I just went Pro, which worked well.

## Preparing a Python Image

Recall that an **image** is something you can store on Docker Hub so others can download and run.  It's a good idea for project to have a repository of docker images, such as ApiLogicServer, test databases, etc.

The running thing is called a **container**.  They can but typically do not utilize local storage, instead accessing external files through _mounts_, and external systems (databases, APIs) via docker _networks_ and _ports_.

I had to prepare a Docker image for ApiLogicServer.  That requires a [Dockerfile](https://github.com/valhuber/ApiLogicServer/blob/main/docker/Dockerfile-main.Dockerfile), where I also keep my notes.

> The process was straight-forward using the noted links... until `pyodbc` was added for Sql Server.  That added 500MB, and was quite complicated.

## Preparing a Docker file from an image

In addition to the ApiLogicServer image, I wanted folks to be able to access a dockerized MySQL database.  Further, I wanted this to be *self-contained* to avoid creating files on folks' hard drives.

I therefore needed to:

1. acquire a self-contained MySQL image (again, that's not the default - the default is data persisted to a volume), and
2. update this database with test data
3. save this altered container as an image (`docker commit...`)

I used this [Dockerfile](https://github.com/valhuber/ApiLogicServer/blob/main/tests/docker_databases/Dockerfile-MySQL-container-data) which again includes my notes.


## SQL Server Docker creation

It was prepared as described in [this Dockerfile](https://github.com/valhuber/ApiLogicServer/blob/main/tests/docker_databases/Dockerfile-SqlSvr-instructions).

For JDBC tools, specify: ```jdbc:sqlserver://localhost:1433;database= NORTHWND```
