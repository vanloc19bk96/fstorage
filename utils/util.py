import json
from collections import OrderedDict
from pathlib import Path
import yaml
from yaml.loader import SafeLoader

def read_json(fname):
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)

def read_yaml(fname):
    fname = Path(fname)
    with open(fname, mode='r') as handle:
        return yaml.load(handle, Loader=SafeLoader)

def extract_keys(dictionary, level = 1, max_level=2, output_keys=None):
    if output_keys is None:
        output_keys = []
    for key, value in dictionary.items():
        output_keys.append(key)
        if type(value) is dict and max_level - level != 0:
            extract_keys(value, level + 1, max_level, output_keys)
    return output_keys

def extract_value_by_key_path(dictionary, keys): # keys must be a list
    value = dictionary[keys[0]]
    for key in keys[1:]:
        if type(value) is dict:
            value = value[key]
        else:
            return value

    return value

def get_keys_from_config(config, max_level=1):
    return extract_keys(config, max_level=max_level)
