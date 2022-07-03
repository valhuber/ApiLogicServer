Under Construction.  

# Use Cases
The system automatically creates multi-page, multi-table applications as described in "Features", with typical usage as described below.

### Back Office Admin
Systems commonly include a number of "back office" admin apps that need to be usable, but do not warrant the time and cost of custom app development.  These are costly to build by hand.

Automatic creation of such apps eliminates the time and expense of such back office apps from your project.

### Prototyping / Agile Collaboration
It's a common observation that business users related poorly to technical documentation such as data model diagrams, but instantly related to running pages containing _their_ data.

API Logic Server can create these apps instantly, from just the data model.  Users are able to run the screens - incuding updates - and begin the collaboration process, such as:
* identify data model issues ("hey, wait, customers have more than 1 address")


* identify rules ("hmm, it needs to verify that balances do not exceed credit limits")

As such items are noted, you can update the data model, recreate, and iterate the design very rapidly since there is no cost to create the API or the UI.

### Complements Custom API-based Apps (Automatic API and Logic Reuse)

That said, it's common that you will need custom apps for complex functions, customer-facing branding, and so forth.

* Create these in your favorite technology (React, Angular, etc)


* Base them on the automatically created API, which handles not only data retrieval and update, but also enforces your [business logic](../Logic:-Rules-plus-Python), which dramatically reduces client app dev effort by factoring out business logic to the shared API.

# Features
Key features are described below.

### Multi-page

From your database, the system creates a page for each table, with a menu on the left.  Clicking a menu link shows list of rows, with:
1. Multi-Field Search
2. Pagination
3. Form transitions to "zoom" into the selected row (click the icon, or just the row)

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/multi-page.png?raw=true"></figure>


### Multi-table - 1:n, n:1 (automatic _predictive joins_)

The display page below is a multi-table page

1. 1:n (One to Many) - the data model defines a one-to-many foreign key relationship from a customer to orders; the orders are presented in a grid

   * Note the grid provides page transitions and pagination, as noted above


2. (n:1) Many to One - the data model defines a many-to-one foreign key relationship from an order to employee (salesrep); the system joins in the most likely field and displays it in the grid


<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/multi-table.png?raw=true"></figure>


### Lookup
On add and update pages, you can establish many-to-one relationships with a lookup.  In the example above, you can lookup the Employee (sales rep) for an Order, or the Product for an Order Detail, etc.  As for predictive joins, these are automatically created.

# Architecture - React, based on created logic-enabled API
The applications are Single Page React applications, acquiring data via the SAFRS JSON:API.  Recall updates are governed by rules.


# Customization

### Intelligent Default Creation
The system makes reasonable attempts to create useful applications
* automatic joins
* "favorite" fields are displayed first, such as field named `name`.
  * You can configure your favorite names when creating:
```
ApiLogicServer create --project_name=my-project \
                      --db_url=nw+ \
                      --favorites='nom nommes'
```
* non-favorites (such as `id`) can be identified with the `--non_favorites` argument; these are shown at the end

### Edit `admin.yaml`

While these defaults are useful in creating a recognizable application, you will want to control the display order, override labels and so forth.  You can specify such customizations by editing the `admin.yaml` file below.

This file is created initially by the system, so it's not necessary to learn the syntax in detail.  Instead, it's straight-forward to alter the file using your IDE or text editor.

  > Press Browser refresh to reload the application after you make changes; it is not necessary to restart the server

<figure><img src="https://github.com/valhuber/apilogicserver/wiki/images/ui-admin/admin-yaml.png?raw=true"></figure>

#### Models and admin correlation

See [this section](https://github.com/valhuber/ApiLogicServer/wiki#data-model-classes).

#### Not altered on `rebuild`
The rebuild commands do not override your customizations.  They do recreate `admin-created.yaml`.  You can use this to merge into your `admin.yaml`, e.g., to pick up new tables, relationships, etc.