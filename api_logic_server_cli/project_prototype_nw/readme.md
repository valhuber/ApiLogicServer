# Welcome to API Logic Server

Choose how you want to get started, below:

&nbsp;

<details markdown>

<summary> Quick Tour - API Logic Server in a Nutshell </summary>

&nbsp;

1. Execute the __Setup and Run__ procedure below 

2. **Start the Server**

<details markdown>

<summary> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Show me how <br><br></summary>

&nbsp;

To run the ApiLogicProject app:

1. Start the Server:

    1. Click **Run and Debug**
    2. Use the dropdown to select **ApiLogicServer - No Security (e.g., for behave tests)**, and
    3. Click the green button to start the server
<br><br>

2. Start the Browser at localhost:5656 by **clicking the url shown in the console log.**

<figure><img src="https://github.com/ApiLogicServer/Docs/blob/main/docs/images/tutorial/2-apilogicproject-nutshell.png?raw=true"></figure>


</details>


3. Explore the automatic **Admin App, and Swagger**

    * To run Swagger: **Home page >> 2. API, with oas/Swagger**<br><br>

4. Explore the API
    * **Automatic API:** `api/expose_api_models.py`
    * **Custom Endpoint:** `api/customize_api.py` - see `add_order()`<br><br>


5. Review `logic/declare_logic.py`
    * Set a breakpoint at **breakpoint here**<br><br>

6. Explore **Custom APIs and Logic Execution / Debugging**
    * In swagger: **POST ServicesEndPoint/add_order > Try it out**
    * At the breakpoint, observe the 
        * **Debugger State** -- row attributes, etc
        * **Logic Log** -- line for each rule fire, showing row, with indents for chaining

</details>

&nbsp;

<details markdown>

<summary> API Logic Server Tutorial </summary>

&nbsp;

_Establish Your Python Environment_ to run the Tutorial, as follows:

1.  Execute the __Setup and Run__ procedure below, then 
2. [Open the Tutorial](Tutorial.md)

The standard API Logic Project Readme follows, below.

</details>

&nbsp;
