from abc import ABC, abstractmethod

# **************************************
# authentication provider abstract class
# **************************************

class Abstract_Authentication_Provider():
        
    @staticmethod
    @abstractmethod
    def get_user(id: str, password: str) -> object:
        """
        Must return a row object with attributes name and role_list
        role_list is a list of row objects with attribute name

        row object is a DotMap or a SQLAlchemy row
        
        print("subclass responsibility")
        return None
        """

