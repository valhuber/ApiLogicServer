from database import models
import logging
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship, remote, foreign

"""
    If you wish to drive models from the database schema,
    you can use this file to customize your schema (add relationships, derived attributes),
    and preserve customizations over iterations (regenerations of models.py).
"""

app_logger = logging.getLogger("api_logic_server_app")
# add relationship: https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#specifying-alternate-join-conditions
models.Employee.Manager = relationship('Employee', cascade_backrefs=True, backref='Manages',
                                       primaryjoin=remote(models.Employee.Id) == foreign(models.Employee.ReportsTo))


# add derived attribute: https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py
@jsonapi_attr
def proper_salary(row):
    if not hasattr(row, "_proper_salary"):
        row._proper_salary = row.Salary * 1.25  # create the attr with default value
    return row._proper_salary


@proper_salary.setter
def proper_salary(row, value):
    row._proper_salary = value
    # print(f'_proper_salary={row._proper_salary}')
    pass

models.Employee.ProperSalary = proper_salary

app_logger.info("..database/customize_models.py: models.Employee.Manager(manages), Employee.ProperSalary")
