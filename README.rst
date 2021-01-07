Python Rules - Logic for SQLAlchemy
===================================

This package enables you to declare rules that govern SQLAlchemy
update transaction logic (multi-table derivations, constraints,
and actions such as sending mail or messages).

Logic is stated in Python, and is over an **40X
more concise than code.**


Features
--------

Logic is declared in Python (example below), and is:

- **Extensible:** logic consists of rules (see below), plus standard Python code

- **Multi-table:** rules like ``sum`` automate multi-table transactions

- **Scalable:** rules are pruned and optimized; for example, sums are processed as *1 row adjustment updates,* rather than expensive SQL aggregate queries

- **Manageable:** develop and debug your rules in IDEs, manage it in SCS systems (such as `git`) using existing procedures


Example:
--------
The following 5 rules represent the same logic as 200 lines
of Python:

.. image:: https://github.com/valhuber/LogicBank/raw/main/images/example.png
    :width: 800px
    :align: center



To activate the rules declared above:

.. code-block:: Python

    LogicBank.activate(session=session, activator=declare_logic)

Depends on:
-----------
- SQLAlchemy
- Python 3.8


More information:
-----------------
The github project includes documentation and examples.


Acknowledgements
----------------
Many thanks to

- Tyler Band, for testing and the Banking sample
- Max Tardiveau, for testing
- Nishanth Shyamsundar, for testing
- Achim Götz, for design collaboration



Change Log
----------

0.0.6 - Initial Version

0.0.7 - Class Name can differ from Table Name

0.0.8 - Much-reduced pip-install dependencies

0.0.9 - Hybrid attribute support, old_row example

0.1.0 - Hybrid attribute support, bug fix

0.1.1 - `Allocation <https://github.com/valhuber/LogicBank/wiki/Sample-Project---Allocation>`_ example -
allocate a payment to a set of outstanding orders

0.2.0 - Minor design refactoring of allocation

0.3.0 - Include logic_bank.extensions (allocation), constraint exceptions raised as ConstraintExceptions

0.4.0 - Eliminate "engine" from runtime, to facilitate use in servers.  Rework nw tests to centralize open logic in setup().

0.5.0 - Support for `Referential Integrity <https://github.com/valhuber/LogicBank/wiki/Sample-Project---Allocation>`_,
with examples.

0.5.1 - Support domain object constructors with complex (side effects)
__init__ behavior; use row_mapper.column_attrs (not all_orm_descriptors)
to avoid 'flush already in progress' when using flask_sqlalchemy

0.6.0 - Support for

- `Rule Extensibility <https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility>`_

   - e.g., for auditing

- Generic early events: ``early_row_event_all_classes`` (see Rule Extensibility link above)

   - e.g., for time/date stamping

- New LogicRow functions (see Rule Extensibility link above):

   - are_attributes_changed

   - set_same_named_attributes

- Minor rename of logic class in ``nw``.  Some screen shots may still show the old name (`rules_bank.py`) instead of `logic.py`.

- Bug Fix: (normal) row events weren't firing (other events - early and commit events - were fine)

0.7.0 - `Custom Exceptions <https://github.com/valhuber/LogicBank/wiki/Custom-Constraint-Handling>`_, Improved docstrings, samples (and Tutorial) reorganized into ``examples`` folder

0.8.0 - `Custom Exceptions <https://github.com/valhuber/LogicBank/wiki/Custom-Constraint-Handling>`_, callback signature **changed** to include
additional parameters

0.9.0 - Add logicRow.get_derived_attributes, which
can be used to enforce behaviors such as
`Unalterable Derivations <https://github.com/valhuber/LogicBank/wiki/Rule-Extensibility#unalterable-derivations>`_
