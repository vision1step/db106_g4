import requests
from bs4 import BeautifulSoup
import os
import json
import re
import time
from dateutil.relativedelta import relativedelta, MO
from datetime import date
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
path =r'./ltn_weeklybiz/%s'

if not os.path.exists(r'./ltn_weeklybiz'):
    os.mkdir(r'./ltn_weeklybiz')
session = requests.session()
url_indexed_list = 'https://ec.ltn.com.tw/list/weeklybiz'
finalpage_number = 0

def get_monday():
    today = date.today()
    last_monday = today + relativedelta(weekday=MO(-1))
    return last_monday.strftime('%Y%m%d')

def req(url,headers):
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def fine_final(url,headers):
    soup = req(url, headers)
    finalpage = soup.select('div[class="pagination boxTitle"]  a[data-desc="最後一頁"]')[0]['href']
    finalpage_number = int(re.findall('\d+', finalpage)[1])
    return finalpage_number

def content_header(soup,n):
    title = soup.select('div[class="listphoto"] a[class]')[n].text.replace('/', '_').replace('<', ' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r", '_').replace('\\', '_').replace('\n', '_')
    href = soup.select('div[class="listphoto"] a')[n]['href']
    clicks = "NA"
    tag = "NA"
    content_text = ''
    content_soup = req(href,headers)
    date = content_soup.select('div[class="text"] span[class="time"]')[0].text
    for j in content_soup.select('p'):
        if len(j.text) > 2:
            content_text += j.text
    content_text = content_text.split('\n')[0]
    output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag, 'clicks': clicks}
    return title, output

def content(soup,n):
    href = soup.select('div[data-desc="文章列表"] a[class="boxText"]')[n]['href']
    title = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p')[n].text.replace('/','_').replace('<', ' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r", '_').replace('\\', '_').replace('\n','_')
    date = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] span')[n].text
    clicks = "NA"
    tag = "NA"
    content_text = ''
    content_soup = req(href,headers)
    for j in content_soup.select('p'):
        if len(j.text) > 2:
            content_text += j.text
    content_text = content_text.split('\n')[0]
    output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag, 'clicks': clicks}
    return title, output

def file_save(path,title):
    with open(path % (title) + '.json', 'w', encoding='utf8') as f:
        json.dump(output, f)

monday = get_monday()
try:
    finalpage_number = fine_final(url_indexed_list,headers)
    session.close()
except:
    print('only 1 page')
    pass
if finalpage_number == 0:
    try:
        soup = req(url_indexed_list,headers)
        for t in range(0, 3):
            title, output = content_header(soup,t)
            file_save(path,title)
    except:
        print('there are no news on the header')
    soup = req(url_indexed_list, headers)
    for k in range(len(soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p'))):
        title, output = content(soup,k)
        file_save(path,title)
        time.sleep(1)
else:
    try:
        soup = req(url_indexed_list,headers)
        for t in range(0, 3):
            title, output = content_header(soup, t)
            file_save(path,title)
    except:
        print('there are no news on the header')
    soup = req(url_indexed_list, headers)
    for i in range(1, int(finalpage_number) + 1):
        url = 'https://ec.ltn.com.tw/list/weeklybiz/' + monday + '/' + str(i)
        print('currently in page ' + str(i))
        soup_main = req(url,headers)
        try:
            for t in range(0, 3):
                title, output = content_header(soup_main, t)
                file_save(path, title)
        except:
            print('there are no news on the header')
        for k in range(len(soup_main.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p'))):
            title, output = content(soup_main, k)
            file_save(path, title)
            time.sleep(1)