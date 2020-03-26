import json
import types
import glob, os
from pathlib import Path
from jsonpath_rw import jsonpath, parse


def main():
    if __name__ == '__main__':
        for filename in glob.glob("../data/raw/*.json"):
            with open(filename) as json_file:
                data = json.load(json_file)
                z = json2tabular(data)
                print(z)
                filename_cleansed = f'../data/cleansed/{Path(filename).name}'
                with open(filename_cleansed, "w") as json_file_cleansed:
                    json.dump(z, json_file_cleansed)


def json2tabular(data: json):
    uri_value = data['uri']
    attributes = data['attributes']
    result: dict = {}
    for attribute_name in attributes:
        attribute = attributes[attribute_name]
        # print(f'{attribute_name} -> {attribute}')
        if attribute_name not in ['crosswalks', 'refentity']:
            attribute_values: str = ','.join(
                [str(y['value']) for y in list(filter(lambda x: dict(x)['ov'] is True, attribute))])
            # attribute_values=urllib.parse.quote(attribute_values)
            print(f'{uri_value} -> {attribute_name} -> {attribute_values}')
            # avoid non-primitive objects
            result[attribute_name] = attribute_values.strip() if '{' not in attribute_values else ""
            # Special handling for known objects/structures
            if 'Addresses' == attribute_name:
                result[attribute_name] = process_addresses(attribute)
                print(f'**{uri_value} -> {attribute_name} -> {result[attribute_name]}')
    return result


def process_addresses(addresses: list):
    addresses_cleansed=[]
    for x in addresses:
        print(f'Label of Address --> {x["label"]}')
        address_cleansed = {}
        for k, v in x['value'].items():
            print(f'\tElements of an Address --> {k} -> {v}')
            if k.lower() != "zip":
                address_cleansed[k] = ",".join(
                    [ignore_complex(p['value']) for p in list(filter(lambda x: dict(x)['ov'] is True, v))])
            elif k.lower() == "zip":
                zip5: str = zip5_extract(flatten([q['value']['Zip5'] for q in
                                                  list(filter(lambda z: dict(z)['ov'] is True, v))]))
                print(f'zip5 --> {zip5}')
                address_cleansed[k] = zip5
        addresses_cleansed.append(address_cleansed)
        print(f'address_cleansed --> {address_cleansed}')
    res = addresses_cleansed
    return res


flatten = lambda l: [item for sublist in l for item in sublist]
zip5_extract = lambda l: ",".join([str(e['value']) for e in l])
ignore_complex = lambda l: "" if "{" in str(l) else str(l)
main()
