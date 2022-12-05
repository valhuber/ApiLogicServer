Submission materials for [PyCon 2023](https://us.pycon.org/2023/speaking/talks/){:target="_blank" rel="noopener"}, April 19 in Salt Lake City.  Links:

* [Tutorial Samples](https://us.pycon.org/2023/speaking/tutorials/samples/){:target="_blank" rel="noopener"}

* [Proposal Submission](https://pretalx.com/pyconus2023/submit/H2DMVf/info/){:target="_blank" rel="noopener"}

# Description

## Title

  > How to Create Web Applications Instantly with API Logic Server - create with one command, customize in your IDE

## Description

Creating web-oriented database projects requires substantial time and background.  In this Tutorial, we introduce a meaningfully faster and simpler approach.

&nbsp;

### Overview

In this tutorial:

* Seeing is believing - you will build, run and customize a complete multi-table database web app
    * You will be able to use it tomorrow on your organizations databases
* You will also gain an excellent introduction to several popular Python technologies -- web apps, database access, project development, etc.

&nbsp;

### What is API Logic Server?

API Logic Server is an open source Python system that creates __customizable database web app projects:__

* Creation is __Instant:__ create _executable_ projects from your database with a _single_ command.  Projects are __Highly Functional,__ providing:

    * __API:__ an endpoint for each table, with filtering, sorting, pagination and related data access

    * __Admin UI:__ multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show

* __Projects are Customizable, using _your IDE_:__ such as VSCode, PyCharm, etc, for familiar edit/debug services

* __Business Logic Automation:__ using unique spreadsheet-like rules, extensible with Python :trophy:

&nbsp;

### Tutorial - build and customize a system

In this Tutorial, you will:

* Create an interesting multi-table application from a pre-supplied sample database

* Run it

* Customize it using VSCode.

* Learn about declarative, spreadsheet-like business logic for multi-table constraints and derivations

&nbsp;

### Excellent Intro to Popular Technologies

This talk will also give you an intro to other technologies you may have already wanted to explore, with _running code_ you can extend:

| Technology  | Used For    | Notes   |
:---------|:-----------|:------------|
| __Python__  | Popular OO Language | New to Python?  This is a great place to learn it<br> * Start with _running_ code<br> * Explore, edit and debug in VSCode<br> * No install, no config |
| __SQLAlchemy__  | Popular Python ORM | Python-friendly object-oriented database access |
| __Flask__  | Popular Python Web Framework | Use to add custom endpoints (examples provided) |
| __VSCode__  | Popular IDE | Use to customize API Logic Projects |
| __Codespaces__  | Cloud-based Dev Container | Provides IDE, git, etc - via a *Browser interface* |
| __APIs__  | Networked database access | Via the SAFRS framework |
| __Docker__ | *Isolated* Containers | Eg., DBMS, API Logic Server, Your App |
| __React-Admin__ | Simplified React UI framework | Further simplified via YAML model |
| __Declarative__ | Vague term ("what not how") | We'll describe key aspects |

&nbsp;

### What you will need

You will need a laptop with a Browser connection, and a GitHub account.  You do *not* need a Python install, a database, or an IDE... and if you *do* have these, they won't be affected.

&nbsp;

## Audience

This tutorial is for developers interested in database systems, and the technologies above.  Required background:

* Basic programming familiarity (if you are familiar with `if/else`, parameterized function calls, `row.column` object access, and basic event oriented programming, you are all set).  Python experience is not required.

* Some database background (if you have heard of tables, columns and foreign keys, you are good to go).


&nbsp;

## Outline

This will be a series of short lectures, and hands-on usage (watch and/or do):

| Section  | Duration    | We'll cover   |
:---------|:-----------|:------------|
| __Introduction__ | 15 min | * What is API Logic Server<br>* Why we wrote it |
| __Starting Codespaces__ | 15 min (total 30) | * Create a cloud-based development environment<br> * Access it VSCode via your browser) |
| __Create Project__  | 15 min (total 45) | Using pre-supplied sample database |
| __Explore Project__ | 30 min (total 1.25 hours) | * User Interface - a multi-page, multi-table application<br>* API - using Swagger to explore pagination, filtering etc |
| __Customize Project__  | 30 min (total 1.75 hours) | * Explore Project Structure in VSCode<br> * API: Add an Endpoint, and test it with the debugger<br>* UI: Adjust captions, hide/show fields |
| __Business Logic__ | 30 min (total 2.25 hours) | * what it is<br> * how to declare it<br> * how it runs<br> * how to debug it<br> * what it means to be _declarative_ |
| __Other Topics__ | 15 min (total 2.25 hours) | * Testing with the Behave Framework<br> * Schema Migrations with Alembic |

Yes, a lot to cover, but automation makes it possible.  Even easy.

&nbsp;

# Additional Notes

Since API Logic Server is open source, you can obtain it - explore its value, and/or investigate the Popular Technologies listed in the table above.

&nbsp;

## Speaking Experience

I have given hundreds of technology presentations to large and small groups, for both technical and business audiences.

* I lead the PACE DBMS effort at Wang Labs, so gave many presentations for press briefings, User Conference Keynotes and working sessions, etc.

* I was the CTO at Versata, so served as the lead technical presenter at User Groups and Conferences.
