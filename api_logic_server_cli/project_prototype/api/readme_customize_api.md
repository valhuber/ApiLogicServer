Without customization, your API supports multi-table retrieval.  For more information, [see here](https://apilogicserver.github.io/Docs/API-Multi-Table).

This describes how to *add new endpoints*.  For more information, [see here](https://apilogicserver.github.io/Docs/API-Customize).

&nbsp;

## Examples      
Examples from tutorial project:
* Examples drawn from [tutorial project](https://github.com/ApiLogicServer/demo/blob/main/api/customize_api.py)
* Use Shift + "." to view in project mode

&nbsp;

### New Endpoint: Standard Flask, not exposed in Swagger

Use standard Flask / SQLAlchemy:

```python

    @app.route('/categories')
    @admin_required()
    def categories():
        """
        Basic Flask / SQLAlchemy endpoint.
        
        Test (returns rows 2-5):
            curl -X GET "http://localhost:5656/categories"
        """

        from sqlalchemy import and_, or_

        db = safrs.DB           # Use the safrs.DB, not db!
        session = db.session    # sqlalchemy.orm.scoping.scoped_session
        Security.set_user_sa()  # an endpoint that requires no auth header (see also @admin_required)

        results = session.query(models.Category) \
            .filter(models.Category.Id > 1) \
            .filter(or_((models.Category.Client_id == 2), (models.Category.Id == 5)))
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
    Illustrates swagger-visible RPC that requires authentication (@jwt_required()).

    Observe authorization is thus enforced.  Test in swagger --
    * Post to endpoint auth to obtain <access_token> value - copy it to clipboard
    * Authorize (top of swagger), using Bearer <access_token>
    * Post to CategoriesEndPoint/getcats, observe only rows 2-5 returned

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
            print(f'each_row: {each_row}')
        dont_rely_on_safrs_debug = True
        # response = {"result" : list(result)}
        if dont_rely_on_safrs_debug:
            rows = util.rows_to_dict(result)
            response = {"result": rows}
        return response
```
