import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

def req(url,headers):
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def content(soup,n):
    title = soup.select('a[class="_1Zdp"]')[n]['title'].replace('<',' ').replace('>',' ').replace('/','').replace('＃','').replace('?','').replace('*','_').replace('\"','_').replace(':','_').replace('\n','_')
    article_id = soup.select('a[class="_1Zdp"]')[n]['href']
    id = article_id.split('/')[-1]
    href = 'https://news.cnyes.com' + article_id
    date = soup.select('a[class="_1Zdp"]')[n].time['datetime']
    content_url = 'https://news.cnyes.com/api/v6/news/' + id
    content_response = session.get(content_url, headers=headers)
    content_json = content_response.json()
    tag = content_json['items']['keywords']
    content = content_json['items']['content']
    content = text_clean(content)
    output = {'date': date, 'title': title, 'content': content, 'href': href, 'tag': tag, 'clicks': 'NA'}
    time.sleep(1)
    return title, output

def text_clean(content):
    if re.search(r'(<a.+?a>)', content) != None:
        content = re.sub(r"(\(<a.+?a>\))", '', content, count=0, flags=re.IGNORECASE)
    if re.search(r'(&l.+?gt;)', content) != None:
        content = re.sub(r'(&l.+?gt;)', '', content, count=0)
    if re.search(r'(&a.+?sp;)', content) != None:
        content = re.sub(r'(&a.+?sp;)', '', content, count=0)
    if re.search(r'(\n)', content) != None:
        content = content.replace('\r', '')
        content = content.replace('\n', '')
    return content

def file_save(path,title):
    with open(path % (title) + '.json', 'w', encoding='utf8') as f:
        json.dump(output, f)


if not os.path.exists(r'./cnyesnewstoday'):
    os.mkdir(r'./cnyesnewstoday')
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
url_news_index = 'https://news.cnyes.com/news/cat/tw_stock?exp=a'
session = requests.session()
soup = req(url_news_index, headers)
path =r'./cnyesnewstoday/%s'
for n in range(len(soup.select('a[class="_1Zdp"]'))):
    title, output = content(soup,n)
    if os.path.exists(path %(title) + '.json'):
        break
    if not os.path.exists(path %(title)):
        file_save(path, title)
session.close()
