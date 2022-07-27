
## Project Structure

When you create an ApiLogicProject, the system creates a project like this that you customize in your API:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/generated-project.png?raw=true"></figure>

[Explore the Tutorial Project](https://github.com/valhuber/Tutorial-ApiLogicProject#readme), and observe that the projects are rather small.  That is because the syste creates _models_ that define _what, not now_.  Explore the project and you will find it easy to understand the API, data model, app and logic files.

Note the entire project is file-based, which makes it easy to perform typical project functions such as source control, diff, merge, code reviews etc.



## Customizing ApiLogicProjects

You will typically want to customize and extend the created project.  Edit the files described in the subsections below.

The 2 indicated files in the tree are the Python files that run for the Basic Web App and the API Server.

Projects are created from a [system-supplied prototype](https://github.com/valhuber/ApiLogicServer/tree/main/prototype).  You can use your own prototype from git (or a local directory) using the ```from_git``` parameter.


## Project Architecture

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/Architecture.png?raw=true"></figure>

ApiLogicServer creates a standard Flask-based 3-tier architecture:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) enables you to write custom web apps, and custom api end points

    * ApiLogicServer automatically creates an Admin App using
[safrs-react-admin](https://github.com/thomaxxl/safrs-react-admin), useful for back-office admin access and prototyping

* [SAFRS](https://github.com/thomaxxl/safrs/wiki) provides the API, which you can use to support mobile apps and internal / external integration

* [SQLAlchemy](https://sqlalchemy-utils.readthedocs.io/en/latest/) provides data access.

* [Logic Bank](https://github.com/valhuber/logicbank#readme) listens for updates, and applies your declared logic, for both API and web app updates.

&nbsp;
