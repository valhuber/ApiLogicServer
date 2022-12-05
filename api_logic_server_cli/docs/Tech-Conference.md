Submission materials for [PyCon 2023](https://us.pycon.org/2023/speaking/talks/){:target="_blank" rel="noopener"}, April 19 in Salt Lake City.  Links:

* [Tutorial Samples](https://us.pycon.org/2023/speaking/tutorials/samples/){:target="_blank" rel="noopener"}

* [Proposal Submission](https://pretalx.com/pyconus2023/submit/H2DMVf/info/){:target="_blank" rel="noopener"}

# Description

## Title

  > Using API Logic Server for Web Applications - create with one command, customize in your IDE

## Description

### What is API Logic Server

API Logic Server is an open source Python system that creates __customizable database web app projects:__

* Creation is __Instant:__ create _executable_ projects from your database with a _single_ command.  Projects are __Highly Functional,__ providing:

    * __API:__ an endpoint for each table, with filtering, sorting, pagination and related data access

    * __Admin UI:__ multi-page / multi-table apps, with page navigations, automatic joins and declarative hide/show

* __Projects are Customizable, using _your IDE_:__ such as VSCode, PyCharm, etc, for familiar edit/debug services

* __Business Logic Automation:__ using unique spreadsheet-like rules, extensible with Python :trophy:

### Tutorial - build and customize a system

In this Tutorial, you will:

* create an application

* run it

* customize it using VSCode.

* learn about declarative, spreadsheet-like business logic for multi-table constraints and derivations

### Excellent Intro to Popular Technologies

This talk will also give you a good intro to other technologies you may have already wanted to explore, with running code you can extend:

| Technology  | Used For    | Notes   |
:---------|:-----------|:------------|
| __SQLAlchemy__  | Popular Python ORM | Python-friendly object-oriented database access |
| __Flask__  | Popular Python Web Framework | Use to add custom endpoints (examples provided) |
| __VSCode__  | Popular IDE | Use to customize API Logic Projects |
| __Codespaces__  | Cloud-based Dev Container | Provides IDE, git, etc - via a *Browser interface* |
| __APIs__  | Networked database access | Via the SAFRS framework |
| __React-Admin__ | Simplified React UI framework | Further simplified via YAML model |
| __Declarative__ | Vague term ("what not how") | We'll describe key aspects |

### What you will need

You will need a laptop with a Browser connection, and a GitHub account.  You do *not* need a Python install, a database, or an IDE... and if you *do* have these, they won't be affected.

## Audience

This tutorial is for developers interested in database systems, and the technologies above.  Required background:

* basic programming familiarity (e.g, understand program structure, event-oriented programming)

* some database background (you are good to go if you have a basic understanding of tables, columns and foreign keys)


## Outline

This will be a series of short lectures, and hands-on usage (watch and/or do):

| Section  | Duration    | We'll cover   |
:---------|:-----------|:------------|
| __Introduction__ | 15 min | * What is API Logic Server<br>* Why we wrote it |
| __Starting Codespaces__ | 5 min | * Create a cloud-based development environment<br> * Access it VSCode via your browser) |
| __Create Project__  | 10 min (total 30) | Using pre-supplied sample database |
| __Explore Project__ | 30 min (total 1 hour) | * User Interface - a multi-page, multi-table application (underlying technology is React Admin)<br>* API - using Swagger to explore pagination, filtering et |
| __Customize Project__  | 45 min (total 1.75 hours) | * Explore Project Structure in VSCode<br>API: Add an Endpoint, and test it with the debugger<br>* UI (adjust captions, hide/show fields) |
| __Business Logic__ | ?? | * what it is<br> * how to declare it<br> * how it runs<br> * how to debug it<br> * what it means to be _declarative_ (automatic invocation, ordering, optimization) |
| __Other Topics__ | As time permits | * Testing with the Behave Framework<br> * Schema Migrations with Alembic |

# Additional Notes

Since API Logic Server is open source, you can obtain it - explore its value, investigate the Popular Technologies listed in the table above

## Speaking Experience

I lead the PACE DBMS effort at Wang Labs, so gave many presentations for press briefings, User Conference Keynotes and working sessions, etc.

I was the CTO at Versata, so served as the lead technical presenter at User Groups and Conferences.
