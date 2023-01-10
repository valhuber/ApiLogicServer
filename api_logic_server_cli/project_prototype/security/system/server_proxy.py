
import config
authentication_provider = config.Config.SECURITY_PROVIDER


class Server():

    _current_user = None
    
    @classmethod
    def current_user(cls):
        """ 
        STUB for authentication - presumably returned from JWT saved during login
        """
        if Server._current_user is None:
            Server._current_user = authentication_provider.get_user("aneu", "")
        return Server._current_user
