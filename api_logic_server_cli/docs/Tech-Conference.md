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
| SQLAlchemy      | Popular Python ORM | Python-friendly object-oriented database access |
| Flask      | Popular Python Web Framework | Use to add custom endpoints (examples provided) |
| VSCode     | Popular IDE | Runs in cloud via Codespaces (other IDEs as well) |
| Codespaces    | Cloud-based Dev Container | Provides IDE, git, etc - via a Browser interface|
| APIs   | Network-based database access | Via the SAFRS framework |
| React-Admin | UI framework for simplified React apps | Further simplified via YAML model |
| Declarative | Vague term ("what not how") | We'll describe key aspects |

### What you will need

You will need a laptop with a Browser connection, and a GitHub account.  You do *not* need a Python install, a database, or an IDE... and if you *do* have these, they won't be affected.

## Audience

This tutorial is for developers interested in database systems, and the technologies above.  Required background:

* basic programming familiarity (e.g, understand program structure, event-oriented programming)

* some database background (you are good to go if you have a basic understanding of tables, columns and foreign keys)


## Outline

This will be a series of short lectures, and hands-on usage (watch and/or do):

* Introduction (15 min)

    * What is API Logic Server

    * Why we wrote it

* Starting Codespaces - you'll create a cloud-based development environment, and access it VSCode via your browser (5 min)

* Create a Project (10 min, Total 30 min)

* Run the Project; we'll explore (30 min, Total 1 hour)

    * the User Interface - a multi-page, multi-table application (underlying technology is React Admin)

    * the API - using Swagger to explore pagination, filtering etc

* Customize the Project - use VSCode to: (45 min, Total 1.75 hour)

    * Explore Project Structure

    * Add an Endpoint, and test it with the debugger

    * Customize the API

* Explore logic

    * what it is
    
    * how to declare it
    
    * how it runs
    
    * how to debug it

    * what it means to be declarative (automatic invocation, ordering, optimization)

* Other Topics - explore on your own (time permitting - 15 min, Total 2 hours)

    * Testing with the Behave Framework

    * Schema Migrations with Alembic

# Additional Notes

Since API Logic Server is open source, you can obtain it - explore its value, investigate the key technologies shown in the table above

## Speaking Experience

I lead the PACE DBMS effort at Wang Labs, so gave many presentations for press briefings, User Conference Keynotes and working sessions, etc.

I was the CTO at Versata, so served as the lead technical presenter at User Groups and Conferences.
