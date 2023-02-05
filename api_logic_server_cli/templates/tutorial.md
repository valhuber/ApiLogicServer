# Tutorial

<details markdown>

&nbsp;

<summary>Welcome to this Tutorial</summary>

Use this Tutorial for a quick tour of API Logic Server - automated project creation from a database, and customization including logic.  As a reference background, a "native" hand-code Flask app is provided for experimentation.

The Key Technology Concepts (at end) is an inventory of essential skills for creating Flask/SQLAlchemy systems.  Each are illustrated here.

These projects all use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/).  Other databases are also provided in Next Steps.

</details>

&nbsp;

<details markdown>

&nbsp;

<summary>1. Basic App: Flask / SQLAlchemy -- flexible, but slow</summary>

This illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project does not provide:

* an API endpoint for each table

* a User Interface

* any security, or business logic (multi-table derivations and constraints).

Execute using the Run Configuration, and test with `cURL`.  The relevant code is `api/end_points.py`.

<details markdown>

<summary> Show me how </summary>

&nbsp;

To run the basic app:

1. Click Run Configurations, and the green button to start the server

2. Copy the `cURL` text, and paste it into the `bash`/`zsh` window

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/tutorial/1-basic-app.png?raw=true"></figure>

</details>

</details>

&nbsp;

</details>


<details markdown>

