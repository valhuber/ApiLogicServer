# Initialize Logging
import logging
import util
import sys
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic import logic_row
from logic_bank.rule_type import constraint
from sqlalchemy.orm import session
from safrs import ValidationError

import database.db
from logic.logic_bank import declare_logic

""" Initialization
1 - Connect
2 - Register listeners (either hand-coded ones above, or the logic-engine listeners).
"""

app_logger = logging.getLogger("api_logic_server_app")
app_logger.debug("logic/__init__ loaded - setup logging, connect to db, register listeners")

setup_logic_logger = False
if setup_logic_logger:
    logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
    logic_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
    handler.setFormatter(formatter)
    logic_logger.addHandler(handler)
    logic_logger.propagate = False

do_engine_logging = False
engine_logger = logging.getLogger('engine_logger')  # for internals
if do_engine_logging:
    engine_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
    handler.setFormatter(formatter)
    engine_logger.addHandler(handler)


# session: session = db.session


def constraint_handler(message: str, constraint: constraint, logic_row: logic_row):    # message: str, constr: constraint, row: logic_row):
    raise ValidationError(message)


# LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler )

app_logger.debug("logic/__init__ LogicBank activated\n")
