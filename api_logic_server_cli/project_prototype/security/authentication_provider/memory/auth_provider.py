from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider
from typing import List, Optional

# **********************
# in mem auth provider
# **********************

users = {}

from dataclasses import dataclass

@dataclass
class DataClassUserRole:
    role_name: str

@dataclass
class DataClassUser:
    name: str
    client_id: int
    id: str
    UserRoleList: Optional [List[DataClassUserRole]] = None


class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def get_user(id: str, password: str) -> object:
        """
        Must return a row object with attributes name and UserRoleList (others as required)
        role_list is a list of row objects with attribute name

        row object is a DotMap (as here) or a SQLAlchemy row
        """
        return users[id]

def add_user(name: str, id: int):
    user = DataClassUser( name=name, id=name, client_id=id)
    users[name] = user
    return user

    """
    user.name = name
    user.UserRoleList = []
    user.client_id = id
    for each_role in role_list:
        r = DotMap()
        r.role_name = each_role
        user.UserRoleList.append(r)
    users[name] = user

    
        add_user("sam", 1, ("sa", "dev"))
        add_user("aneu", 2, ("tenant", "manager"))
        add_user("client1", 3, ("tenant", "manager"))
        add_user("client2", 4, ("renter", "manager"))
        add_user("mary", 5, ("tenant", "manager"))
    """

sam = add_user("sam", 1)
sam_role_list = [DataClassUserRole(role_name="manager")]
sam.UserRoleList = sam_role_list

aneu = add_user("aneu", 1)
aneu_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
aneu.UserRoleList = aneu_role_list

c1 = add_user("client1", 3)
c1_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
c1.UserRoleList = c1_role_list

c2 = add_user("client2", 4)
c2_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="renter")]
c2.UserRoleList = c1_role_list

m = add_user("mary", 5)
m_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
m.UserRoleList = c1_role_list

sam_row = Authentication_Provider.get_user("sam", "")
print(f'Sam: {sam_row}')

"""
this is a super-simplistic auth_provider, to demonstrate the "provide your own" approach
will typically user provider for sql
"""