import time

# from vuln.get_vuln_cpe import get_jvn, get_nvd
from vuln.get_vuln_cpe import get_nvd
from cpe.get_cpe_list import get
# from extract.extract_data import extract_jvn, extract_nvd
from extract.extract_data import extract_nvd
# from integrate.integrate_data import integrate
# from save.save_db import save



def main():
    cpe_list = get() # cpe/cpe.listをdictで取得
    for key, value in cpe_list.items(): 
        for v in value:
            cpe = v['cpe']
            for c in cpe:
                part, vender, product = c.split(':')

                # cpeから脆弱性情報の取得してdictオブジェクトを受け取る
                # jvn_vuln = get_jvn(part, vender, product)
                nvd_vuln = get_nvd(part, vender, product)

                # 上のデータからデータフォーマットに沿ってデータを抽出
                # jvn_data = extract_jvn(jvn_vuln)
                nvd_data = extract_nvd(nvd_vuln)

                # 上のデータを統合
                # data = integrate(product, jvn_data, nvd_data)

                # 上のデータを保存
                # save(key, data)
                time.sleep(6) # 30秒で5リクエスト = 6秒で1リクエスト(nvd)

    
if __name__ == '__main__':
    main()
