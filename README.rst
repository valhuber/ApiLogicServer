API Logic Server
================

Creates an executable API from a database:

- **API:** `swagger/OpenAPI <https://swagger.io/>`_ and `JSON:API <jsonapi.org>`_ compliant.  Uses `SAFRS <https://pypi.org/project/safrs/>`_ , a modern approach that enables client applications to configure their own API to reduce network traffic.

- **Web App:** a multi-page, multi-table web app; incorporates `Flask AppBuilder <https://flask-appbuilder.readthedocs.io/en/latest/>`_ and `fab-quickstart <https://pypi.org/project/fab-quick-start/>`_.

- **Logic:** spreadsheet-like rules for multi-table derivations and constraint that reduce transaction logic by 40X, using `Logic Bank <https://pypi.org/project/logicbank//>`_.

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


Generation
**********
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

You may also wish to include the ``open_with`` parameter,
to open an IDE or Editor on the created project.  For example,
PyCharm (``charm``) will open the project and create / initialize the ``venv``
automatically (some PyCharm configuration may be required):

.. code-block:: Python

    ApiLogicServer create --project_name=my_api_logic_server db_url=sqlite:///nw.sqlite --open_with=charm


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

Demo / Tutorial (no install)
----------------------------
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
- Gloria Huber and Denny McKinney, for doc review


Change Log
----------
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
