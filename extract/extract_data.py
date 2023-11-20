def extract_jvn(data):
    pass

def extract_nvd(data):
    print(data['totalResults'])
    print(data['resultsPerPage'])
    print(data['startIndex'])
    cve = data['vulnerabilities']['cve']
