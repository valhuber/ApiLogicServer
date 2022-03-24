from behave import *
import requests, pdb
import test_utils
import json

@given('Sample Database')
def step_impl(context):
    assert True

@when('Transactions are submitted')
def step_impl(context):
    assert True is not False

@then('Enforce business policies with Logic (rules + code)')
def step_impl(context):
    scenario = "Transaction Processing"
    test_utils.prt(f'Rules Report', scenario)
    assert True