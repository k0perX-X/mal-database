import lxml
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import os
import pandas as pd
import codecs
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=[
    'Name',
    'Score rank',
    'Popularity rank',
    'Score',
    'Episodes',
    'Type',
    'Link',
    'Premiered',
    'English name',
    'Japanese name',
    'Synonyms',
    'Status',
    'Aired',
    'Broadcast',
    'Producers',
    'Licensors',
    'Studios',
    'Source',
    'Genres',
    'Duration',
    'Rating',
    'Members Favorites',
    'Members Total',
    'Members Watching',
    'Members Completed',
    'Members On-Hold',
    'Members Dropped',
    'Members Plan to Watch',
    'Members score 10',
    'Members score 9',
    'Members score 8',
    'Members score 7',
    'Members score 6',
    'Members score 5',
    'Members score 4',
    'Members score 3',
    'Members score 2',
    'Members score 1',
])
urls = ['0']
with codecs.open('latest/urls.txt', 'r', 'utf-16') as f:
    for line in f:
        urls.append(line[:-1])
with open(f"latest/date.txt", 'r') as f:
    date = f.read()

paths = []
for dir in os.listdir('latest/pages'):
    if os.path.isdir('latest/pages/' + dir):
        for file in os.listdir('latest/pages/' + dir):
            if os.path.isfile(f'latest/pages/{dir}/{file}'):
                if '_stats' not in file:
                    paths.append(f'latest/pages/{dir}/{file}')
paths.sort(key=lambda x: int(x[x.rindex('/') + 1:-5]))


