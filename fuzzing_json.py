import random
import datetime
import numpy
import json
import orjson, uuid, dataclasses, typing
import msgspec
import string
from tqdm import tqdm

#I hope this is somewhat what you were looking for.

TLD = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil']
fuzz_chars = ['\n', '\t', '\r', '\b', '\f', '\\', '"']

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits ) for x in range(length))

#I was a bit unsure whether or not to include this because of the "Anslag" in the assignment
def random_unicode_string(length, min_codepoint=0x0000, max_codepoint=0xFFFF):
    return ''.join(chr(random.randint(min_codepoint, max_codepoint)) for _ in range(length))

def random_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + ''.join(fuzz_chars)) for _ in range(length))

def random_truefalse():
    return random.choice([True, False])

#This function finds "[(TypeError('Integer exceeds 64-bit range') from ORJSON"
def random_int():
    return random.randint(-10000000000000000000, -1000000000000000000)

def random_unicode(length):
    return ''.join(chr(random.randint(32, 126)) for _ in range(length))

def random_top_level_domain():
    return ''.join(random.choice(TLD))

def random_type():
    return random.choice(["Object", "Array", "String", "Number", "Boolean", "Null", "NULL"])

def generate_large_integer():
    return random.randint(0, 2**53 - 1)

def generate_large_double():
    return random.uniform(0, 1.8e308)

def random_element():
    choice = random.randint(0, 5)
    if choice == 0:
        return random_string(random.randint(1, 10))
    elif choice == 1:
        return random_int()
    elif choice == 2:
        return random_truefalse()
    elif choice == 3:
        return None
    elif choice == 4:
        return [random_element() for _ in range(random.randint(1, 5))]
    elif choice == 5:
        return random_unicode_string(random.randint(1, 10))
    elif choice == 6:
        return generate_large_double()
    elif choice == 7:
        return generate_large_integer()

def random_data_structure(max_depth=3):
    if max_depth == 0:
        return random_element()

    choice = random.randint(0, 5)
    if choice == 0:
        return [random_data_structure(max_depth - 1) for _ in range(random.randint(1, 5))]
    elif choice == 1:
        return {random_string(random.randint(1, 10)): random_data_structure(max_depth - 1) for _ in range(random.randint(1, 5))}
    elif choice == 2:
        return tuple(random_data_structure(max_depth - 1) for _ in range(random.randint(1, 5)))
    elif choice == 3:
        return {random.choice([random_string(random.randint(1, 10)), random.randint(-10000, 10000)]) for _ in range(random.randint(1, 5))}
    elif choice == 4:
        return {random_unicode_string(random.randint(1, 10)): random_data_structure(max_depth - 1) for _ in range(random.randint(1, 5))}
    elif choice == 5:
        return {random.choice([random_unicode_string(random.randint(1, 10)), random.randint(-10000, 10000)]) for _ in range(random.randint(1, 5))}

def random_data_generator():
    while True:
        nested_object = {
            random_key(random.randint(1, 10)): random_string(random.randint(1, 10))
            for _ in range(random.randint(1, 5))
        }
        yield {
            random_key(random.randint(-10000, 10000)): random_string(random.randint(1, 10)),
            random_key(random.randint(-10000000000000, 10000)): random_int(),
            random_key(random.randint(-10000, 10000)): random_truefalse(),
            random_key(random.randint(-10000, 10000)): None,
            random_key(random.randint(-10000, 10000)): nested_object,
            random_key(random.randint(-10000, 10000)): [random_string(random.randint(1, 10)) for _ in range(random.randint(1, 5))],
            random_key(random.randint(-10000, 10000)): [nested_object for _ in range(random.randint(1, 5))],
            random_key(random.randint(-10000, 10000)): tuple(random_string(random.randint(1, 10)) for _ in range(random.randint(1, 5))),
            random_key(random.randint(-10000, 10000)): tuple(nested_object for _ in range(random.randint(1, 5))),
            random_key(random.randint(-10000, 10000)): random_data_structure(),
            
        }
        # yield {
        #     # 'data': random_string(random.randint(1, 10)),
        #     'type': random_type(),
        #     'status': random_string(random.randint(1, 10)),
        #     'job': random_string(random.randint(1, 10)),
        #     'password': random_string(random.randint(1, 10)),
        #     'username': random_string(random.randint(1, 10)),
        #     'token': random_string(random.randint(1, 10)),
        #     "id": random_int(),
        #     "korv": {"id": random_int(), "name": random_string(random.randint(1, 10))},
        #     "dog": [0,1,2],
        #     "hot": (0,1,2),
        #     "str": "hello",
        #     "double": 1.0,
        #     "float": 1.0,
        #     "True": True,
        #     "False": False,
        #     "None": None,
            
        #     'name': random_string(random.randint(1, 10)),
        #     'email': random_string(random.randint(1, 10))+ '@' + random_string(random.randint(1, 10)) + random_top_level_domain(),
        #     'phone': random_string(random.randint(1, 10)),
        #     'address': random_string(random.randint(1, 10)),
        #     'description': random_string(random.randint(1, 10)),
        #     'date': random_string(random.randint(1, 10)),
        #     'datetime': random_string(random.randint(1, 10)),
        #     'active': random_truefalse(),
        #     'enabled': random_truefalse(),
        #     'disabled': random_truefalse(),
        #     'deleted': random_truefalse(),
        #     'created': random_truefalse(),
        #     'updated': random_truefalse(),
        #     'unicode_string': random_unicode(random.randint(1, 10)),
        #     'empty_string': '',
        #     'null_value': None,
        #     'long_string': random_string(random.randint(100, 200)),
        #     'special_chars': random.choice(fuzz_chars),
        #     'nested_object': {
        #         'key': random_string(random.randint(1, 10)),
        #         'value': random_string(random.randint(1, 10)),
        #     },
        #     'list': [random_string(random.randint(1, 10)) for _ in range(random.randint(1, 5))],
        #     'empty_list': [],
        #     'list_of_dicts': [
        #         {
        #             'key': random_string(random.randint(1, 10)),
        #             'value': random_string(random.randint(1, 10)),
        #         }
        #         for _ in range(random.randint(1, 5))
        #     ],

        # }


# All of the comments above is old code