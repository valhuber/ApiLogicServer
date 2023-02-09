from security.system.authorization import Grant, Security
from database import models
import database
import safrs
import logging

app_logger = logging.getLogger(__name__)

db = safrs.DB
session = db.session


class Roles():
    """ Define Roles here, so can use code completion (Roles.tenant) """
    tenant = "tenant"
    renter = "renter"
    manager = "manager"

Grant(  on_entity = models.Category,    # illustrate multi-tenant
        to_role = Roles.tenant,
        filter = lambda : models.Category.Client_id == Security.current_user().client_id)  # User table attributes

Grant(  on_entity = models.Category,    # u2 has both roles - should return client_id 2 (2, 3, 4), and 5
        to_role = Roles.manager,
        filter = lambda : models.Category.Id == 5)

app_logger.debug("Declare Security complete - security/declare_security.py"
    + f' -- {len(database.authentication_models.metadata.tables)} tables loaded')
