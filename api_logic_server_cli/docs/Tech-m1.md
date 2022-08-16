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

## Dev Install fails due to `psycopg2`

Ran into significant drame with Postgres support - `psycopg2`.  Under [investigation](pip install psycopg2_m1-*-macosx_12_0_arm64.whl).

## Docker Databases

Was able to run MySQL, any performance degradation was not user-visible.

