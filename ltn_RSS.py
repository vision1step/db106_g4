import requests
from bs4 import BeautifulSoup
import os
import json
import re
import time
path =r'./ltn_RSS/%s'
if not os.path.exists(r'./ltn_RSS'):
    os.mkdir(r'./ltn_RSS')
rss = 'https://news.ltn.com.tw/rss/business.xml'
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
session = requests.session()
response = session.get(rss, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')
session.close()
for n in range(len(soup.select('item'))):
    title = soup.select('item')[n].title.text.replace('/','_').replace('<','_').replace('>','_').replace('\\','_').replace('＃','_').replace('?','_').replace("\r",'_').replace("\n",'_')
    if os.path.exists(path % (title)+ '.json'):
        break
    date = soup.select('item')[n].pubdate.text
    clicks = "NA"
    tag = "NA"
    content_text = ''
    content_url = ''
    try:
        content_url = re.search(r'https://news.ltn.com.tw/news/business/breakingnews/(\d)+', soup.select('item')[n].text)[0]
    except:
        content_url = re.search(r'https://news.ltn.com.tw/news/business/paper/(\d)+', soup.select('item')[n].text)[0]
    response_content = session.get(content_url, headers=headers)
    content_soup = BeautifulSoup(response_content.text, 'html.parser')
    for j in content_soup.select('p'):
        if len(j.text) > 2:
            content_text += j.text
    content_text = content_text.split('\n')[0]
    output = {'date': date, 'title': title, 'content': content_text, 'href': content_url, 'tag': tag, 'clicks': clicks}
    with open(path % (title) + '.json', 'w', encoding='utf8') as f:
        json.dump(output, f)
    time.sleep(3)
session.close()
