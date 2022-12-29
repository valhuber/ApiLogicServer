
## JSON:API - Related Data, Filtering, Sorting, Pagination

The `ApiLogicServer create` command creates an API Logic Project that implements your API.  No additional code is required.

* You get an __endpoint for each table__, with __CRUD support__ - create, read, update and delete.

* The API also supports __related data access__, based on relationships in the models file (typically derived from foreign keys).


&nbsp;

  > **Key Take-away:** instant *rich* APIs, with filtering, sorting, pagination, related data access and swagger.  **Custom App Dev is unblocked.**

&nbsp;

## Automatic Swagger Generation

API creation includes automatic swagger generation.  

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/swagger.png?raw=true"></figure>

Start the server, and open your Browser at `localhost:5656`.  Or, explore the sample app [running at PythonAnyWhere](http://apilogicserver.pythonanywhere.com/api){:target="_blank" rel="noopener"}.

&nbsp;

## Provider-Defined vs. Consumer-Defined

JSON:APIs are interesting because they are _Consumer-Defined,_ to __reduce network traffic__ and __minimize organizational dependencies.__

Contrast these to Provider-Defined APIs.  These can be simpler for interrnal users, whose needs can be determiend.

But for a wider class of consumers (e.g., business partenrs), providers typically cannot predict consumer needs.  Consumers often resort to making multiple calls to obtain the data they need, or invoke APIs that return too much data.  These can increase network traffic.

&nbsp;

## Swagger to construct API calls

Provider-defined API calls typically have more/longer arguments.  To facilitate creating invoking APIs, use swagger to obtain the url.

  > Tip: use Swagger to debug your API parameters, then use the copy/paste services to use these in your application.

&nbsp;

## Logic Enabled

API Logic Server is so-named because all the update APIs automatically enforce your [business Logic](../Logic-Why){:target="_blank" rel="noopener"}.

  > **Key Take-away:** your API encapsulates your logic, factoring it out of APIs for greater concisenss and sharing / consistency

&nbsp;

## Examples

The [Behave Tests](../Behave){:target="_blank" rel="noopener"} provide several examples of using the API.  You can [review them here](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype_nw/test/api_logic_server_behave/features/steps/place_order.py).


&nbsp;

## Key Usage: custom apps

The automatic Admin App is useful, but most systems will require custom User Interfaces.  Use your favorite framework (eg, React).
