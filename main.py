import time
import json
from datetime import datetime, timedelta, timezone
import os

from vuln.get_vuln_cpe import get_jvn_detail, get_jvn_overview
# from vuln.get_vuln_cpe import get_jvn_overview, get_jvn_detail, get_nvd
from cpe.get_cpe_list import get
from extract.extract_data import extract_jvn_id, extract_jvn
# from extract.extract_data import extract_jvn_id, extract_jvn, extract_nvd
# from integrate.integrate_data import integrate
from db.save_db import MongoManager

JST = timezone(timedelta(hours=+9), 'JST')

def main():
    mm = MongoManager('', '')
    with open("lasttime", "r") as f:
        last_time = f.read()
    if last_time == None:
        last_time = "2015/1/1"

    _last_time = datetime.strptime(last_time + ' +0900', "%Y/%m/%d %z")
    e_day = datetime.now(JST) - timedelta(1)
    if (e_day - _last_time).days <= 0:
        print("Unable to update due to latest version")
        exit(1)
    e_day = e_day.strftime('%Y/%m/%d')

    cpe_list = get() # cpe/cpe.listをdictで取得
    for key, value in cpe_list.items(): 
        for v in value:
            cpe = v['cpe']
            for c in cpe:
                try:
                    part, vender, product = c.split(':')
                except:
                    print(c)
                    exit(1)
                jvn_vuln = get_jvn_overview(part, vender, product, last_time, e_day)
                totalresult, startindex, jvn_ids = extract_jvn_id(jvn_vuln)
                while int(totalresult) >= int(startindex) + 50:
                    option = f"&startItem={int(startindex) + 50}"
                    jvn_vuln = get_jvn_overview(part, vender, product, last_time, e_day, option)
                    totalresult, startindex, _jvn_ids = extract_jvn_id(jvn_vuln)
                    jvn_ids = jvn_ids + _jvn_ids
                jvn_data = []
                for i in range(len(jvn_ids)//10 + 1):
                    _jvn_data = get_jvn_detail("+".join(jvn_ids[i*10:(i+1)*10]))
                    _jvn_data = extract_jvn(part, vender, product, _jvn_data)
                    jvn_data = jvn_data + _jvn_data
                
                data = jvn_data

                # nvd_vuln = get_nvd(part, vender, product)
                # totalresults, resultsperpage, startindex, nvd_data = extract_nvd(nvd_vuln)
                # while totalresults > (startindex + 1) * resultsperpage:
                #     time.sleep(6) # 30秒で5リクエスト = 6秒で1リクエスト(nvd)
                #     nvd_vuln = get_nvd(part, vender, product, f'&startIndex={startindex + 1}')
                #     totalresults, resultsperpage, startindex, _nvd_data = extract_nvd(nvd_vuln)
                #     nvd_data = nvd_data + _nvd_data
                # print(json.dumps(nvd_data))
                
                # # 上のデータを統合
                # data = integrate(product, jvn_data, nvd_data)

                # 上のデータを保存
                mm.save(key, data)

                time.sleep(6)
    with open("lasttime", "w") as f:
        f.write(e_day)

    
if __name__ == '__main__':
    main()
