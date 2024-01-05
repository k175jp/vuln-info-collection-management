import requests
import json
import time
import xmltodict

class TryException(Exception):
    pass

def get_jvn_overview(part, vender, product, s_day, e_day, option="", count=1):
    if count > 10:
        raise TryException("try 10 times without success")

    s_year, s_month, s_date = s_day.split('/')
    e_year, e_month, e_date = e_day.split('/')
    
    # uriの生成
    # uri = f'https://jvndb.jvn.jp/myjvn?method=getVulnOverviewList&feed=hnd&cpeName=cpe:/{part}:{vender}:{product}&datePublicStartY={s_year}&datePublicStartM={s_month}&datePublicStartD={s_date}&datePublicEndY={e_year}&datePublicEndM={e_month}&datePublicEndD={e_date}&datePublishedStartY={s_year}&datePublishedStartM={s_month}&datePublishedStartD={s_date}&datePublishedEndY={e_year}&datePublishedEndM={e_month}&datePublishedEndD={e_date}&dateFirstPublishedStartY={s_year}&dateFirstPublishedStartM={s_month}&dateFirstPublishedStartD={s_date}&dateFirstPublishedEndY={e_year}&dateFirstPublishedEndM={e_month}&dateFirstPublishedEndD={e_date}{option}'
    uri = f'https://jvndb.jvn.jp/myjvn?method=getVulnOverviewList&feed=hnd&cpeName=cpe:/{part}:{vender}:{product}&datePublicStartY=2015&rangeDatePublished=n&dateFirstPublishedStartY={s_year}&dateFirstPublishedStartM={s_month}&dateFirstPublishedStartD={s_date}&dateFirstPublishedEndY={e_year}&dateFirstPublishedEndM={e_month}&dateFirstPublishedEndD={e_date}{option}'

    # リクエストの送信
    response = requests.get(uri)
    if response.status_code == 200:
        # xmlデータをdictに変換
        xml_data = xmltodict.parse(response.text)
    else:
        time.sleep(1)
        try:
            xml_data = get_jvn_overview(part, vender, product, s_day, option, count+1)
        except TryException as e:
            print(e)
            xml_data = {}
    return xml_data

def get_jvn_detail(vulnIds, count=1):
    if count > 10:
        raise TryException("try 10 times without success")

    # uriの生成
    uri = f'https://jvndb.jvn.jp/myjvn?method=getVulnDetailInfo&feed=hnd&vulnId={vulnIds}'

    response = requests.get(uri)
    if response.status_code == 200:
        xml_data = xmltodict.parse(response.text)
    else:
        time.sleep(1)
        try:
            xml_data = get_jvn_detail(vulnids, count+1)
        except TryException as e:
            print(e)
            xml_data = {}
    return xml_data


def get_nvd(part, vender, product, option="", count=1):
    if count > 10:
        raise TryException("try 10 times without success")

    # uriの生成
    uri = f'https://services.nvd.nist.gov/rest/json/cves/2.0?virtualMatchString=cpe:2.3:{part}:{vender}:{product}:*:*:*:*:*&noRejected{option}'

    # リクエストの送信
    response = requests.get(uri)
    if response.status_code == 200:
        # jsonデータをdictに変換
        json_data = json.loads(response.text)
    else:
        time.sleep(1)
        try:
            json_data = get_nvd(part, vender, product, option, count+1)
        except TryException as e:
            print(e)
            json_data = {}

    return json_data

