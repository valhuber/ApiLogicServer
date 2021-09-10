import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging


def declare_logic():
    app_logger = logging.getLogger("api_logic_server_app")
    app_logger.info("logic_bank.py - declare_logic")

    """ example from default database
    
    Rule.constraint(validate=models.Customer,
                    as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
    
    use code completion to declare rules here """
