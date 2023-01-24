from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider
from typing import List, Optional
from safrs import jsonapi_rpc

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
    password: str
    UserRoleList: Optional [List[DataClassUserRole]] = None

    # called by authentication
    def check_password(self, password=None):
        # print(password)
        return password == self.password

    @classmethod
    @jsonapi_rpc(valid_jsonapi=False)
    def login(cls, *args, **kwargs):
        """
            description: Login - Generate a JWT access token
            args:
                username: user
                password: password
        """
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)

        user = users[id]
        if not user or not user.check_password(password):
            abort(401, "Wrong username or password")

        access_token = create_access_token(identity=user)
        return { "access_token" : access_token}


class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def get_user(id: str, password: str) -> object:
        """
        Must return a row object with attributes name and UserRoleList (others as required)
        role_list is a list of row objects with attribute name

        row object is a DotMap (as here) or a SQLAlchemy row
        """
        return users[id]

def add_user(name: str, id: int, password: str):
    user = DataClassUser( name=name, id=name, client_id=id, password=password)
    users[name] = user
    return user

sam = add_user("sam", 1, "p")
sam_role_list = [DataClassUserRole(role_name="manager")]
sam.UserRoleList = sam_role_list

aneu = add_user("aneu", 1, "p")
aneu_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
aneu.UserRoleList = aneu_role_list

c1 = add_user("u1", 1, "p")
c1_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
c1.UserRoleList = c1_role_list

c2 = add_user("u2", 2, "p")
c2_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="renter")]
c2.UserRoleList = c1_role_list

m = add_user("mary", 5, "p")
m_role_list = [DataClassUserRole(role_name="manager"), DataClassUserRole(role_name="tenant")]
m.UserRoleList = c1_role_list

sam_row = Authentication_Provider.get_user("sam", "")
print(f'Sam: {sam_row}')

"""
this is a super-simplistic auth_provider, to demonstrate the "provide your own" approach
will typically user provider for sql

to test
1. Create project: nw-
2. Use memory.auth_provider in config.py
3. Disable api/authentication_expose_api.py
"""