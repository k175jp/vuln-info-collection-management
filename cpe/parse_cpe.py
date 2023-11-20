import xml.etree.ElementTree as ET

def get_cpe(xml, app_list):
    cpe_list = []
    for events, elem in ET.iterparse(xml):
        # if 'cpe-item' in elem.tag:
        if 'cpe23-item' in elem.tag:
            cpe = elem.attrib['name'].split(':')
            part = cpe[2]
            vender = cpe[3]
            product = cpe[4]
            part + ':' vender + ':'
            for app in app_list.values():
                for a in app:
                    for b in a.split(' '):
                        if b.lower() not in lower():
                            break
                        #if b.lower() not in elem.attrib['name'].lower():
                        #    break
                    else:
                        #cpe = ':'.join(elem.attrib['name'].split(':')[2:6])
                        cpe_list.append(cpe)
        elem.clear()
    print('\n'.join(cpe_list))
with open('cpe.list', 'r') as f:
    app = f.read()
app = app.split('\n\n')
app_list = {}
for a in app:
    s = [b for b in a.split('\n') if b != '']
    app_list[s[0]] = s[1:]

xml = 'cpe-list.xml'
get_cpe(xml, app_list)

