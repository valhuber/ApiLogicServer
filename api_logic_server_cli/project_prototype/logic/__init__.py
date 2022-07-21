import logging
from logic_bank.logic_bank import LogicBank  # required for import operation
from logic_bank.exec_row_logic import logic_row
from logic_bank.rule_type import constraint
from safrs import ValidationError

app_logger = logging.getLogger("api_logic_server_app")
app_logger.debug("logic/__init__ begin")

import database.db
from logic.declare_logic import declare_logic

app_logger.debug(f'\nlogic/__init__ - {len(database.models.metadata.tables)} tables loaded')

def constraint_handler(message: str, constraint: constraint, logic_row: logic_row):    # message: str, constr: constraint, row: logic_row):
    raise ValidationError(message)


app_logger.debug("logic/__init__ end\n")
