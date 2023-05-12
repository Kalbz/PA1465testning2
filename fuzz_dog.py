import random

import json
import orjson
import msgspec
import string
import itertools
from tqdm import tqdm


FUZZ_CHARS = ['\n', '\t', '\r', '\b', '\f', '\\', '"']

def random_truefalse(length):
    if length % 2 == 0:
        return True
    else:
        return False


def random_int(length):
    """Return a random integer between 0 and 10000."""
    return random.randint(0, length)

def random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation + ''.join(FUZZ_CHARS)
    return ''.join(random.choice(characters) for _ in range(length))

def random_list(length, max_depth):
    return [random_data(max_depth - 1) for _ in range(length)]

def random_dict(length, max_depth):
    return {random_string(random.randint(1, 10)): random_data(max_depth - 1) for _ in range(length)}

def random_data(max_depth=3):
    simple_data_types = [
        random_string,
        random_truefalse,
        random_int,
    ]

    complex_data_types = [
        random_list,
        random_dict,
    ]

    if max_depth > 0:
        data_types = simple_data_types + complex_data_types
    else:
        data_types = simple_data_types

    random_function = random.choice(data_types)

    if random_function in complex_data_types:
        return random_function(random.randint(1, 10), max_depth - 1)
    else:
        return random_function(random.randint(1, 10))

def random_data_generator():
    """Yield random data as dictionaries."""
    keys = [
        'data',
        'type',
        'status',
        'job',
        'password',
        'username',
        'token',
        'id',
        'name',
        'email',
        'phone',
        'address',
        'description',
        'date',
        'time',
        'datetime',
        'active',
    ]

    for _ in itertools.repeat(None):
        yield {key: random_data() for key in keys}



def main():
    random.seed(9001)
    data_generator = random_data_generator()
    exeptions = []
    mismatches = []
    for _ in tqdm(range(1000)):
        data = next(data_generator)
        try:
            output_json = json.dumps(data, indent=None, separators=(',', ':'))
            print(output_json)
            output_orjson = orjson.dumps(data)
            output_mesgspec = msgspec.json.encode(data)
        except Exception as exception:
            exeptions += [(exception, data)]
        else:
            if not output_json.encode() == output_orjson == output_mesgspec:
                print(output_json.encode(), output_orjson, output_mesgspec)
                mismatches += [data]
    print(f'{len(exeptions)} exceptions and {len(mismatches)} mismatches found')


if __name__ == '__main__':
    main()



# @dataclasses.dataclass
# class Member:
#     id: int
#     active: bool = dataclasses.field(default=False)

# @dataclasses.dataclass
# class Object:
#     id: int
#     name: str
#     members: typing.List[Member]

# >>> orjson.dumps(Object(1, "a", [Member(1, True), Member(2)]))
# b'{"id":1,"name":"a","members":[{"id":1,"active":true},{"id":2,"active":false}]}'


# >>> import orjson, datetime, zoneinfo
# >>> orjson.dumps(
#     datetime.datetime(2018, 12, 1, 2, 3, 4, 9, tzinfo=zoneinfo.ZoneInfo("Australia/Adelaide"))
# )
# b'"2018-12-01T02:03:04.000009+10:30"'
# >>> orjson.dumps(
#     datetime.datetime(2100, 9, 1, 21, 55, 2).replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
# )
# b'"2100-09-01T21:55:02+00:00"'
# >>> orjson.dumps(
#     datetime.datetime(2100, 9, 1, 21, 55, 2)
# )
# b'"2100-09-01T21:55:02"'