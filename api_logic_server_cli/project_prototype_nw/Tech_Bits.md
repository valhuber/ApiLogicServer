&nbsp;&nbsp;&nbsp;

# Tech Bits

While the focus of API Logic Server is to create projects, it is also a great source of examples.  Whether you are learning Python, or teaching it, it's a great start to have samples, in a running project, that you can experiment with.

| Area | Skill | Example    | Notes   |
|:---- |:------|:-----------|:--------|
| __SQLAlchemy__ | Data Model Classes | [```database/customize_models.py```](database/customize_models.py) |   |
|  | Read / Write | [```api/customize_api.py```](api/customize_api.py) | see `def order():`  |
|  | Multiple Databases | [```database/bind_databases.py```](database/bind_databases.py) |    |
|  | Events | [```security/system/security_manager.py```](security/system/security_manager.py) |    |
| __Alembic__ | Schema Changes | [```database/alembic/readme.md```](database/alembic/readme.md) |   |
|  | Read / Write | [```api/customize_api.py```](api/customize_api.py) | see `def order():`  |
| __Flask__ | End Point | [```api/customize_api.py```](api/customize_api.py) |  see `def order():` |
|  | Events | [```api/customize_api.py```](api_logic_server_run.py) |  see `flask_events` |
| __API__ | Read / Write | [```test/.../place_order.py```](test/api_logic_server_behave/features/steps/place_order.py) |   |
| __Config__ | Config | [```config.py```](config.py) |   |
|  | Env variables | [```config.py```](config.py) | os.getenv(...)  |
| __Behave__ | Testing | [```test/a.../place_order.py```](test/api_logic_server_behave/features/steps/place_order.py) |   |
| __Docker__ | Dev Env | [```.devcontainer/devcontainer.json```](.devcontainer/devcontainer.json) | See also "dockerFile":... |
|  | Containerize Project | [```devops/docker/build-container.dockerfile```](devops/docker/build-container.dockerfile) |  |