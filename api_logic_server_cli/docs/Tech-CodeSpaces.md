[CodeSpaces](https://github.com/features/codespaces){:target="_blank" rel="noopener"} is a GitHub project that enables you to use VSCode in your Browser to develop on rapidly deployed docker containers.  It's quite remarkable.  

Api Logic Server has been explored under CodeSpaces, and is starting to run.  This is a __work in progress.__

Here is the [test project](https://github.com/valhuber/Tutorial-ApiLogicProject#readme){:target="_blank" rel="noopener"}.

&nbsp;

## Configuring the project

Here are some instructions you can use to explore API Logic Server running under CodeSpaces.

__1. Signup for CodeSpaces__ - use [this link](https://github.com/features/codespaces/signup){:target="_blank" rel="noopener"}, where you already have a GitHub account

__2. Get the Tutorial Project__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-tutorial-repo.png
?raw=true"></figure> 

__3. Configure a Port__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port.png?raw=true"></figure>

__4. Configure the `Codespaces-ApiLogicServer` launch configuration__ (see above)

__5. Start the Server__ using the provided Launch Configuration = `Codespaces-ApiLogicServer`

__6. Open the Browser__

Click the globe, below.  This should start your Browser, and the links on the left (Customer etc) should return data.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-port.png?raw=true"></figure>


&nbsp;

## Status - Running, still experimental

On 7/24/2022, the Admin App is working, cURL is working, and Swagger is working.  While still experimental, this looks very promising.
