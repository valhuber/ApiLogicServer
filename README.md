# API Logic Server

Creates an executable API from a database:

- **API:** [swagger/OpenAPI](https://swagger.io/)
  and [JSON:API](https://jsonapi.org) compliant.
  Uses [SAFRS](https://pypi.org/project/safrs/), a modern approach that enables client applications to configure their own API to reduce network traffic.


- **Web App:** a multi-page, multi-table web app;
  uses [fab-quickstart](https://pypi.org/project/fab-quick-start).


- **Logic:** spreadsheet-like rules for multi-table derivations and constraint
  that reduce transaction logic by 40X,
  using [Logic Bank](https://pypi.org/project/logicbank).

## Usage

### Installation

Install with pip:

```
cd ~/Desktop
mkdir server
cd server
virtualenv venv
source venv/bin/activate
# windows venv\Scripts\activate
pip install ApiLogicServer
```

### Generation

This verifies proper install:

```
ApiLogicServer create --project_name=my_api_logic_server
cd my_api_logic_server
virtualenv venv
source venv/bin/activate
# windows venv\Scripts\activate
pip install -r requirements.txt
```

More commonly, you would include the ``db_url`` parameter,
a SQLAlchemy url designating the database used for creation.

You may also wish to include the ``open_with`` parameter,
to open an IDE or Editor on the created project.  For example,
PyCharm (``charm``) will open the project and create / initialize the ``venv``
automatically (some PyCharm configuration may be required):

```
ApiLogicServer create --project_name=my_api_logic_server db_url=sqlite:///nw.sqlite --open_with=charm
```


### Execution

```
python api_logic_server_run.py
python ui/basic_web_app/run.py
```


## Features


### API: SAFRS JSON:API and Swagger


Your API is available in swagger:

<figure><img src="images/swagger.png"></figure>


### Basic Web App - Flask Appbuilder

Generated fab pages look as shown below:

1. **Multi-page:** apps include 1 page per table

2. **Multi-table:** pages include ``related_views`` for each related child table, and join in parent data

3. **Favorite field first:** first-displayed field is "name", or `contains` "name" (configurable)

4. **Predictive joins:** favorite field of each parent is shown (product *name* - not product *id*)

5. **Ids last:** such boring fields are not shown on lists, and at the end on other pages

<figure><img src="https://raw.githubusercontent.com/valhuber/fab-quick-start/master/images/generated-page.png"></figure>

Customize your app by editing ``ui/basic_web_app/app/views.py``.

### Logic

Logic is declared in Python (example below), and is:

- **Extensible:** logic consists of rules (see below), plus standard Python code

- **Multi-table:** rules like ``sum`` automate multi-table transactions

- **Scalable:** rules are pruned and optimized; for example, sums are processed as *1 row adjustment updates,* rather than expensive SQL aggregate queries

- **Manageable:** develop and debug your rules in IDEs, manage it in SCS systems (such as `git`) using existing procedures

The following 5 rules represent the same logic as 200 lines
of Python:
<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/example.png"></figure>

Declare your logic by editing ``logic/rules_bank.py``


## More information

The github project includes documentation and examples.


## Acknowledgements

Many thanks to

- Thomas Pollet, for SAFRS
- Daniel Gaspar, for Flask AppBuilder
- Achim Götz, for design collaboration


## Change Log

1.0.7 - Initial Version

1.0.8 - Fix windows bug, options to specify clone-from and open-with