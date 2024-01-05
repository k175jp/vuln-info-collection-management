# def extract_jvn_overview(_data):
#     if _data == {}:
#         return 
#     data = _data['rdf:RDF']['item']
#     totalresults = _data['rdf:RDF']['status:Status']['@totalRes']
#     startindex = _data['rdf:RDF']['status:Status']['@firstRes']
    
#     jvn_data = []
#     jvn_ids = []
#     for jvn in data:
#         jvn_id = jvn.get('sec:identifier')
#         cve_id = ""
#         for _cve in jvn.get('sec:references'):
#             if _cve.get('@source') == 'CVE' or _cve.get('@source') == 'NVD':
#                 cve_id = _cve.get('@id')
#                 break
#         product = jvn.get('sec:cpe').get('@product')
#         cpe = jvn.get('sec:cpe').get('#text')
#         cvss = []
#         if isinstance(jvn.get('sec:cvss'), dict):
#             score = jvn.get('sec:cvss').get('@score')
#             vector = jvn.get('sec:cvss').get('@vector')
#             cvss.append({'source': 'isec-jvndb@ipa.go.jp', 'score': score, 'vector': vector})
#         elif isinstance(jvn.get('sec:cvss'), list):
#             for _cvss in jvn.get('sec:cvss'):
#                 score = _cvss.get('@score')
#                 vector = _cvss.get('@vector')
#                 cvss.append({'source': 'isec-jvndb@ipa.go.jp', 'score': score, 'vector': vector})
            
#         description = jvn.get('description')
#         published = jvn.get('dcterms:issued')
#         lastmodified = jvn.get('dcterms:modified')
#         jvn_data.append({'cveid': cve_id, 'jvnid': jvn_id, 'published': published, 'lastModified': lastmodified, 'description': description, 'cvss': cvss, 'productInfo': {'product': product, 'cpe': cpe}})
#         jvn_ids.append(jvn_id)
#     return totalresults, startindex, jvn_ids, jvn_data

def extract_jvn_id(_data):
    if _data == {}:
        return 
    data = _data.get('rdf:RDF', {}).get('item', [])
    totalresults = _data.get('rdf:RDF', {}).get('status:Status', {}).get('@totalRes', "0")
    startindex = _data.get('rdf:RDF', {}).get('status:Status', {}).get('@firstRes', "0")

    if isinstance(data, dict):
        data = [data]

    jvn_ids = []
    try:
        for jvn in data:
            jvn_id = jvn.get('sec:identifier', "")
            jvn_ids.append(jvn_id)
        jvn_ids = [i for i in jvn_ids if i != '']
        return totalresults, startindex, jvn_ids
    except:
        print(_data)
        exit(1)
    

def extract_jvn(_part, _vender, _product, _data):
    if _data == {}:
        return
    data = _data.get("VULDEF-Document", {}).get("Vulinfo", [])
    if isinstance(data, dict):
        data = [data]

    jvn_data = []
    for jvn in data:
        jvn_id = jvn.get("VulinfoID", "")
        vuln_info = jvn.get("VulinfoData", {})
        cve_id = ""
        for i in vuln_info.get("Related", {}).get("RelatedItem", {}):
            _cve_id = i.get("VulinfoID", "")
            if "CVE-" in _cve_id:
                cve_id = _cve_id
                break
        published = vuln_info.get("DateFirstPublished", "")
        lastmodified = vuln_info.get("DateLastUpdated", "")
        description = jvn.get("VulinfoData", {}).get("VulinfoDescription", {}).get("Overview")
        product = ""
        version = ""
        affecteditem = vuln_info.get("Affected", {}).get("AffectedItem", [])
        if isinstance(affecteditem, dict):
            affecteditem = [affecteditem]
        for i in affecteditem:
            if i.get("Cpe", {}).get("#text", "") == f"cpe:/{_part}:{_vender}:{_product}":
                product = i.get("ProductName", "")
                version = i.get("VersionNumber", "")
                break
        _cvss = vuln_info.get("Impact", {}).get("Cvss", [])
        cvss = []
        if isinstance(_cvss, list):
            for __cvss in _cvss:
                cvss.append({"version": __cvss.get("@version", ""), "score": __cvss.get("Base", ""), "vector": __cvss.get("Vector", ""), 'source': 'isec-jvndb@ipa.go.jp'})
        elif isinstance(_cvss, dict):
            cvss.append({"version": _cvss.get("@version", ""), "score": _cvss.get("Base", ""), "vector": _cvss.get("Vector", ""), 'source': 'isec-jvndb@ipa.go.jp'})
        impact = vuln_info.get("Impact", {}).get("ImpactItem", {}).get("Description", "")
        take_measures = vuln_info.get("Solution", {}).get("SolutionItem", {}).get("Description", "")
        jvn_data.append({"cve_id": cve_id, "jvn_id": jvn_id, "published": published, "lastModified": lastmodified, "description": description, "product": product, "version": version, "cvss": cvss, "impact": impact, "take_measures": take_measures})
    return jvn_data
        
# def extract_nvd(data):
#     if data == {}:
#         return

#     totalresults = data.get('totalResults')
#     resultsperpage = data.get('resultsPerPage')
#     startindex = data.get('startIndex')
#     cves = data.get('vulnerabilities', [])
#     nvd_data = []
#     for _cve in cves:
#         cve = _cve.get('cve', {})

#         cve_id = cve.get('id', "")
#         published = cve.get('published', "")
#         lastmodified = cve.get('lastModified', "")
#         descriptions = cve.get('descriptions', [])
#         cvss_metrics = cve.get('metrics', {})
#         configurations = cve,get('configurations', [])
#         description = ''
#         for d in descriptions:
#             if d.get('lang', "") == 'en':
#                 description = d.get('value', "")
#                 break
#         cvss = []
#         for _cvss_metric in cvss_metrics.values():
#             for cvss_metric in _cvss_metric:
#                 cvss_source = cvss_metric.get('source', "")
#                 cvss_score = cvss_metric.get('cvssData').get('baseScore', "")
#                 cvss_vector = cvss_metric.get('cvssData').get('vectorString', "")
#                 cvss.append({'version': '2.3', 'source': cvss_source, 'score': cvss_score, 'vector': cvss_vector})
#         config = []
#         for __config in configurations:
#             cpe = []
#             for _config in __config.get('nodes', []):
#                 operator = _config.get('operator', "")
#                 negate = _config.get('negate', "")
                
#                 _cpe_match = _config.get('cpeMatch', [])
#                 for cpe_match in _cpe_match:
#                     _cpe = cpe_match.get('criteria', "")
#                     try:
#                         vstart = cpe_match.get('versionStartIncluding', "")
#                         vend = cpe_match.get('versionEndExcluding', "")
#                         cpe.append({'cpe': _cpe, 'versionStart': vstart, 'versionEnd': vend})
#                     except:
#                         cpe.append({'cpe': _cpe})
#                 config.append({'operator': operator, 'negate': negate, 'cpe': cpe})
#         nvd_data.append({'cveid': cve_id, 'published': published, 'lastModified': lastmodified, 'description': description, 'cvss': cvss, 'productInfo': config})
#         return totalresults, resultsperpage, startindex, nvd_data