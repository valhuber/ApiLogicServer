While a standards-based API is a great start, sometimes you need custom endpoints tailored exactly to your business requirement.  You can create these as shown below, where we create an additional endpoint for `add_order`.

## Customize the API with ```expose_services.py```: add RPCs, Services

Initially the API exposes all your tables as collection endpoints.  You can add additional endpoints by editing ```expose_services.py```, as illustrated by the Add Service example.  For more on customization, see [SAFRS Customization docs](https://github.com/thomaxxl/safrs/wiki/Customization).

To review the implementation: 

1. Open **Explorer > api/customize_api.py**:
3. Set the breakpoint as shown
4. Use the swagger to access the `ServicesEndPoint > add_order`, and
   1. **Try it out**, then 
   2. **execute**
5. Your breakpoint will be hit
   1. You can examine the variables, step, etc.
6. Click **Continue** on the floating debug menu (upper right in screen shot below)

<figure><img src="https://github.com/valhuber/ApiLogicServer/raw/main/images/docker/VSCode/nw-readme/customize-api.png"></figure>

