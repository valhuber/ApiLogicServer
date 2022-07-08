
Most of API Logic Server functionality derives from the data model classes created from your schema when you create your project with `ApiLogicServer create`.  In the example below:

* On the right are the created data model classes
* On the left are references to it from the Admin Web App `admin.yaml` model file that defines how the app behaves:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/model/relns-admin.png?raw=true"></figure>

Observe that:

1. A __class__ is created for each table.  The name (e.g. `OrderDetail`) is derived from the table name, but is capitalized and singlularized


2. The __table name__ is from your schema, this corresponds to a resource collection in the API


3. Relationships are created on the _one_ side of one-to-many relationships.  The __relationship name__ is the target class + "List", and is available in Python (`items = anOrder.OrderDetailList`).  These names are used in your UI admin apps, and your API


4. Relationships have 2 names; the __backref__ name is now the _many_ side refers to the _one" side (e.g., anOrder = anOrderDetail.order`)


Relationship names are also part of your API:

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/model/relns-api.png?raw=true"></figure>

> Each database has extensions which can introduce issues in model generation, so facilities are described in [Troubleshooting](Troubleshooting) to edit models and rebuild.
