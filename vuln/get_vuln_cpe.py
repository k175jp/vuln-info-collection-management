import requests
import json

def get_jvn(part, vender, product):
    pass

def get_nvd(part, vender, product):
    uri = f'https://services.nvd.nist.gov/rest/json/cves/2.0?virtualMatchString=cpe:2.3:{part}:{vender}:{product}:*:*:*:*:*&noRejected'
    response = requests.get(uri)
    json_data = json.loads(response.text)

    return json_data

