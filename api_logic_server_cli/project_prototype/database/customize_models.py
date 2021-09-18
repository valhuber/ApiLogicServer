from database import models
from safrs import jsonapi_attr
from sqlalchemy.orm import relationship, remote, foreign

"""
If you wish to drive models from the database schema,
you can use this file to customize your schema (add relationships, derived attributes),
and preserve customizations over iterations (regenerations of models.py).

Called from models.py (classes describing schema, per introspection).
"""
