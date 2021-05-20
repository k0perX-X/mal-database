import requests
import lxml
from lxml import etree
import codecs

headers = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

error_file = open('latest/urls_errors.txt', 'r')
url_file = codecs.open('latest/urls.txt', 'a', 'utf-16')
errors = []

for url in error_file:
    print(url)
    first = True
    res = requests.get(url, headers=headers)
    tree = lxml.etree.fromstring(res.text, parser=lxml.etree.HTMLParser())
    if tree.xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/table/tr') is None:
        errors.append(url)
        print('error')
    for row in tree.xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/table/tr'):
        if first:
            first = False
        else:
            url_file.write(row.xpath('td[2]/div/div[2]/h3/a')[0].get("href") + '\n')

error_file.close()
url_file.close()

with open('latest/urls_errors.txt', 'w') as f:
    for url in errors:
        f.write(url + '\n')
