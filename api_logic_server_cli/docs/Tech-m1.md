This page documents my move from a 2019 Intel MBP 16 to a 2021 M1 Pro 14 (32G).

# Requirements

Besides typical home use, I rely on this machine for API Logic Server dev.  That entails testing across

| Aspect  | Specifics    | Using   |
:---------|:-----------|:------------|
| OS      | Mac, Windows 11, Unix (Ubuntu) | Parallels 14 |
| DB      | Sqlite, MySql, Sql/Server, Postgres | Docker |
| IDE     | VSCode, Pycharm | |
| Tools   | Atom, Firefox | |
| Docs    | GitHub Pages, MKDocs, Google Docs, slides | |
| Other   | Better Touch Tool | |

# Notes

## Docker - ApiLogicServer

Installs and runs without issue.  

It is slower, however, on M1.  For example, once started, the `ApiLogicServer welcome` command takes under a second on x86, but 7-9 on M1.

## Install fails due to `psycopg2`

Ran into significant drame with Postgres support - `psycopg2`.  Under [investigation](pip install psycopg2_m1-*-macosx_12_0_arm64.whl).  [Evidently](https://github.com/psycopg/psycopg/issues/344) this is not supported out of the box.  There are [various approaches](https://doesitarm.com/app/psycopg2) that work if you are willing to install Postgres locally.  I had been using Docker, so this remains an open item.

So that M1 Macs work, API Logic Server version 05.03.34 has removed the psycopg2 from the install, so it needs to be [installed manually](../Install-psycopg2).

## Sql Server Docker Fails

The [Docker database images](..Database-Connectivity/) work for M1 Macs, __except SQL/Server__ (it fails to start).

## Docker Databases

Was able to run MySQL, any performance degradation was not user-visible.

