from security.system.security_manager import Grant, Security
from database import models
import safrs

db = safrs.DB
session = db.session

'''

Declare Security here, for example:

class Roles():
    """ Define Roles here, so can use code completion (Roles.tenant) """
    tenant = "tenant"
    renter = "renter"

Grant(  on_entity = models.Category,    # need way to say "any model with attr xyx"?
        to_role = Roles.tenant,
        filter = models.Category.Id == Security.current_user().client_id)  # User table attributes
'''