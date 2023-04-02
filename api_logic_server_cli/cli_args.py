

class ProjectArgs():
    
    def __init__(self):
        self.command = None # type: str
        self.project_name = None # type: str
        """ full nodal name """
        self.db_url = None # type: str
        self.bind_key = None # type: str
        self.bind_key_url_separator = None # type: str
        self.api_name = None # type: str
        self.host = None # type: str
        self.port = None # type: str
        self.swagger_host = None # type: str
        self.not_exposed = None # type: str
        self.from_git = None # type: str
        self.db_types = None # type: str
        self.open_with = None # type: str
        self.run = None
        self.use_model = None # type: str
        self.admin_app = None
        self.flask_appbuilder = None
        self.favorites = None
        self.non_favorites = None
        self.react_admin = None
        self.extended_builder = None
        self.include_tables = None
        self.multi_api = None
        self.infer_primary_key = None
