# App Fiddle

<details markdown>

&nbsp;

<summary>Welcome to the Flask/SQLAlchemy "App Fiddle"</summary>

You've perhaps used JS Fiddle to explore JavaScript and HTML.  With the power of Codespaces, we can now provide a "fiddle" for a *complete application.*

Use this ***Application Fiddle*** to learn Flask/SQLAlchemy in Codespaces.  You have 3 running apps - execute them, explore the code, alter them (e.g., create endpoints, issue queries), use the debugger, etc.

The Key Technology Concepts (at end) is an inventory of essential skills for creating Flask/SQLAlchemy systems.  Each are illustrated here.

These projects all use the [Northwind Sample Database](https://apilogicserver.github.io/Docs/Sample-Database/).  Other databases are also provided in Next Steps.

Start with the first application - a Basic Flask/SQLAlchemy App.

Then, discover **API Logic Server** - an Open Source CLI to create executable projects, **instantly,** with a single command.  Its open source, and **open** technology: customize projects in your IDE, including unique spreadsheet like rules for logic and security - 40X more concise than manual code.

</details>

&nbsp;

<details markdown>

&nbsp;

<summary>1. Basic App: Flask / SQLAlchemy -- flexible, but slow</summary>

This illustrates a typical framework-based approach for creating projects - a minimal project for seeing core Flask and SQLAlchemy services in action.

Execute using the Run and Debug (*1. Basic App: Flask / SQLAlchemy*), and test with `cURL`.  The relevant code is `1. Basic_App/api/end_points.py`.

<details markdown>

<summary> Show me how </summary>

&nbsp;

To run the basic app:

1. Click **Run and Debug** (you should see *1. Basic App: Flask / SQLAlchemy*), and the green button to start the server

2. Copy the `cURL` text, and paste it into the `bash`/`zsh` window

3. When you have reviewed the result, stop the server

<figure><img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/1-basic-app.png?raw=true"></figure>

</details>

Frameworks are flexible, and leverage your existing dev environment (IDE, git, etc).  But the manual effort is time-consuming, and complex.  This minimal project **does not provide:**

* an API endpoint for each table

* a User Interface

* any security, or business logic (multi-table derivations and constraints).


</details>

&nbsp;

</details>


<details markdown>

