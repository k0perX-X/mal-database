import requests
import lxml
from lxml import etree
import datetime
from bs4 import BeautifulSoup
import os
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
d = datetime.datetime.today()
if not os.path.exists('latest'):
    os.mkdir('latest')
with open(f"latest/date.txt", 'w') as f:
    f.write(f'{d.day}.{d.month}.{d.year}_{d.hour}-{d.minute}')


f = codecs.open('latest/urls.txt', 'w', 'utf-16')
errors_file = open('latest/urls_errors.txt', 'w')
min_page = 0
max_page = 17800
soup = BeautifulSoup(requests.get(f'https://myanimelist.net/topanime.php?limit={max_page}', headers=headers).text,
                     features="html.parser")
while soup.find(class_='error404') is None:
    max_page += 50
    soup = BeautifulSoup(requests.get(f'https://myanimelist.net/topanime.php?limit={max_page}', headers=headers).text,
                         features="html.parser")

# max_page = 17850
for i in range(min_page, max_page, 50):
    print(i)
    first = True
    res = requests.get(f'https://myanimelist.net/topanime.php?limit={i}', headers=headers)
    tree = lxml.etree.fromstring(res.text, parser=lxml.etree.HTMLParser())
    for row in tree.xpath('//*[@class="top-ranking-table"]/tr'):
        if first:
            first = False
        else:
            f.write(row.xpath('td[2]/div/div[2]/h3/a')[0].get("href") + '\n')
    if first:
        errors_file.write(f'https://myanimelist.net/topanime.php?limit={i}\n')
        print('error')

f.close()
