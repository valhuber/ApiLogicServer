Logic Bank governs SQLAlchemy
update transaction logic - multi-table derivations, constraints,
and actions such as sending mail or messages. Logic consists of both:

* **Rules - 40X** more concise
using a spreadsheet-like paradigm, and

* **Python - control and extensibility,**
using standard tools and techniques

> The example described below is a _typical_ example of multi-table logic.
>
> You may find it helpful to begin with [this Tutorial, using a basic example](../../wiki/Tutorial).

This readme contains:

1. [Background](#background)
    * [Why](#why---simple-cocktail-napkin-spec-explodes-into-massive-legacy-code) - problems addressed
    * [What](#what---declare-spreadsheet-like-rules---40x-more-concise) - what are spreadsheet-like rules
    * [How](#how---usage-and-operation-overview) - usage / operation overview
    * [Logic Execution](#logic-execution-add-order---watch-react-chain) - sample transaction execution, reuse and scalability
    * [Instant Web App](#an-agile-perspective) - built using [Flask App Builder Quickstart](https://github.com/valhuber/fab-quick-start/wiki)
1. [Install Instructions](#installation) - of Python and Logic Bank, with verify and run instructions
1. [Project Information](#project-information)


# Background

## Why - Simple Cocktail-Napkin Spec Explodes into Massive Legacy Code

If you've coded backend database logic - multi-table derivations and constraints -
you know how much work it is, and how tedious.  Whether you code it in
triggers and stored procedures, in ORM events, or UI controllers, it's a lot:
typically nearly half the effort for a database project.

It's also incredibly repetitive - you often get the feeling you're doing the same thing over and over.

And you're right.  It's because backend logic follows patterns of "what" is supposed to happen.
And your code is the "how".  Suddenly, a simple cocktail napkin specification explodes into a massive amount of legacy code:

<figure><img src="images/overview/rules-vs-code.png"></figure>

Logic Bank was designed to make the cocktail napkin spec _executable_.

## What - Declare Spreadsheet-like Rules - 40X More Concise
Logic Bank introduces rules that are 40X more concise than legacy code.
The 5 rules below (lines 40-49) express the same logic as 200 lines of code [**(see them here)**](examples/nw/logic/legacy).  That's because rules are all about "what"
-- spreadsheet-like expressions that automate the tedious "how":

<figure><img src="images/overview/cocktail-logic-bank.png"></figure>

### Standard Python - Declare, Extend, Manage
Logic Bank is fully integrated with Python:
* **Declare** rules in Python as shown above (more details in How, below)
* **Extend** rules with Python (rule on line 51 invokes the Python function on line 32)
* **Manage** logic using your existing IDE (PyCharm, VSCode etc for code completion, debugging, etc),
and source control tools and procedures

### Technology Evaluation
40X is... _large_ - do these results hold in practice?
See [here](../../wiki#technology-evaluation) for
additional background, and real world experience.


## How - Usage and Operation Overview
<figure><img src="images/architecture.png"></figure>
Logic Bank operates as shown above:

 1. **Declare and Activate** (see example above):

    a. Create a ```declare_logic``` function (above, line 12),
    and declare your rules using ```Rule.``` (e.g., with IDE code completion)
 
    b. After opening your database, call ```activate```
    to register your rules, and establish Logic Bank as
    a listener for SQLAlchemy ```before_flush``` events
    
    
 2. Your application operates as usual: makes calls on `SQLAlchemy` for inserts, updates and deletes
    and issues `session.commit()`

    - By bundling transaction logic into SQLAlchemy data access, your logic
  is automatically shared, whether for hand-written code (Flask apps, APIs)
  or via generators such as Flask AppBuilder
      

 3. The **Logic Bank** engine handles SQLAlchemy `before_flush` events on
`Mapped Tables`, so executes when you issue ```session.commit()```
    

 4. The logic engine operates much like a spreadsheet:
    - **watch** for changes at the attribute level
    - **react** by running rules that referenced changed attributes, which can
    - **chain** to still other attributes that refer to
_those_ changes.  Note these might be in different tables,
providing automation for _multi-table logic_

Logic does not apply to updates outside SQLAlchemy,
nor to SQLAlchemy batch updates or unmapped sql updates.

Let's see how logic operates on a typical, multi-table transaction.

### Logic Execution: Add Order - Watch, React, Chain

<figure><img src="images/check-credit.png"></figure>


The `add_order` example illustrates how
__Watch / React / Chain__ operates to
check the Credit Limit as each OrderDetail is inserted:

1.  The `OrderDetail.UnitPrice` (copy, line 49) references Product, so inserts cause it to be copied
    
2.  `Amount` (formula, line 48) watches `UnitPrice`, so its new value recomputes `Amount`
    
3.  `AmountTotal` (sum, line 46) watches `Amount`, so `AmountTotal` is adjusted (more on adjustment, below)
    
4.  `Balance` (sum, line 43) watches `AmountTotal`, so it is adjusted
    
5.  And the Credit Limit constraint (line 40) is checked (exceptions are raised if constraints are violated, and the transaction is rolled back)
    
All of the dependency management to see which attributes have changed,
logic ordering, the SQL commands to read and adjust rows, and the chaining
are fully automated by the engine, based solely on the rules above.

### Spreadsheet-like Automatic Reuse
Just as a spreadsheet reacts
to inserts, updates and deletes to a summed column,
rules automate _adding_, _deleting_ and _updating_ orders.
This is how 5 rules represent the same logic as 200 lines of code.

Check out more examples:
* [**Ship Order**](../../wiki/Ship-Order) illustrates *cascade*, another form of multi-table logic
* [**Banking**](../../wiki/Sample-Project---Banking) is a complex transaction using the command pattern

### Scalability: Automatic Prune / Optimize logic
Scalability requires more than clustering - SQLs must be pruned
and optimized.  For example, the balance rule:
* is **pruned** if only a non-referenced column is altered (e.g., Shipping Address)
* is **optimized** into a 1-row _adjustment_ update instead of an
expensive SQL aggregate

For more on how logic automates and optimizes multi-table transactions,
[click here](../../wiki#scalability-automatic-pruning-and-optimization).


## An Agile Perspective
The core tenant of agile is

    Working software, driving collaboration, for rapid iterations

Here's how rules can help.

#### Working Software _Now_
The examples above illustrate how just a few rules can replace 
[pages of code](examples/nw/logic/legacy).

#### Collaboration: Running Screens - Automatic Basic Web App

Certainly business users are more easily able to
read rules than code.  But still, rules are
pretty abstract.

Business users relate best to actual working pages -
_their_ interpretation of working software.
The [fab-quick-start](https://github.com/valhuber/fab-quick-start/wiki)
project enables you to build a basic web app in minutes.

<figure><img src="images/fab.png"></figure>

This project has already generated such an app, which you can run
once you've finished the Installation process, below.

#### Iteration - Automatic Ordering
Rules are _self-ordering_ - they recognize their interdependencies,
and order their execution and database access (pruning, adjustments etc)
accordingly.  This means:

* order is independent - you can state the rules in any order
and get the same result

* maintenance is simple - just make changes, additions and deletions,
the engine will reorganize execution order and database access, automatically


# Installation
First, follow the instructions to verify / install Python, then install Logic Bank.

### Python Installation

The first section below verifies whether your Python environment is current.
The following section explains how to install a current Python environment.

#### Verify Pre-reqs: Python 3.8, virtualenv, pip3
Ensure you have these pre-reqs:
```
python --version
# requires 3.8 or higher (Relies on `from __future__ import annotations`, so requires Python 3.8)

pip --version
# version 19.2.3 or higher... you might be using pip3

pyenv --version
# 1.2.19 or higher
```
#### Install Python (if required)
If you are missing any, install them as described here.  Skip this step if your pre-reqs are fine.

To install Python:

* Python3.8 

   * Run the windows installer
      * Be sure to specify "add Python to Path"
   * On mac/Unix, consider [using homebrew](https://brew.sh/), as described
[here](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)
   
* virtualenv - see [here](https://www.google.com/url?q=https%3A%2F%2Fpackaging.python.org%2Fguides%2Finstalling-using-pip-and-virtual-environments%2F%23creating-a-virtual-environment&sa=D&sntz=1&usg=AFQjCNEu-ZbYfqRMjNQ0D0DqU1mhFpDYmw)  (e.g.,  `pip install virtualenv`)
   * on PC, see [these instructions](https://pypi.org/project/pyenv-win/)

* An IDE - optional - any will do (I've used [PyCharm](https://www.jetbrains.com/pycharm/download) and [VSCode](https://code.visualstudio.com), install notes [here](https://github.com/valhuber/fab-quick-start/wiki/IDE-Setup)), though different install / generate / run instructions apply for running programs.

Issues?  [Try here](https://github.com/valhuber/fab-quick-start/wiki/Mac-Python-Install-Issues).


### Install LogicBank
This procedure installs the Logic Bank source code, including
examples you can explore.

> To use Logic Bank in your own project: `pip install LogicBank`

In your IDE or Command Line:

```
# optionally fork, and then (WARNING - remove hyphens if you download the zip)
git clone https://github.com/valhuber/LogicBank.git
cd LogicBank
# windows: python -m venv venv
virtualenv venv
# For windows: .\venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
```
> **Warning -** if you just download the zip, *be sure* to remove the hyphen from the name.

> **Warning -** if you use an IDE, be sure to activate the virtual environment, and verify you are running a proper version of Python.

### Verify and Run

#### Run the `nw/tests`
Run the `nw/tests` programs under your IDE or the
command line; start with `test_add_order` and `test_upd_order_shipped,`
and see the [walk-throughs here](../../wiki/home#logic-execution-watch-react-chain).
The tests use ```unittest``` - you can run them as follows:

```
cd examples/nw/tests
python -m unittest test_add_order.py
python test_add_order.py  # or, run it like this

python -m unittest discover -p "test*.py"  # run all tests
```

> Note: the console **log** depicts logic execution
>
> Log lines are long - consider copying them to a text
> editor to view with / without word wrap
> 
> Or, run in an IDE - they look [like this](../../wiki/home#debugging-standard-debugger-logic-logging).

#### Optional - Run `basic_web_app`
Flask App Builder is based on SQLAlchemy, so it can integrate  Logic Bank as
[described here](../../wiki/Flask-App-Builder-Integration).  The project contains a
pre-built sample you can run:

```
cd LogicBank
cd examples/nw/basic_web_app
python run.py
```
You then start the app (use **new window**) with
[`http://0.0.0.0:8080`](http://0.0.0.0:8080), or try

* [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/)
* [`http://127.0.0.1:8080/`](http://127.0.0.1:8080/)

> **Login** (upper right): user = admin, password = p

You can
1. Navigate to Order 11011 (a _multi-page_ web app)
    * Click **Menu > Customer List** 
    * Click the **magnifying glass** for the first customer
    * Click the **List Order tab**
    * Click the **magnifying glass* for Order **11011**
2. Click Edit so you can make changes
3. Change the Shipped Date
4. Click save
5. Verify logic enforcement
    * The web app has been [configured](../../wiki/Flask-App-Builder-Integration) to activate the rules
    * The logic for this update [is interesting](../../wiki/Ship-Order) -
    check out the console log

## Next Steps

### Run the Tutorial

First, run the [**10 minute Tutorial**](../../wiki/Tutorial).
You will see how to create, run and debug a rule in a simple, running example.

### Explore Sample Transactions

Then, check out the [**Examples**](../../wiki/Examples) - note the **navigation bar** on the right.  Key samples:
* [**Ship Order**](../../wiki/Ship-Order) illustrates *cascade*, another form of multi-table logic
* [**Allocation**](../../wiki/Sample-Project---Allocation) illustrates *extensibility*,
providing a reusable pattern for a *provider* to allocate
to a set of *recipients*
* [**Banking**](../../wiki/Sample-Project---Banking) is a complex transaction using the command pattern
* [**Referential Integrity**](../../wiki/Referential-Integrity) illustrates referential integrity support


A good way to proceed is to
* Clear the log
* Run the test
* Review the log, and the rules that drove the processing


### Articles
There a few articles that provide some orientation to Logic Bank:
* [Extensible Rules](https://dzone.com/articles/logic-bank-now-extensible-drive-95-automation-even) - defining new rule types, using Python
* [Declarative](https://dzone.com/articles/agile-design-automation-how-are-rules-different-fr) - exploring _multi-statement_ declarative technology
* [Automate Business Logic With Logic Bank](https://dzone.com/articles/automate-business-logic-with-logic-bank) - general introduction, discussions of extensibility, manageability and scalability
* [Agile Design Automation With Logic Bank](https://dzone.com/articles/logical-data-indendence) - focuses on automation, design flexibility and agile iterations

### See also the [LogicBankExamples](https://github.com/valhuber/LogicBankExamples) project

The `Logic Bank Examples` [(setup instructions here)](../../wiki/Sample-Project---Setup)
contains the same examples, but _not_ the `logic_bank` engine source code.
It uses the logic engine via `pip install`, as you would for your own projects:

```
pip install logicbank
```
> This is **not required here**, and requires the same
> pre-reqs noted above



# Project Information

<figure><img src="images/logic-bank-project.png"></figure>

#### What's in the project
Logic Bank consists of:

* Several test database systems - `nw,`  `banking`,
  `referential_integrity` and `payment_allocation`;
these contain

    * [Databases](examples/nw/db) sqlite (no install required) and models

    * [Test folders](examples/nw/tests) that run key transactions - just run the scripts
(note the logs)

    * [Flask AppBuilder apps](examples/nw/basic_web_app) (as described above)
    
    * [Logic](examples/nw/logic) - rules (and for `nw`,
    the manual `legacy` code for contrast to rules)
    
* The `nw` sample illustrates comparisons of Business logic, both
[by code](examples/nw/logic/legacy) and by rules (shown above).

* The `logic_bank` engine source code


#### Status: Running, Under Development
Functionally complete, 9/29/2020, tested for 2 databases.

Incubation - ready to explore and provide feedback
on general value, and features.

#### Internals

To explore:

* Click [here](../../wiki/Explore-Logic-Bank)
    for install / operations procedures
    
* Click [here](../../wiki/Logic-Walkthrough) for a
    short overview of internal logic execution

#### Acknowledgements
There are many to thank:
* Tyler Band, for testing and the Banking example
* Max Tardiveau, for testing
* Nishanth Shyamsundar, for PC testing
* Michael Holleran, for collaboration
* Mike Bayer, for suggestions on leveraging Python typing
* Achim Götz, for reporting an issue in FAB Quick Start use of Logic Base
* Gloria, for many reviews... and golden patience
