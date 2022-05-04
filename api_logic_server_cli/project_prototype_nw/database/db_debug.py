from sqlalchemy import create_engine, inspect

e = create_engine("sqlite:////Users/val/dev/servers/ApiLogicProject/database/db.sqlite")
inspector = inspect(e)
pk = inspector.get_pk_constraint("Category")
cols = inspector.get_columns("Category")
print(f'\nSqlite debug info\npk: {str(pk)}, \ncols: {str(cols)}\n')