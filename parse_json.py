# import sys
# sys.setrecursionlimit(10000)

# import xmltodict
import json
with open("r.txt", 'r', encoding='utf-8') as f:
    # root = xmltodict.parse(f.read())
    root = json.load(f)
# key = "/"
# parse(root, key)

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

keys = extract_json_keys(root)

for key in keys:
    print(key)
