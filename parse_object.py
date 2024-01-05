import sys
sys.setrecursionlimit(10000)
import xmltodict
import json
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('filepath')
parser.add_argument('ext')
args = parser.parse_args()
filepath = args.filepath
ext = args.ext

def extract_json_keys(data, parent_key='', separator='::'):
    keys = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = parent_key + separator + key if parent_key else key
            keys.extend(extract_json_keys(value, new_key, separator))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = parent_key + separator + str(i) if parent_key else str(i)
            keys.extend(extract_json_keys(item, new_key, separator))
    else:
        keys.append(parent_key)
    return keys

with open(filepath, 'r', encoding='utf-8') as f:
    if ext == 'json':
        root = json.load(f)
    elif ext == 'xml':
        root = xmltodict.parse(f.read())

keys = extract_json_keys(root)

for key in keys:
    print(key)
