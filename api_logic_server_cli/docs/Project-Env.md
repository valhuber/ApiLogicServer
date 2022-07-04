
# Virtual Environment
This section applies only to `pip` installs.  Docker based installs eliminate such environment issues, and are therefore recommended.

You created a virtual environment when you installed ApiLogicServer.  This ```venv``` will work for all of your created ApiLogicServer projects, or you can use a per-project ```venv``` as described below.

Alternatively, you can create a self-contained virtual environment for each project.
The created project contains a ```requirements.txt``` used to create a [virtual environment](https://docs.python.org/3/library/venv.html).
You can create it in the usual manner:

```sh
cd ApiLogicProject
python3 -m venv venv       # may require python -m venv venv
source venv/bin/activate   # windows venv\Scripts\activate
python3 -m pip install -r requirements.txt
```

> The install sometimes fails due on machines with an older version of `pip`.  If you see a message suggesting you upgrade  `pip` , do so.

> If VSCode does not find your `venv`, you can [specify it manually](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter) using `Python: Select Interpreter`

For more information, see [Work with Environments](https://code.visualstudio.com/docs/python/environments#_work-with-environments).