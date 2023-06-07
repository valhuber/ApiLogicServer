from enum import Enum


class ExtendedEnum(Enum):
    """
    enum that supports list() to print allowed values

    Thanks: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class OptLocking(ExtendedEnum):
    """
    Valid Values for OptLocking, e.g.

        Config.OPT_LOCKING == OptLocking.OPTIONAL.value

    Args:
        ExtendedEnum (_type_): _description_
    """
    IGNORED = "ignored"
    OPTIONAL = "optional"
    REQUIRED = "required"

class CliArgsBase():
    
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
        self.favorites = None # type: str
        self.non_favorites = None # type: str
        self.react_admin = None
        self.extended_builder = None
        self.include_tables = None
        self.multi_api = None
        self.infer_primary_key = None
        self.opt_locking = None # type: str
        """ <str> in OptLocking.list() """
        self.id_column_alias = None  # type: str
        """ safrs reserves id as property, so use this alias for db cols with that name """
        self.opt_locking_attr = None # type: str
