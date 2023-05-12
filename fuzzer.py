import fuzzing_json
import random
import datetime
import numpy
import json
import orjson, uuid, dataclasses, typing
import msgspec
import string
from tqdm import tqdm



def main():
    random.seed(9001)
    data_generator = fuzzing_json.random_data_generator()
    exeptions = []
    mismatches = []
    for _ in tqdm(range(1000)):
        data = next(data_generator)
        try:
            output_json = json.dumps(data, indent=None, separators=(',', ':'), ensure_ascii=False).encode('utf8')
            output_orjson = orjson.dumps(data)
            output_mesgspec = msgspec.json.encode(data)
        except Exception as exception:
            exeptions += [(exception, data)]
            
        else:
            if not output_json == output_orjson == output_mesgspec:
                print(output_json.encode(), output_orjson, output_mesgspec)
                mismatches += [data]
    print(f'{len(exeptions)} exceptions and {len(mismatches)} mismatches found')
    print(exeptions)

if __name__ == '__main__':
    main()
