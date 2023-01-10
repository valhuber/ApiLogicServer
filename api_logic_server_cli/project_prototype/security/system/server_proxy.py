
import config
authentication_provider = config.Config.SECURITY_PROVIDER


class Server():

    _JWT = None
    """ current user's JWT (user, roles) """
    
    @classmethod
    def current_user_from_JWT(cls):
        """ 
        STUB for authentication - presumably returned from JWT saved during login
        """
        if Server._JWT is None:
            Server.login("aneu", "")
        return Server._JWT
    
    @classmethod
    def login(cls, id, password):
        Server._JWT = authentication_provider.get_user("aneu", "")
