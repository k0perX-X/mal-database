import lxml
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import os
import pandas as pd
import codecs
from bs4 import BeautifulSoup
import numpy as np

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
# urls = ['0']
# with codecs.open('latest/urls.txt', 'r', 'utf-16') as f:
#     for line in f:
#         urls.append(line[:-1])
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
    def cleaning_str(s):
        while s.find('  ') != -1:
            s = s.replace('  ', ' ')
        if s[0] == ' ':
            s = s[1:]
        if s[-1] == ' ':
            s = s[:-1]
        return s

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
        name = cleaning_str(name)
    except:
        error += 'Name, '
    try:
        score_rank = page.xpath('//*[@class="numbers ranked"]/strong')[0].text.replace('#', '')
        score_rank = cleaning_str(score_rank)
    except:
        error += 'Score_rank, '
    try:
        popularity_rank = page.xpath('//*[@class="numbers popularity"]/strong')[0].text.replace('#', '')
        popularity_rank = cleaning_str(popularity_rank)
    except:
        error += 'Popularity_rank, '
    try:
        score = page.xpath('//*[@class="fl-l score"]/div')[0].text
        score = cleaning_str(score)
    except:
        error += 'Score, '
    try:
        # link = urls[int(path[path.rindex('/') + 1:-5])]
        link = page.xpath('//*[@class="breadcrumb "]/div[3]/a')[0].get('href')
    except Exception as e:
        error += f'Link, {e}'
    try:
        j = 10
        for i in stats.find_all("div", class_="spaceit_pad"):
            if 'Watching:' in i.text:
                watching = i.text.replace('Watching: ', '')
                watching = cleaning_str(watching)
            elif 'Completed:' in i.text:
                completed = i.text.replace('Completed: ', '')
                completed = cleaning_str(completed)
            elif 'On-Hold:' in i.text:
                on_hold = i.text.replace('On-Hold: ', '')
                on_hold = cleaning_str(on_hold)
            elif 'Dropped:' in i.text:
                dropped = i.text.replace('Dropped: ', '')
                dropped = cleaning_str(dropped)
            elif 'Plan to Watch:' in i.text:
                plan_to_watch = i.text.replace('Plan to Watch: ', '')
                plan_to_watch = cleaning_str(plan_to_watch)
            elif 'Total:' in i.text:
                total = i.text.replace('Total: ', '')
                total = cleaning_str(total)
            # elif 'votes' in i.text:
            #     j -= 1
            #     print(i.text)
            #     scores[j] = i.text[i.text.find('(') + 1: i.text.rindex('votes') - 1]
            elif 'English:' in i.text:
                english = i.text.replace('English: ', '').replace('\n', '')
                english = cleaning_str(english)
            elif 'Synonyms:' in i.text:
                synonyms = i.text.replace('Synonyms: ', '').replace('\n', '')
                synonyms = cleaning_str(synonyms)
            elif 'Japanese:' in i.text:
                japanese = i.text.replace('Japanese: ', '').replace('\n', '')
                japanese = cleaning_str(japanese)
    except Exception as e:
        error += f'stats, '
    try:
        for i in stats.find_all("table", class_="score-stats"):
            splitted = i.text.split('\n')
            for i in range(len(splitted)):
                if splitted[i].isnumeric():
                    scores[int(splitted[i]) - 1] = \
                        splitted[i + 1][splitted[i + 1].find('(') + 1: splitted[i + 1].rindex('votes') - 1]
        for i in range(len(scores)):
            try:
                scores[i] = cleaning_str(scores[i])
            except:
                pass
    except:
        error += f'scores, '
        error_scores = True
    try:
        for i in page.xpath('//*[@id="content"]/table/tr/td[1]/div/div'):
            s = ''.join(i.itertext())
            if 'Type:' in s:
                type_anime = s.replace('\n', '').replace('Type:', '').replace('  ', ' ')
                while type_anime.find('  ') != -1:
                    type_anime = type_anime.replace('  ', ' ')
                if type_anime[0] == ' ':
                    type_anime = type_anime[1:]
            if 'Episodes:' in s:
                episodes = s.replace('\n', '').replace('Episodes:', '').replace('  ', ' ')
                while episodes.find('  ') != -1:
                    episodes = episodes.replace('  ', ' ')
                if episodes[0] == ' ':
                    episodes = episodes[1:]
            if 'Status:' in s:
                status = s.replace('\n', '').replace('Status:', '').replace('  ', ' ')
                while status.find('  ') != -1:
                    status = status.replace('  ', ' ')
                if status[0] == ' ':
                    status = status[1:]
            if 'Aired:' in s:
                aired = s.replace('\n', '').replace('Aired:', '').replace('  ', ' ')
                while aired.find('  ') != -1:
                    aired = aired.replace('  ', ' ')
                if aired[0] == ' ':
                    aired = aired[1:]
            if 'Premiered:' in s:
                premiered = s.replace('\n', '').replace('Premiered:', '').replace('  ', ' ')
                while premiered.find('  ') != -1:
                    premiered = premiered.replace('  ', ' ')
                if premiered[0] == ' ':
                    premiered = premiered[1:]
            if 'Broadcast:' in s:
                broadcast = s.replace('\n', '').replace('Broadcast:', '').replace('  ', ' ')
                while broadcast.find('  ') != -1:
                    broadcast = broadcast.replace('  ', ' ')
                if broadcast[0] == ' ':
                    broadcast = broadcast[1:]
            if 'Producers:' in s:
                producers = s.replace('\n', '').replace('Producers:', '').replace('  ', ' ')
                while producers.find('  ') != -1:
                    producers = producers.replace('  ', ' ')
                if producers[0] == ' ':
                    producers = producers[1:]
            if 'Licensors:' in s:
                licensors = s.replace('\n', '').replace('Licensors:', '').replace('  ', ' ')
                while licensors.find('  ') != -1:
                    licensors = licensors.replace('  ', ' ')
                if licensors[0] == ' ':
                    licensors = licensors[1:]
            if 'Studios:' in s:
                studios = s.replace('\n', '').replace('Studios:', '').replace('  ', ' ')
                while studios.find('  ') != -1:
                    studios = studios.replace('  ', ' ')
                if studios[0] == ' ':
                    studios = studios[1:]
            if 'Source:' in s:
                source = s.replace('\n', '').replace('Source:', '').replace('  ', ' ')
                while source.find('  ') != -1:
                    source = source.replace('  ', ' ')
                if source[0] == ' ':
                    source = source[1:]
            if 'Genres:' in s:
                genres = s.replace('\n', '').replace('Genres:', '').replace('  ', ' ')
                while genres.find('  ') != -1:
                    genres = genres.replace('  ', ' ')
                if genres[0] == ' ':
                    genres = genres[1:]
                genres1 = genres
                genres = ''
                for i in genres1.split(', '):
                    if i[:len(i)//2] == i[len(i)//2:]:
                        genres += i[:len(i)//2] + ', '
                    else:
                        genres += i + ', '
                genres = genres[:-2]
            if 'Duration:' in s:
                duration = s.replace('\n', '').replace('Duration:', '').replace('  ', ' ')
                while duration.find('  ') != -1:
                    duration = duration.replace('  ', ' ')
                if duration[0] == ' ':
                    duration = duration[1:]
            if 'Rating:' in s:
                rating = s.replace('\n', '').replace('Rating:', '').replace('  ', ' ')
                while rating.find('  ') != -1:
                    rating = rating.replace('  ', ' ')
                if rating[0] == ' ':
                    rating = rating[1:]
            if 'Favorites:' in s:
                favorites = s.replace('\n', '').replace('Favorites:', '').replace('  ', ' ')
                while favorites.find('  ') != -1:
                    favorites = favorites.replace('  ', ' ')
                if favorites[0] == ' ':
                    favorites = favorites[1:]
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


pool = ThreadPool(100)
results = list(pool.map(append, paths))
# results = list(map(append, paths))

for result in results:
    df = df.append(result, ignore_index=True)
df = df.replace('None found, add some ', np.NAN).replace('None ', np.NAN)\
    .replace('Unknown ', np.NAN).replace('N/A', np.NAN)
df['Members On-Hold'] = df['Members On-Hold'].str.replace(',', '')
df['Members Total'] = df['Members Total'].str.replace(',', '')
df['Members Watching'] = df['Members Watching'].str.replace(',', '')
df['Members Completed'] = df['Members Completed'].str.replace(',', '')
df['Members Dropped'] = df['Members Dropped'].str.replace(',', '')
df['Members Plan to Watch'] = df['Members Plan to Watch'].str.replace(',', '')
df['Members Favorites'] = df['Members Favorites'].str.replace(',', '')
for i in df.columns:
    df[i] = df[i].str.replace('\n', '')

if not os.path.exists(f'csv'):
    os.mkdir(f'csv')
df.to_csv(f'csv/{date}.csv')
