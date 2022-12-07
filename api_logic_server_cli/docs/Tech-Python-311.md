# Python 3.11

Requires `psycopg2-binary==2.9.5`.

Fails to run:

```
(venv) val@Vals-MPB-14 ApiLogicServer % ApiLogicServer welcome
Traceback (most recent call last):
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/bin/ApiLogicServer", line 33, in <module>
    sys.exit(load_entry_point('ApiLogicServer==6.4.3', 'console_scripts', 'ApiLogicServer')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/bin/ApiLogicServer", line 25, in importlib_load_entry_point
    return next(matches).load()
           ^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/metadata/__init__.py", line 198, in load
    module = import_module(match.group('module'))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/lib/python3.11/site-packages/api_logic_server_cli/cli.py", line 81, in <module>
    from create_from_model.model_creation_services import ModelCreationServices
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/lib/python3.11/site-packages/api_logic_server_cli/create_from_model/model_creation_services.py", line 21, in <module>
    from api_logic_server_cli.sqlacodegen_wrapper import sqlacodegen_wrapper
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/lib/python3.11/site-packages/api_logic_server_cli/sqlacodegen_wrapper/sqlacodegen_wrapper.py", line 22, in <module>
    from sqlacodegen_wrapper.sqlacodegen.sqlacodegen.codegen import CodeGenerator
  File "/Users/val/dev/servers/install/ApiLogicServer/venv/lib/python3.11/site-packages/api_logic_server_cli/sqlacodegen_wrapper/sqlacodegen/sqlacodegen/codegen.py", line 9, in <module>
    from inspect import ArgSpec
ImportError: cannot import name 'ArgSpec' from 'inspect' (/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/inspect.py)
(venv) val@Vals-MPB-14 ApiLogicServer % 
```