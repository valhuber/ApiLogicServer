import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import logging

from logic_bank.extensions.allocate import Allocate


def unpaid_orders(provider: LogicRow):
    """ returns Payments' Customers' Orders, where AmountOwed > 0, by OrderDate """
    customer_of_payment = provider.row.Customer
    unpaid_orders_result = provider.session.query(models.Order)\
        .filter(models.Order.AmountOwed > 0, models.Order.CustomerId == customer_of_payment.Id)\
        .order_by(models.Order.OrderDate).all()
    return unpaid_orders_result


def declare_logic():

    Rule.sum(derive=models.Customer.Balance, as_sum_of=models.Order.AmountOwed)

    Rule.formula(derive=models.Order.AmountOwed, as_expression=lambda row: row.AmountTotal - row.AmountPaid)
    
    Rule.sum(derive=models.Order.AmountPaid, as_sum_of=models.PaymentAllocation.AmountAllocated)

    Rule.formula(derive=models.PaymentAllocation.AmountAllocated, as_expression=lambda row:
        min(Decimal(row.Payment.AmountUnAllocated), Decimal(row.Order.AmountOwed)))

    Allocate(provider=models.Payment,  # uses default (overrideable) while_calling_allocator
            recipients=unpaid_orders,
            creating_allocation=models.PaymentAllocation)
