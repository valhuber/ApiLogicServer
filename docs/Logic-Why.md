Logic automation is a _unique_ answer to a significant and unaddressed problem - the automation gap:

> For transaction systems, backend multi-table constraint and derivation logic is often nearly *half* the system.  It's the iceberg under the surface of the API.

> While there are varying degrees of front-end "low code" automation, **back-end logic is not addressed** by conventional approaches of *"your code goes here"*.

API Logic Server uses [Logic Bank](https://github.com/valhuber/logicbank#readme) to automate update transaction logic - multi-table derivations, constraints, and actions such as sending mail or messages.

Logic consists of both:

* **Rules - 40X** more concise using a spreadsheet-like paradigm, and

* **Python - control and extensibility,** using standard tools and techniques

&nbsp;

## Why Rules - Velocity, Quality, Agility, Performance

If you've coded backend database logic - multi-table derivations and constraints -
you know how much work it is, and how tedious.  Whether you code it in
triggers and stored procedures, in ORM events, or UI controllers, it's a lot:
typically nearly half the effort for a database project.

It's also incredibly repetitive - you often get the feeling you're doing the same thing over and over.

And you're right.  It's because backend logic follows patterns of "what" is supposed to happen.
And your code is the "how".  

Declarative logic addresses this by automating the _why_ with spreadsheet-like rules that are 40x more concise than code.  Conciseness can obviously improve velocity, but ___declarative logic___ - automatically re-used, invoked, ordered and optimized - can dramatically improve quality and accelerate iteration / maintenance cycles:

| Concept | Rule Automation | Why It Matters|
| :--- |:---|:---|
| Re-use | Automatic re-use over all resources and actions | __Velocity / Conciseness:__ Eliminates logic replication over multiple UI controllers or services. |
| Invocation | Automatic logic execution, on referenced data changes |__Quality:__ Eliminates the _"code was there but not called"_ problem.<br><br>Rules are _active,_ transforming ‘dumb’ database objects into _smart_ business objects |
| Execution Order | Automatic ordering based on dependencies |__Maintenance:__ Eliminates the _"where do I insert this code"_ problem - the bulk of maintenance effort. |
| Dependency Management | Automatic chaining |__Conciseness:__ Eliminates the code that tests _"what's changed"_ to invoke relevant logic |
| Persistence | Automatic optimization |__Performance:__ Unlike Rete engines which have no concept of old values, transaction logic can prune rules for unchanged data, and optimize for adjustment logic based on the difference between old/new values.  This can literally result in sub-second performance instead of multiple minutes, and can be tuned without recoding.. |

Logic Bank was designed to make the cocktail napkin spec _executable_.

### Metrics: 95% at 40X

In most transactional database systems, backend logic accounts for nearly half the code.

In past rule implementations addressing moderate-sized systems (typically consisting of 50-1000 tables):

* rules automate well over 95% of the logic.

* rules are 40x more concise than code.  We'll explore a typically complex multi-table transaction below; [here's the code vs. rules comparison](https://github.com/valhuber/LogicBank/wiki/by-code).

### Complexity: automate 95%, standard language for rest

The rule language is simple, by design.  Here is a [summary of the rule types](../Logic) - under a dozen.  The rules are deceptively simple, achieving power through chaining.

So, how do rules address complexity?

* The underlying design objective is _not to automate every problem_.  That would lead to a large set of rules that is difficult to understand and use.


* Instead, the focus is on _value,_ by automating the __most common__ cases (the 95%), with value noted above for quality, agility and performance.

While 95% is certainly remarkable, it's not 100%.  Automating most of the logic is of no value unless there are provisions to address the remainder.

That provision is standard Python, provided as standard events.  This will be typically be used for non-database oriented logic such as files and messages, and for extremely complex database logic.

&nbsp;