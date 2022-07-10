While a standards-based API is a great start, sometimes you need custom endpoints tailored exactly to your business requirement.  Initially the API exposes all your tables as collection endpoints.  You can add additional endpoints by editing ```expose_services.py```, as illustrated below. 


## Use Flask

You will observe the standard "Hello World" endpoint, which directly uses Flask.  These do not appear in Swagger.

&nbsp;

## Use SAFRS: endpoint with swagger

 You can create these as shown below, where we create an additional endpoint for `add_order`.
 
 For more on customization, see [SAFRS Customization docs](https://github.com/thomaxxl/safrs/wiki/Customization).

To review the implementation, and how to use the debugger for your custom endpoints: 

1. Open **Explorer > api/customize_api.py**:
3. Set the breakpoint as shown
4. Use the swagger to access the `ServicesEndPoint > add_order`, and
   1. **Try it out**, then 
   2. **execute**
5. Your breakpoint will be hit
   1. You can examine the variables, step, etc.
6. Click **Continue** on the floating debug menu (upper right in screen shot below)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>

