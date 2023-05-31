from behave import *
import requests, pdb
import json
import test_utils

host = "localhost"
port = "5656"

@given('Category: 1')
def step_impl(context):
    pass


@when('Get Cat1')
def step_impl(context):
    get_cat1 = "http://localhost:5656/api/Category/1/?fields%5BCategory%5D=Id%2CCategoryName%2CDescription%2CClient_id%2C_check_sum_%2CS_CheckSum"
    r = requests.get(url=get_cat1, headers= test_utils.login())
    response_text = r.text
    cat1 = json.loads(response_text)  # 'str' object has no attribute 'read'
    context.cat1 = cat1  # checksum: -4130312969102546939
    pass

@then('Expected Cat1 Checksum')
def step_impl(context):
    cat1 = context.cat1
    expected_checksum = "-4130312969102546939"
    checksum = cat1["data"]["attributes"]["S_CheckSum"]
    assert checksum == "-4130312969102546939", f'Unexpected Checksum[{checksum}, expected {expected_checksum}]'


@when('Patch Valid Checksum')
def step_impl(context):
    patch_uri = "http://localhost:5656/api/Category/1/"
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Description": "x",
                    "S_CheckSum": "-4130312969102546939"
                },
                "type": "Category",
                "id": "1"
            }
        }
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    context.response = r

@then('Valid Checksum, Invalid Description')
def step_impl(context):
    response_text = context.response.text
    assert "x cannot be" in response_text,\
    "Opt Locking Failed: Matching Checksum test"


@when('Patch Missing Checksum')
def step_impl(context):
    patch_uri = "http://localhost:5656/api/Category/1/"
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Description": "x",
                    "S_CheckSum": "-4130312969102546939"
                },
                "type": "Category",
                "id": "1"
            }
        }
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    context.response = r



@when('Patch Invalid Checksum')
def step_impl(context):
    patch_uri = "http://localhost:5656/api/Category/1/"
    patch_args = \
        {
            "data": {
                "attributes": {
                    "Description": "x",
                    "S_CheckSum": "Patch Invalid Checksum"
                },
                "type": "Category",
                "id": "1"
            }
        }
    r = requests.patch(url=patch_uri, json=patch_args, headers=test_utils.login())
    context.response = r

@then('Invalid Checksum')
def step_impl(context):
    response_text = context.response.text
    assert "Sorry, row altered by another" in response_text,\
    "Patch Invalid Checksum"
