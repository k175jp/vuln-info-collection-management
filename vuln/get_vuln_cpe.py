import requests
import json

def get_jvn(part, vender, product):
    pass

def get_nvd(part, vender, product):
    # uriの生成
    uri = f'https://services.nvd.nist.gov/rest/json/cves/2.0?virtualMatchString=cpe:2.3:{part}:{vender}:{product}:*:*:*:*:*&noRejected'
    # リクエストの送信
    response = requests.get(uri)
    # jsonデータをdictに変換
    json_data = json.loads(response.text)

    return json_data

