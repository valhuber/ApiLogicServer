This page documents my move from a 2019 Intel MBP 16 to a 2021 M1 Pro 14 (32G).

# Requirements

Besides typical home use, I rely on this machine for API Logic Server dev.  That entails testing across

| Aspect  | Specifics    | Using   |
:---------|:-----------|:------------|
| OS      | Mac, Windows 11, Unix (Ubuntu) | Parallels 14 |
| DB      | Sqlite, MySql, Sql/Server, Postgres | Docker |
| IDE     | VSCode, Pycharm | |
| Docs    | GitHub Pages, MKDocs, Google Docs, slides | |
| Other   | Better Touch Tool | |

# Notes

## Parallels / Windows11

This was rather remarkable.  Under MBP 16 / VMWare Fusion / Windows 10, boot time was 70 seconds.  Under M1 / Parallels / Windows 11, it is 8-10 seconds.

## Docker - For ApiLogicServer

Installs and runs without issue.  

### Initially slower

It is slower, however, on M1.  For example, once started, the `ApiLogicServer welcome` command takes under a second on x86, but 7-9 on M1.

### Update - ARM-based images are quite fast

On investigation, you can create separate docker images for x86 vs. ARM.  The ARM version starts instantly.


#### Building Dual Docker Images - failing

It appears to be possible to build images that run on both AMD and ARM, but I have not been able to address that.
  Initial attempt failed with:

```
multiarch-support:amd64 : Depends: libc6:amd64 (>= 2.3.6-2) but it is not inst
```

Researching [this](https://stackoverflow.com/questions/71310357/multiarch-supportamd64-depends-libc6amd64-2-3-6-2-but-it-is-not-instal).


## Install initially failed due to `psycopg2` (Postgres)

Ran into significant drame with Postgres support - `psycopg2`.  Under [investigation](pip install psycopg2_m1-*-macosx_12_0_arm64.whl).  [Evidently](https://github.com/psycopg/psycopg/issues/344) this is not supported out of the box.  There are [various approaches](https://doesitarm.com/app/psycopg2) that work if you are willing to install Postgres locally.  I had been using Docker, so this remains an open item.

So that M1 Macs work, API Logic Server version 05.03.34 has removed the psycopg2 from the install, so it needs to be [installed manually](../Install-psycopg2).

### Resolved - M1 support released

Update: as of Oct 2022, the most recent release of `psycopg2` provides ARM support.  With this, Postgres happily runs fine.  As of 6.1.2, it will no longer require manual install.

## Docker Databases - running

The [Docker database images](..Database-Connectivity/) work for M1 Macs, __except SQL/Server__ (it fails to start). It is architecture specific.

These solutions were successful [as described here](https://github.com/valhuber/ApiLogicServer/blob/main/tests/docker_databases/Dockerfile-SqlSvr-instructions-m1).  Many thanks for the following information:

* [ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16)

* [SQL/Server](https://medium.com/geekculture/docker-express-running-a-local-sql-server-on-your-m1-mac-8bbc22c49dc9)