def append(path):
    with codecs.open(path, 'r', 'utf-16') as f:
        page = lxml.etree.fromstring(f.read(), parser=lxml.etree.HTMLParser())
    with codecs.open(path[:-5] + '_stats.html', 'r', 'utf-16') as f:
        stats = BeautifulSoup(f.read(), 'lxml')
    error = ''
    name = None
    score_rank = None
    popularity_rank = None
    score = None
    link = None
    watching = None
    completed = None
    on_hold = None
    dropped = None
    plan_to_watch = None
    total = None
    english = None
    synonyms = None
    japanese = None
    type_anime = None
    episodes = None
    status = None
    aired = None
    premiered = None
    broadcast = None
    producers = None
    licensors = None
    studios = None
    source = None
    genres = None
    duration = None
    rating = None
    favorites = None
    error_scores = False
    scores = [None for i in range(10)]
    try:
        name = page.xpath('//*[@class="title-name h1_bold_none"]/strong')[0].text
    except:
        error += 'Name, '
    try:
        score_rank = page.xpath('//*[@class="numbers ranked"]/strong')[0].text.replace('#', '')
    except:
        error += 'Score_rank, '
    try:
        popularity_rank = page.xpath('//*[@class="numbers popularity"]/strong')[0].text.replace('#', '')
    except:
        error += 'Popularity_rank, '
    try:
        score = page.xpath('//*[@class="fl-l score"]/div')[0].text
    except:
        error += 'Score, '
    try:
        link = urls[int(path[path.rindex('/') + 1:-5])]
    except:
        error += 'Link, '
    try:
        j = 10
        for i in stats.find_all("div", class_="spaceit_pad"):
            if 'Watching:' in i.text:
                watching = i.text.replace('Watching: ', '')
            elif 'Completed:' in i.text:
                completed = i.text.replace('Completed: ', '')
            elif 'On-Hold:' in i.text:
                on_hold = i.text.replace('On-Hold: ', '')
            elif 'Dropped:' in i.text:
                dropped = i.text.replace('Dropped: ', '')
            elif 'Plan to Watch:' in i.text:
                plan_to_watch = i.text.replace('Plan to Watch: ', '')
            elif 'Total:' in i.text:
                total = i.text.replace('Total: ', '')
            # elif 'votes' in i.text:
            #     j -= 1
            #     print(i.text)
            #     scores[j] = i.text[i.text.find('(') + 1: i.text.rindex('votes') - 1]
            elif 'English:' in i.text:
                english = i.text.replace('English: ', '').replace('\n', '')
            elif 'Synonyms:' in i.text:
                synonyms = i.text.replace('Synonyms: ', '').replace('\n', '')
            elif 'Japanese:' in i.text:
                japanese = i.text.replace('Japanese: ', '').replace('\n', '')
    except Exception as e:
        error += f'stats, '
    try:
        for i in stats.find_all("table", class_="score-stats"):
            splitted = i.text.split('\n')
            for i in range(len(splitted)):
                if splitted[i].isnumeric():
                    scores[int(splitted[i]) - 1] = \
                        splitted[i + 1][splitted[i + 1].find('(') + 1: splitted[i + 1].rindex('votes') - 1]
    except:
        error += f'scores, '
        error_scores = True
    try:
        for i in page.xpath('//*[@id="content"]/table/tr/td[1]/div/div'):
            s = ''.join(i.itertext())
            if 'Type:' in s:
                type_anime = s.replace('\n', '').replace('Type:', '').replace('  ', ' ')
            if 'Episodes:' in s:
                episodes = s.replace('\n', '').replace('Episodes:', '').replace('  ', ' ')
            if 'Status:' in s:
                status = s.replace('\n', '').replace('Status:', '').replace('  ', ' ')
            if 'Aired:' in s:
                aired = s.replace('\n', '').replace('Aired:', '').replace('  ', ' ')
            if 'Premiered:' in s:
                premiered = s.replace('\n', '').replace('Premiered:', '').replace('  ', ' ')
            if 'Broadcast:' in s:
                broadcast = s.replace('\n', '').replace('Broadcast:', '').replace('  ', ' ')
            if 'Producers:' in s:
                producers = s.replace('\n', '').replace('Producers:', '').replace('  ', ' ')
            if 'Licensors:' in s:
                licensors = s.replace('\n', '').replace('Licensors:', '').replace('  ', ' ')
            if 'Studios:' in s:
                studios = s.replace('\n', '').replace('Studios:', '').replace('  ', ' ')
            if 'Source:' in s:
                source = s.replace('\n', '').replace('Source:', '').replace('  ', ' ')
            if 'Genres:' in s:
                genres = s.replace('\n', '').replace('Genres:', '').replace('  ', ' ')
            if 'Duration:' in s:
                duration = s.replace('\n', '').replace('Duration:', '').replace('  ', ' ')
            if 'Rating:' in s:
                rating = s.replace('\n', '').replace('Rating:', '').replace('  ', ' ')
            if 'Favorites:' in s:
                favorites = s.replace('\n', '').replace('Favorites:', '').replace('  ', ' ')
    except Exception as e:
        error += 'page, '
    if not error_scores:
        for i in range(len(scores)):
            if scores[i] is None:
                scores[i] = 0
    if error != '':
        print(error + path + '\n', end='')
    return {
        'Name': name,
        'Score rank': score_rank,
        'Popularity rank': popularity_rank,
        'Score': score,
        'Episodes': episodes,
        'Type': type_anime,
        'Link': link,
        'Premiered': premiered,
        'English name': english,
        'Japanese name': japanese,
        'Synonyms': synonyms,
        'Status': status,
        'Aired': aired,
        'Broadcast': broadcast,
        'Producers': producers,
        'Licensors': licensors,
        'Studios': studios,
        'Source': source,
        'Genres': genres,
        'Duration': duration,
        'Rating': rating,
        'Members Favorites': favorites,
        'Members Total': total,
        'Members Watching': watching,
        'Members Completed': completed,
        'Members On-Hold': on_hold,
        'Members Dropped': dropped,
        'Members Plan to Watch': plan_to_watch,
        'Members score 10': scores[9],
        'Members score 9': scores[8],
        'Members score 8': scores[7],
        'Members score 7': scores[6],
        'Members score 6': scores[5],
        'Members score 5': scores[4],
        'Members score 4': scores[3],
        'Members score 3': scores[2],
        'Members score 2': scores[1],
        'Members score 1': scores[0],
    }


pool = ThreadPool(50)
results = list(pool.map(append, paths))
# results = list(map(append, paths))

for result in results:
    df = df.append(result, ignore_index=True)

if not os.path.exists(f'csv'):
    os.mkdir(f'csv')
df.to_csv(f'csv/{date}.csv')
