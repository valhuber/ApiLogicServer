
__1. Create your project__

```
cd ApiLogicServer          # your install folder
source venv/bin/activate   # windows venv\Scripts\activate

ApiLogicServer create   # Return to accept default project name, db

```


__2. Do *not* create the `venv` outside PyCharm__


__3. Open the ApiLogic Project__

__4. Create a new Virtual Environment using PyCharm defaults__

PyCharm will ask you to configure a Python Interpreter.  Do so as shown below.

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/PyCharm/PyCharm-create-venv.png"></figure>


__5. `pip` install__

Some versions of Pycharm automatically load your dependencies, others do not.  But it's simple to load them using the terminal window:

```bash
source venv/bin/activate          # windows: venv\Scripts\activate
pip install -r requirements.txt   # the requirements.txt file was pre-created by ApiLogicServer
```

> The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.



__6. Run the pre-configured `run` launch configuration__

Some versions of Pycharm may require that you update the Launch Configuration(s) to use your `venv`.