API Logic Server
================

API-enabled backend development takes time.  This can block Mobile App Dev projects, and
strategic business initiatives for internal / external (B2B) integration.

API Logic Server creates an **executable JSON:API backend**, *instantly*,
with crud support (including filtering, sorting, pagination), and
related data retrieval for every table.  With Swagger.

It also creates a **multi-page, multi-table web app**, *instantly*,
so developers can engage with business users - early in the project - for agile iterations.

Finally, it provides a logic engine that executes **spreadsheet-like rules**
for multi-table derivations and constraints
- *40X* more concise than legacy code, extensible with Python.

This `video <https://www.youtube.com/watch?v=gVTdu6c0iSI/>`_ shows the creation of a backend - in minutes -  that would typically require weeks.

With over 12k downloads in its first 2 months, API Logic Server is
`Open Source on GitHub <https://github.com/valhuber/ApiLogicServer#readme/>`_.


Usage
-----

Installation
************
Install with pip:

.. code-block:: Python

    cd ~/Desktop
    mkdir server
    cd server
    virtualenv venv
    source venv/bin/activate
    # windows venv\Scripts\activate
    pip install ApiLogicServer


Creation
********
This verifies proper install:

.. code-block:: Python

    ApiLogicServer create --project_name=my_api_logic_server
    cd my_api_logic_server  # create / initialize the venv
    virtualenv venv
    source venv/bin/activate
    # windows venv\Scripts\activate
    pip install -r requirements.txt

More commonly, you would include the ``db_url`` parameter,
a SQLAlchemy url designating the database used for creation.

Execution
*********

.. code-block:: Python

    python api_logic_server_run.py
    python ui/basic_web_app/run.py



Features
--------

API: SAFRS JSON:API and Swagger
*******************************

Your API is available in swagger:

.. image:: https://github.com/valhuber/ApiLogicServer/blob/main/images/swagger.png?raw=true
    :width: 800px
    :align: center


Basic Web App - Flask Appbuilder
********************************
Generated fab pages look as shown below:

#. **Multi-page:** apps include 1 page per table

#. **Multi-table:** pages include ``related_views`` for each related child table, and join in parent data

#. **Favorite field first:** first-displayed field is "name", or `contains` "name" (configurable)

#. **Predictive joins:** favorite field of each parent is shown (product *name* - not product *id*)

#. **Ids last:** such boring fields are not shown on lists, and at the end on other pages

.. image:: https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png
    :width: 800px
    :align: center

Customize your app by editing ``ui/basic_web_app/app/views.py``.

Logic:
******
Logic is declared in Python (example below), and is:

- **Extensible:** logic consists of rules (see below), plus standard Python code

- **Multi-table:** rules like ``sum`` automate multi-table transactions

- **Scalable:** rules are pruned and optimized; for example, sums are processed as *1 row adjustment updates,* rather than expensive SQL aggregate queries

- **Manageable:** develop and debug your rules in IDEs, manage it in SCS systems (such as `git`) using existing procedures

The following 5 rules represent the same logic as 200 lines
of Python:

.. image:: https://github.com/valhuber/LogicBank/raw/main/images/example.png
    :width: 800px
    :align: center

Declare your logic by editing ``logic/rules_bank.py``

Demo / Tutorial (no database install)
-------------------------------------
See the `Tutorial. <https://github.com/valhuber/ApiLogicServerTutorial/>`_


More information:
-----------------
The github project includes documentation and examples.


Acknowledgements
----------------
Many thanks to

- Mike Bayer, for SQLAlchemy
- Thomas Pollet, for SAFRS
- Daniel Gaspar, for Flask AppBuilder
- Denny McKinney, for Tutorial review
- Achim Götz, for design collaboration
- Michael Holleran, for design collaboration and testing
- Nishanth Shyamsundar, for review and testing
- Gloria Huber and Denny McKinney, for doc review


Change Log
----------
03/23/2021 - 02.00.01: Minor doc changes, CLI argument simplification for default db_url

03/17/2021 - 02.00.00: Create create_admin.sh, copy sqlite3 DBs locally, model_ext

03/10/2021 - 01.04.10: Fix issues in creating Basic Web App

03/03/2021 - 01.04.09: Services, cleanup main api_run

02/23/2021 - 01.04.08: Minor - proper log level for APIs

02/20/2021 - 01.04.07: Tutorial, Logic Bank 0.9.4 (bad warning message)

02/15/2021 - 01.04.06: Tutorial

02/08/2021 - 01.04.05: add employee audit foreign key in nw.sqlite

02/07/2021 - 01.04.04: fix default project name

02/07/2021 - 01.04.03: db_url default (for Jupyter)

02/07/2021 - 01.04.02: Internal Renaming

02/06/2021 - 01.04.00: Fix constraint reporting, get related (issues 7,8)

02/02/2021 - 01.04.00: TBD

02/01/2021 - 01.03.01: Fix logic logging, nw rules

01/31/2021 - 01.03.00: Resolve n:m relationships (revised models.py)

01/29/2021 - 01.02.04: Minor cleanup

01/29/2021 - 01.02.03: Flask AppBuilder fixes - Admin setup, class vs table names (wip)

01/28/2021 - 01.02.02: Command line cleanup

01/27/2021 - 01.02.00: Many
* Host option
* --from_git defaults to local directory
* hello world example
* nw rules pre-created

01/25/2021 - 01.01.01: MySQL fixes
