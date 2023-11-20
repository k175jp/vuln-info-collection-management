import gzip
import requests
import io

URL = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz"

def get_cpe(url):
    res = requests.get(url)
    if res.status_code == 200:
        gzip_file = io.BytesIO(res.content)
        with gzip.open(gzip_file, 'rt') as f:
            xml_data =  f.read()
        with open('cpe-list.xml', 'w') as f:
            f.write(xml_data)
get_cpe(URL)
