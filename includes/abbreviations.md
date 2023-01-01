*[parent]: One side of a one-to-many relationship (e.g., Customer for Orders)
*[Parent]: One side of a one-to-many relationship (e.g., Customer for Orders)
*[child]: Many side of a one-to-many relationship (e.g., Orders for Customer)
*[Child]: Many side of a one-to-many relationship (e.g., Orders for Customer)
*[lookup]: User Interface to get list of parent rows, select one, and fill child Foreign Key (e.g. Lookup Product for OrderDetail)
*[Lookup]: User Interface to get list of parent rows, select one, and fill child Foreign Key (e.g. Lookup Product for OrderDetail)
*[Lookups]: User Interface to get list of parent rows, select one, and fill child Foreign Key (e.g. Lookup Product for OrderDetail)
*[lookups]: User Interface to get list of parent rows, select one, and fill child Foreign Key (e.g. Lookup Product for OrderDetail)
*[Foreign Key]: one or more fields in child rows that identify a parent row (e.g., OrderDetail.ProductId identifies a Product)
*[foreign key]: one or more fields in child rows that identify a parent row (e.g., OrderDetail.ProductId identifies a Product)
*[Multi-Page]: Applications providing multiple pages, e.g. a Customer Page and an Order Page
*[Multi-page]: Applications providing multiple pages, e.g. a Customer Page and an Order Page
*[multi-page]: Applications providing multiple pages, e.g. a Customer Page and an Order Page
*[Multi-Table]: An Application form displaying multiple table, e.g., an Order with a (Parent) Sales Rep, and (children) OrderDetails
*[Multi-table]: An Application form displaying multiple table, e.g., an Order with a (Parent) Sales Rep, and (children) OrderDetails
*[multi-table]: An Application form displaying multiple table, e.g., an Order with a (Parent) Sales Rep, and (children) OrderDetails
*[Declarative Hide/Show]: Support for Application fields that are displayed/hidden based on an expression for the current row declared in the Admin.yaml file
*[Automatic Joins]: Automatically joined parent data, e.g., the ProductName (instead of the ProductId) for OrderDetails; these defaults can be overridden in the Admin.yaml file
*[Automatic joins]: Automatically joined parent data, e.g., the ProductName (instead of the ProductId) for OrderDetails; these defaults can be overridden in the Admin.yaml file
*[automatic joins]: Automatically joined parent data, e.g., the ProductName (instead of the ProductId) for OrderDetails; these defaults can be overridden in the Admin.yaml file
*[Page Transitions]: form controls that enable users to navigate to forms for related data, e.g., from a Customer/Orders page to an Order/OrderDetails page
*[Page transitions]: form controls that enable users to navigate to forms for related data, e.g., from a Customer/Orders page to an Order/OrderDetails page
*[Cascade Add]: support for adding child rows (e.g., OrderDetails) after adding a parent row (e.g., Order)
*[Pagination]: support to show large lists of rows in page-size sets, to reduce database overhead and unwieldly pages
*[pagination]: support to show large lists of rows in page-size sets, to reduce database overhead and unwieldly pages
*[Declarative]: specifications that dictate _what_ should be done, instead of detailed that is _how_ the feature is provided.  Declarative specifications are much more concise, automatically ordered, automamatically optimized and automatically invoked (re-used).  Declarative specifications can be used for client, API and logic behavior
*[declarative]: specifications that dictate _what_ should be done, instead of detailed that is _how_ the feature is provided.  Declarative specifications are much more concise, automatically ordered, automamatically optimized and automatically invoked (re-used).  Declarative specifications can be used for client, API and logic behavior
*[Business Logic]: multi-table constraints and derivations, e.g., the Customer Balance may not exceed the CreditLimit, and is derived as the sum of unshipped Order AmountTotals.
*[business logic]: multi-table constraints and derivations, e.g., the Customer Balance may not exceed the CreditLimit, and is derived as the sum of unshipped Order AmountTotals.
*[ORM]: Object Relational Manager - dev-friendly sql access, such as row objects (e.g., SQLAlchemy)
*[orm]: Object Relational Manager - dev-friendly sql access, such as row objects (e.g., SQLAlchemy)
*[Codespaces]: a Github product that creates complete cloud-based dev environments for containerized Github projects, including Browser-based IDE development.
*[docker account]: create using your browser at hub.docker.com
*[docker repository]: can can be downloaded (pulled) to create a docker image on your local computer
*[docker image]: created from a docker repository, a set of local files that can be run as a docker container
*[docker container]: a running image
*[Authentication]: a login function that confirms a user has access, usually by posting credentials and obtaining a token identifying the users' roles.
*[Authorization]: controlling access to row/columns based on assigned roles.
*[Role]: in security, users are assigned one or many roles.  Roles are authorized for access to data, potentially down to the row/column level.
*[Authentication-Provider]: Developer-supplied Class that, given a id/password, authenticates a user and returns the list of authorized roles (on None).  Invoked by the system when client apps log in.
