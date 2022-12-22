from dotmap import DotMap  # a dict, but you can say aDict.name instead of aDict['name']... like a row
from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider

# **********************
# in mem auth provider
# **********************

users = {}

class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def get_user(id: str, password: str) -> object:
        """
        Must return a row object with attributes name and UserRoleList (others as required)
        role_list is a list of row objects with attribute name

        row object is a DotMap (as here) or a SQLAlchemy row
        """
        return users[id]

def add_user(name: str, id: int, role_list):
    user = DotMap()
    user.name = name
    user.UserRoleList = []
    user.client_id = id
    for each_role in role_list:
        r = DotMap()
        r.role_name = each_role
        user.UserRoleList.append(r)
    users[name] = user

add_user("Sam", 1, ("sa", "dev"))
add_user("aneu", 2, ("tenant", "manager"))
add_user("Client1", 3, ("tenant", "manager"))
add_user("Client2", 4, ("renter", "manager"))

sam_row = Authentication_Provider.get_user("Sam", "")
print(f'Sam: {sam_row}')

"""
this is a super-simplistic auth_provider ( a STUB)
will typically user provider for sql
"""