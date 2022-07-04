# Python for a Java Developer

I quite like Python.  I've used assembler, PL/1, and Java.  Python (particularly with good IDEs) is my favorite.

Though, there were some surprises I wish I'd been told about.  So, here you go.

## Basics

You'll discover these soon enough:

1. Indents vs. braces - obvious, but the real implication is that _you need an IDE_, because they keep track of indents (vs. spaces).  I've used PyCharm and VSCode, both are wonderful: great editors, debuggers.

2. Non-typed - well-known, but you can (should) use [Type Hints](https://docs.python.org/3/library/typing.html) for clarity, and code completion.

3. CLI - Python includes great tools for making Command Line Interfaces, like Click.  A little fiddly, you might want to have a look at [these examples](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/cli.py) (near the end)

4. Modules - are not packages.  There is a magic file `__init.py__` that makes a directory into a module.

&nbsp;

## Pip, environments and PythonPath

Pip is how to lead libraries (packages) - not by setting up folder.  It's great, but quickly leads to Pyton's version of "DLL Hell" where libraries interfere from different projects.  So, the best practice is to set up [Virtual Environments](https://docs.python.org/3/library/venv.html?highlight=virtual%20environment).

A related issue is loading classes / modules at runtime.  Be clear on your `PythonPath`.  And, be aware the some IDEs (PyCharm is one) provide super-friendly support to simplify things by setting this automatically.  Which is nice, until you discover that a program that runs in the IDE fails outside it.  Days of fun.

&nbsp;

## Import is a 4 letter word

Oy, where do I start.

### Executable - non-class code runs on import

First, imports are executable... which means nothing to a Java developer.  The key underlying fact is that Python does not require all code to be in a class.

### Imports often fail to compile

I still do not understand where Python and the IDE figure out what I can import.  You'll find lots of Stack Overflow articles on imports (e.g., sibling imports).

For me, it usually degenerates into a trial and error exercise.  You might find [sibling imports](https://github.com/valhuber/SiblingImports) a useful project to fiddle with.

### Circular Imports

I understand that Python's 1-pass nature means your imports have to be in a certain order to work.  I have spent days battling this.  I hope you have better luck, but at least you have a heads up.  As always, introduce changes in small numbers to avoid having lots of potential problems.

&nbsp;

## Mac Installs

If you like imports, you'll love Mac installs.

Way back when, Apple installed Python.  Python 2.  Which is very old - Python3 is now the standard.

But Mac was stuck with Python == Python2.  Which probably gets you the wrong version.

I guess as folks dealt with this, there arose many ways of installing - brew, the Python installer, maybe others.

And that was further compounded by alternate ways of running Pip, things like `venv`.

As I flailed, I tried many of them.  The end result was that I finally concluded I did not know what I was running.

So, and __I hope you avoid this__, I wound having to re-install my computer.  Just wow.

Where I wound up was simple:

* stick with the Python.org installer
* I am not using `venv` or `pip` directly; I use them with Python(3) so I know they are consistent:

```
python3 -m venv venv  # of course, it *might* be Python, not Python3 (!)
python3 -m pip install ApiLogicServer
```