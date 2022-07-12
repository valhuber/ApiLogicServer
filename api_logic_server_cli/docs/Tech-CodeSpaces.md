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


__3. Configure the Admin App__ for your URL:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/configure-admin.png?raw=true"></figure>

__4. Configure a Port__

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/create-port.png?raw=true"></figure>

__5. Start the Server__ using the provided Launch Configuration = `ApiLogicServer`


__6. Open the Browser__

Click the globe, below.  This should start your Browser, and the links on the left (Customer etc) should return data.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/open-port.png?raw=true"></figure>


&nbsp;

## Status

On 7/11/2022, the project status is as folows:

### Admin App Working

Got Admin App working using procedure above:

* added port 5656
* started server using __Launch Configuration__ = `ApiLogicServer`, and 
* click __port > globe__ to start Browser.

> Note: __port > copy local address__ = `https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/`.

### cURL working

cURL is working, providing more evidence of remote connectivity:


```bash

  curl -o ~/Desktop/curl-out.txt 'https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/api/OrderDetail/1040?include=Product,Order&page[limit]=1' --globoff -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5'  -H 'Referer: https://valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev/admin-app/index.html' -H 'authorization: Bearer xxxx' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'
```


### Unable to configure run swagger

The home page of the running Admin App has a link (item 2) to run Swagger.  In the test above, you can click it to see the Swagger web page, but __Try it Now__ fails due to a bad __host__ address.  It's running properly on [pythonanywhere](http://apilogicserver.pythonanywhere.com/admin-app/index.html){:target="_blank" rel="noopener"}.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/invalid-host.png?raw=true"></figure>

To address this, I created another Launch Configuration `ApiLogicServer-swagger` to specify __host__  (it's argument 1), using the "copy local address" from above: `valhuber-tutorial-apilogicproject-wrv7gj45fgxq6-5656.githubpreview.dev`.

Starting the server with this Launch Configuration fails with:

```bash
  fails with: OSError: [Errno 99] Cannot assign requested address 
```

It is particularly surprising, since the Launch Configuration `ApiLogicServer` succeeds as noted above.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/git-codespaces/cannot-assign-server.png?raw=true"></figure>