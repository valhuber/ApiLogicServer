API Logic Server
================

Creates an executable API from a database:

- **API:** `swagger/OpenAPI <https://swagger.io/>`_ and `JSON:API <jsonapi.org>`_ compliant.  Uses `SAFRS <https://pypi.org/project/safrs/>`_ , a modern approach that enables client applications to configure their own API to reduce network traffic.

- **Web App:** a multi-page, multi-table web app; incorporates `fab-quickstart <https://pypi.org/project/fab-quick-start/>`_.

- **Logic:** spreadsheet-like rules for multi-table derivations and constraint that reduce transaction logic by 40X, using `Logic Bank <https://pypi.org/project/logicbank//>`_.


Installation
------------
Install with pip:

.. code-block:: Python

    cd ~/Desktop
    mkdir server
    cd server
    virtualenv venv
    pip install ApiLogicServer


Generation
----------
.. code-block:: Python

    ApiLogicServer create --project_name=my_api_logic_server


Execution
---------
.. code-block:: Python

    cd my_api_logic_server
    python api_logic_server_run.py
    python ui/basic_web_app/run.py

API: SAFRS JSON:API and Swagger
-------------------------------
Your API is available in swagger:

.. image:: https://github.com/valhuber/ApiLogicServer/blob/main/images/swagger.png?raw=true
    :width: 800px
    :align: center


Basic Web App - Flask Appbuilder
--------------------------------
Generated fab pages look as shown below:

#. **Multi-page:** apps include 1 page per table

#. **Multi-table:** pages include ``related_views`` for each related child table, and join in parent data

#. **Favorite field first:** first-displayed field is "name", or `contains` "name" (configurable)

#. **Predictive joins:** favorite field of each parent is shown (product *name* - not product *id*)

#. **Ids last:** such boring fields are not shown on lists, and at the end on other pages

.. image:: https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png
    :width: 800px
    :align: center

Customize your app by editing `ui/basic_web_app/app/views.py`.

Logic:
------
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

Declare your logic by editing `logic/rules_bank.py`


More information:
-----------------
The github project includes documentation and examples.


Acknowledgements
----------------
Many thanks to

- Thomas Pollet, for SAFRS
- Daniel Gaspar
- Achim Götz, for design collaboration


Change Log
----------

0.0.6 - Initial Version