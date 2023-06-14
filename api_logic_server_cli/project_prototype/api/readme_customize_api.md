Without customization, your API supports multi-table retrieval.  For more information, [see here](https://apilogicserver.github.io/Docs/API-Multi-Table).

This describes how to *add new endpoints*.  For more information, [see here](https://apilogicserver.github.io/Docs/API-Customize).

&nbsp;

## Examples      
Examples from tutorial project:
* Examples drawn from [tutorial project](https://github.com/ApiLogicServer/demo/blob/main/api/customize_api.py)
* Use Shift + "." to view in project mode

&nbsp;

### New Endpoint: Standard Flask with Security, not exposed in Swagger

Use standard Flask / SQLAlchemy (background [here](https://docs.sqlalchemy.org/en/20/core/connections.html)):

```python
    @app.route('/filters_cats')
    @admin_required()
    def filters_cats():
        """
        Illustrates:
        * Explore SQLAlchemy and/or filters.
        
        Test (returns rows 2-5) (no auth):
            curl -X GET "http://localhost:5656/filters_cats [no-filter | simple-filter]"
        """

        from sqlalchemy import and_, or_
        filter_type = request.args.get('filter')
        if filter_type is None:
            filter_type = "multiple filters"
        db = safrs.DB           # Use the safrs.DB, not db!
        session = db.session    # sqlalchemy.orm.scoping.scoped_session
        Security.set_user_sa()  # an endpoint that requires no auth header (see also @admin_required)

        if filter_type.startswith("n"):
            results = session.query(models.Category)    # .filter(models.Category.Id > 1)
        elif filter_type.startswith("s"):               # normally coded like this
            results = session.query(models.Category) \
                .filter(models.Category.Id > 1) \
                .filter(or_((models.Category.Client_id == 2), (models.Category.Id == 5)))
        else:                                           # simulate grant logic (multiple filters)
            client_grant = models.Category.Client_id == 2
            id_grant = models.Category.Id == 5
            grant_filter = or_( client_grant, id_grant)
            results = session.query(models.Category) \
                .filter(models.Category.Id > 1)  \
                .filter(grant_filter)
        return_result = []
        for each_result in results:
            row = { 'id': each_result.Id, 'name': each_result.CategoryName}
            return_result.append(row)
        return jsonify({ "success": True, "results":  return_result})
```

&nbsp;

### New Endpoint: Standard Flask, exposed in Swagger

```python
class CategoriesEndPoint(safrs.JABase):
    """
    Illustrates
    * Swagger-visible RPC that requires authentication (@jwt_required()).

    Test in swagger (auth required)
    * Post to endpoint auth to obtain <access_token> value - copy it to clipboard
    * Authorize (top of swagger), using Bearer <access_token>
    * Post to CategoriesEndPoint/get_cats, observe only row 1 returned

    """

    @staticmethod
    @jwt_required()
    @jsonapi_rpc(http_methods=['POST'], valid_jsonapi=False)
    def get_cats():
        db = safrs.DB
        session = db.session
        # Security.set_user_sa()  # use to bypass authorization (also requires @admin_required)

        result = session.query(models.Category)
        for each_row in result:
            app_logger.debug(f'each_row: {each_row}')
        rows = util.rows_to_dict(result)
        response = {"result": rows}
        return response
```

&nbsp;

## Data Access

The samples also illustrate several forms of data access, summarized in the table below.  Note the use of `util.py`, included with all projects.

| Function | Auth required                         | Illustrates             | Util Usage  |
|:-------------- |:------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|
| ```order_nested_objects()``` |    | Nested Model Objects         | util.format_nested_objects() jsoniify(row).json   |
| ```get_cats()``` |  Y  | Model query      |Util.rows_to_dict<br>..row.to_dict   |
| ```filters_cats()``` |  Y  | Model query, filters         | No: No  - Manual {} creation   |
| ```raw_sql_cats()``` |    | Raw sql        | Util.rows_to_dict<br>..fields iterator   |


