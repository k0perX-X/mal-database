import requests
from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import codecs
from bs4 import BeautifulSoup

step = int(sys.argv[1])

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
errors = []


def anime_dic(url: tuple):
    url, number_anime = url[0], url[1]

    def get_page(link):
        return requests.get(link, headers=headers).text

    pool1 = ThreadPool(2)
    anime_page_res_stats, anime_page_res = pool1.map(get_page, [url + '/stats', url])
    try:
        soup = BeautifulSoup(anime_page_res, features="html.parser")
        if soup.find(class_='title-name h1_bold_none') is None:
            raise IndexError
        soup = BeautifulSoup(anime_page_res_stats, features="html.parser")
        if soup.find(class_='title-name h1_bold_none') is None:
            raise IndexError
        with codecs.open(f'latest/pages/{((number_anime - 1) // step) * step}/{number_anime}_stats.html', 'w', 'utf-16') as f:
            f.write(anime_page_res_stats)
        with codecs.open(f'latest/pages/{((number_anime - 1) // step) * step}/{number_anime}.html', 'w', 'utf-16') as f:
            f.write(anime_page_res)
        return None
    except IndexError:
        print(str(number_anime) + " " + url + '\n', end='')
        return number_anime
    except Exception as e:
        print(str(number_anime) + " " + url + str(e) + '\n', end='')
        return number_anime


for dir in os.listdir('latest/pages'):
    if os.path.isdir('latest/pages/' + dir):
        if os.path.isfile(f'latest/pages/{dir}/errors.txt'):
            with open(f'latest/pages/{dir}/errors.txt', 'r') as error_file:
                for line in error_file:
                    errors.append(int(line))
            os.remove(f'latest/pages/{dir}/errors.txt')

if os.path.isfile('latest/pages/download_errors.txt'):
    with open('latest/pages/download_errors.txt', 'r') as error_file:
        for line in error_file:
            errors.append(int(line))
    os.remove('latest/pages/download_errors.txt')

i = 0
j = 0
urls = []
with codecs.open('latest/urls.txt', 'r', 'utf-16') as urls_file:
    for url in urls_file:
        i += 1
        if i in errors:
            j += 1
            if j > step:
                break
            urls.append((url[:-1], i))
            errors.remove(i)
            # print(i, url)

pool = ThreadPool(20)
results = list(pool.map(anime_dic, urls))

while None in results:
    results.remove(None)

results = results + errors

if len(results) > 0:
    with open(f'latest/pages/download_errors.txt', 'w') as error_file:
        for i in results:
            error_file.write(str(i) + '\n')
