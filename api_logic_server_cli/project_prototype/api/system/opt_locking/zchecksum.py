import decimal

import sqlalchemy
from sqlalchemy import inspect

from safrs import SAFRSBase


def checksum(list_arg: list) -> int:

    real_tuple = []
    skip_none = True  # work-around for non-repeatable hash(None)
    if skip_none:     # https://bugs.python.org/issue19224
        real_tuple = []
        for each_entry in list_arg:
            if each_entry is None:
                real_tuple.append(13)
            else:
                real_tuple.append(each_entry)
    result = hash(tuple(real_tuple))
    print(f'checksum[{result}] from row: {list_arg})')
    return result


def checksum_row(row: object) -> int:
    inspector = inspect(row)
    mapper = inspector.mapper
    iterate_properties = mapper.iterate_properties
    attr_list = []
    for each_property in iterate_properties:
        print(f'row.property: {each_property} <{type(each_property)}>')
        if isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(row, each_property.class_attribute.key))
    return_value = checksum(attr_list)
    inspector_class = inspector.mapper.class_ 
    print(f'checksum_row (get) [{return_value}], inspector: {inspector}')
    return return_value  # eg. 6785985870086950264
    pass


def checksum_old_row(logic_row_old: object) -> int:
    attr_list = []
    for each_property in logic_row_old.keys():
        print(f'old_row.property: {each_property} <{type(each_property)}>')
        if True:  # isinstance(each_property, sqlalchemy.orm.properties.ColumnProperty):
            attr_list.append(getattr(logic_row_old, each_property))
    return_value = checksum(attr_list)
    print(f'checksum_old_row [{return_value}] -- seeing -4130312969102546939 (vs. get: -4130312969102546939-4130312969102546939)')
    return return_value  # eg. -4130312969102546939 (get: -4130312969102546939)
    pass

def checksum_lists(list_arg: list):
    real_tuple = list_arg
    skip_none = True 
    if skip_none:
        real_tuple = []
        for each_entry in list_arg:
            if each_entry is None:
                real_tuple.append(13)
            else:
                real_tuple.append(each_entry)
    result = \
        list(
            map(
                lambda l:
                    hash(tuple(l)),
                [ real_tuple ]
            )
        )
    print(f'check_sum_lists({list_arg}) = {result}')
    return result

checksum_3_lists = \
    list(  # thanks: https://stackoverflow.com/questions/39583070/checksum-for-a-list-of-numbers
        map(
            lambda l:
                hash(tuple(l)),
            [ [1,2], [3,4], [5,6]]
        )
    )
print(f'checksum_3_lists = {checksum_3_lists} - e.g, [-3550055125485641917, 1079245023883434373, -7007623702649218251]\n')

expected = -3550055125485641917
assert expected == checksum([1, 2]), "not repeatable ints"
assert expected == checksum([1, 2]), "not repeatable ints"  # ensure works twice in a row

variable_1_2 = [1, 2]
assert expected == checksum(variable_1_2), "not repeatable variable"

assert expected == checksum(variable_1_2), "not repeatable variable"


expected = 6378967857448501442
assert expected == checksum([1, "hello", decimal.Decimal(2)]), "mixed types"

expected = -6838578810036353648
if expected == checksum([1, "hello", decimal.Decimal(2), None]):
    print( "mixed types with None succeeds with work-around for hash(None)")
else:
    print( "..FAILS - None makes hash fail...\n")

assert 1 == hash(1), "hash 1"
assert -4594863902769663758 == hash('abc'), "hash 'abc'"
expected_value = -9223372036584854238
hash_none = hash(None)
if hash(None) == expected_value:
    print("None Hashes")
else:  # https://bugs.python.org/issue19224
    print(f"\nFAILS - Hash(None) {hash_none} is not repeatable - {hash(None)}, {hash(None)}")
    print(f"... {hash(None)}")

"""
    expected_value is not repeatable over runs, so server would not compute same value on retrieval then update??
        Would be a showstopper for checksum
        But, hash is based on a random seed, with you can override with env variable (see run config)
            Hash results are then repeatable

    EXCEPT: non-repeatable hash(None)
        So, we work around that by arbitrary substitution
"""
