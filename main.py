import time

# from vuln.get_vuln_cpe import get_jvn, get_nvd
from vuln.get_vuln_cpe import get_nvd
from cpe.get_cpe_list import get
# from extract.extract_data import extract_jvn, extract_nvd
from extract.extract_data import extract_nvd
# from integrate.integrate_data import integrate
# from save.save_db import save



def main():
    cpe_list = get()
    result = {}
    for key, value in cpe_list.items():
        for v in value:
            cpe = v['cpe']
            for c in cpe:
                part, vender, product = c.split(':')
                # jvn_vuln = get_jvn(part, vender, product)
                nvd_vuln = get_nvd(part, vender, product)
                # jvn_data = extract_jvn(jvn_vuln)
                nvd_data = extract_nvd(nvd_vuln)
                # data = integrate(product, jvn_data, nvd_data)
                # save(key, data)
                time.sleep(6)
                break
            break
        break
    
if __name__ == '__main__':
    main()
