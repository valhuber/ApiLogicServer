from database import models
import logging
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship, remote, foreign

"""
    If you wish to drive models from the database schema,
    you can use this file to customize your schema (add relationships, derived attributes),
    and preserve customizations over iterations (regenerations of models.py).
"""

app_logger = logging.getLogger(__name__)

# add relationship: https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#specifying-alternate-join-conditions
models.Employee.Manager = relationship('Employee', cascade_backrefs=True, backref='Manages',
                                       primaryjoin=remote(models.Employee.Id) == foreign(models.Employee.ReportsTo))
"""
added relationships appear in your api / swagger, automatically.

They must be manually added to your ui/admin/admin.yaml, e.g.

      - direction: tomany
        fks:
          - ReportsTo
        name: Manages
        resource: Employee
      - direction: toone
        fks:
        - ReportsTo
        name: Manager
        resource: Employee

"""


# add derived attribute: https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py
@jsonapi_attr
def proper_salary(row):  # type: ignore [no-redef]
    if not hasattr(row, "_proper_salary"):
        row._proper_salary = row.Salary * 1.25  # create the attr with default value
    return row._proper_salary


@proper_salary.setter
def proper_salary(row, value):  # type: ignore [no-redef]
    row._proper_salary = value
    # print(f'_proper_salary={row._proper_salary}')
    pass

models.Employee.ProperSalary = proper_salary

app_logger.info("..database/customize_models.py: models.Employee.Manager(manages), Employee.ProperSalary")
