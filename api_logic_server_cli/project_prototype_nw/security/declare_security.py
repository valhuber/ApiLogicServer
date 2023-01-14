from security.system.authorization import Grant, Security
from database import models
import database
import safrs
import logging

app_logger = logging.getLogger("api_logic_server_app")
app_logger.debug("logic/declare_logic.py")

db = safrs.DB
session = db.session


class Roles():
    """ Define Roles here, so can use code completion (Roles.tenant) """
    tenant = "tenant"
    renter = "renter"

Grant(  on_entity = models.Category,    # illustrate multi-tenant
        to_role = Roles.tenant,         # th now a lamba
        filter = lambda : models.Category.Client_id == Security.current_user().client_id)  # User table attributes

Grant(  on_entity = models.Category,
        to_role = Roles.renter,
        filter = lambda : models.Category.Id == 2)

app_logger.info("Declare Security complete - security/declare_security.py"
    + f' -- {len(database.authentication_models.metadata.tables)} tables loaded')
