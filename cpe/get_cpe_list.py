import json

def get():
    with open('cpe/cpe.list', 'r') as f:
        cpe_list = json.load(f)
    return cpe_list
