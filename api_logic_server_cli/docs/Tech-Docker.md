
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