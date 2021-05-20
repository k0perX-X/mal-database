import requests
from multiprocessing.dummy import Pool as ThreadPool
import sys
import os
import codecs
from bs4 import BeautifulSoup
import eventlet
eventlet.monkey_patch()


step = int(sys.argv[1])
num = int(sys.argv[2])
if not os.path.exists('latest/pages'):
    os.mkdir('latest/pages')
if not os.path.exists(f'latest/pages/{num}'):
    os.mkdir(f'latest/pages/{num}')

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


def anime_dic(url: tuple):
    url, number_anime = url[0], url[1]

    def get_page(link):
        with eventlet.Timeout(15):
            return requests.get(link, headers=headers).text

    try:
        pool1 = ThreadPool(2)
        anime_page_res_stats, anime_page_res = pool1.map(get_page, [url + '/stats', url])
        soup = BeautifulSoup(anime_page_res, features="html.parser")
        if soup.find(class_='title-name h1_bold_none') is None:
            raise FileExistsError
        soup = BeautifulSoup(anime_page_res_stats, features="html.parser")
        if soup.find(class_='title-name h1_bold_none') is None:
            raise FileExistsError
        with codecs.open(f'latest/pages/{num}/{number_anime}_stats.html', 'w', 'utf-16') as f:
            f.write(anime_page_res_stats)
        with codecs.open(f'latest/pages/{num}/{number_anime}.html', 'w', 'utf-16') as f:
            f.write(anime_page_res)
        return None
    except FileExistsError:
        print(str(number_anime) + " " + url + '\n', end='')
        return number_anime
    except Exception as e:
        print(str(number_anime) + " " + url + str(e) + '\n', end='')
        return number_anime


i = 0
urls = []
with codecs.open('latest/urls.txt', 'r', 'utf-16') as urls_file:
    for url in urls_file:
        i += 1
        if i > num:
            if i > num + step:
                break
            urls.append((url[:-1], i))
            # print(i, url)

pool = ThreadPool(20)
results = list(pool.map(anime_dic, urls))
# results = list(map(anime_dic, urls))

while None in results:
    results.remove(None)

if len(results) > 0:
    with open(f'latest/pages/{num}/errors.txt', 'w') as error_file:
        for i in results:
            error_file.write(str(i) + '\n')
