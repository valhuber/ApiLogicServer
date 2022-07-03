
## What - Declare Spreadsheet-like Rules - 40X More Concise
So, what _is_ declarative logic.  Let's review a representatively complex example.

### Current Approach - Simple Cocktail-Napkin Spec Explodes into Massive Legacy Code

Let's imagine we have a "cocktail napkin spec" shown (in blue) in the diagram below.  How might we enforce such logic?

* In UI controllers - this is the most common choice.  It's actually the worst choice, since it offers little re-use, and does not apply to non-UI cases such as API-based application integration.
* Centralized in the database - in the past, we might have written triggers, but a modern software architecture centralizes such logic in an App Server tier.  If you are using an ORM such as SQLAlchemy, you can _ensure sharing_ with `before_flush` events as shown below

After we've determined _where_ to put the code, we then have to _write_ it.  Our simple cocktail napkin specification explodes into a massive amount of legacy code:

<figure><img src="https://github.com/valhuber/LogicBank/raw/main/images/overview/rules-vs-code.png"></figure>

### Logic is 40x more concise
Logic Bank introduces rules that are 40X more concise than legacy code.
The 5 rules below (lines 40-49) express the same logic as 200 lines of code [**(see them here)**](https://github.com/valhuber/LogicBank/wiki/by-code).  That's because rules are all about "what"
-- spreadsheet-like expressions that automate the tedious "how":

<figure><img src="https://github.com/valhuber/ApiLogicServer/wiki/images/logic/5-rules-cocktail.png?raw=true"></figure>
