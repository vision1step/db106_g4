import requests
from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime, timedelta, date
import time
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
path =r'./ltn_weeklybiz/%s'
if not os.path.exists(r'./ltn_weeklybiz'):
    os.mkdir(r'./ltn_weeklybiz')
session = requests.session()
url_indexed_list = 'https://ec.ltn.com.tw/list/weeklybiz'
finalpage_number = 0
try:
    response = session.get(url_indexed_list, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    finalpage = soup_list.select('div[class="pagination boxTitle"]  a[data-desc="最後一頁"]')[0]['href']
    finalpage_number = int(re.findall('\d+', finalpage)[1])
    session.close()
except:
    print('only 1 page')
    pass
if finalpage_number == 0:
    try:
        response_list = session.get(url_indexed_list, headers=headers)
        soup = BeautifulSoup(response_list.text, 'html.parser')
        for t in range(0, 3):
            title = soup.select('div[class="listphoto"] a[class]')[t].text.replace('/', '_').replace('<',' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r", '_').replace('\\','_').replace('\n', '_')
            href = soup.select('div[class="listphoto"] a')[t]['href']
            clicks = "NA"
            tag = "NA"
            content_text = ''
            content_response = session.get(href, headers=headers)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            date = content_soup.select('div[class="text"] span[class="time"]')[0].text
            for j in content_soup.select('p'):
                if len(j.text) > 2:
                    content_text += j.text
            output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag,'clicks': clicks}
            with open(path % (title) + '.json', 'w', encoding='utf8') as f:
                json.dump(output, f)
    except:
        print('there are no news on the header')
    response_list = session.get(url_indexed_list, headers=headers)
    soup = BeautifulSoup(response_list.text, 'html.parser')
    for k in range(len(soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p'))):
        href = soup.select('div[data-desc="文章列表"] a[class="boxText"]')[k]['href']
        title = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p')[k].text.replace('/', '_').replace('<', ' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r",'_').replace('\\', '_').replace('\n', '_')
        date = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] span')[k].text
        clicks = "NA"
        tag = "NA"
        content_text = ''
        content_response = session.get(href, headers=headers)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        for j in content_soup.select('p'):
            if len(j.text) > 2:
                content_text += j.text
        output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag,'clicks': clicks}
        with open(path % (title) + '.json', 'w', encoding='utf8') as f:
            json.dump(output, f)
        time.sleep(1)
else:
    try:
        response_list = session.get(url_indexed_list, headers=headers)
        soup = BeautifulSoup(response_list.text, 'html.parser')
        for t in range(0, 3):
            title = soup.select('div[class="listphoto"] a[class]')[t].text.replace('/', '_').replace('<',' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r", '_').replace('\\','_').replace('\n', '_')
            href = soup.select('div[class="listphoto"] a')[t]['href']
            clicks = "NA"
            tag = "NA"
            content_text = ''
            content_response = session.get(href, headers=headers)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            date = content_soup.select('div[class="text"] span[class="time"]')[0].text
            for j in content_soup.select('p'):
                if len(j.text) > 2:
                    content_text += j.text
            output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag,
                      'clicks': clicks}
            with open(path % (title) + '.json', 'w', encoding='utf8') as f:
                json.dump(output, f)
    except:
        print('there are no news on the header')
    response_list = session.get(url_indexed_list, headers=headers)
    soup = BeautifulSoup(response_list.text, 'html.parser')
    for i in range(1, int(finalpage_number) + 1):
        url_indexed_list = 'https://ec.ltn.com.tw/list/weeklybiz/' + '/' + ref_date.strftime('%Y%m%d') + '/' + str(
            i)
        print('currently in page ' + str(i))
        response_list = session.get(url_indexed_list, headers=headers)
        soup = BeautifulSoup(response_list.text, 'html.parser')
        for t in range(0, 3):
            title = soup.select('div[class="listphoto"] a[class]')[t].text.replace('\n', '')
            href = soup.select('div[class="listphoto"] a')[t]['href']
            clicks = "NA"
            tag = "NA"
            content_text = ''
            content_response = session.get(href, headers=headers)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            date = content_soup.select('div[class="text"] span[class="time"]')[0].text
            for j in content_soup.select('p'):
                if len(j.text) > 2:
                    content_text += j.text
            output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag,
                      'clicks': clicks}
            with open(path % (title) + '.json', 'w', encoding='utf8') as f:
                json.dump(output, f)
        for k in range(len(soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p'))):
            href = soup.select('div[data-desc="文章列表"] a[class="boxText"]')[k]['href']
            title = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p')[k].text.replace('/','_').replace('<', ' ').replace('>', ' ').replace('/', '').replace('＃', '').replace('?', '').replace("\r",'_').replace('\\', '_').replace('\n', '_')
            date = soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] span')[k].text
            clicks = "NA"
            tag = "NA"
            content_text = ''
            content_response = session.get(href, headers=headers)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            for j in content_soup.select('p'):
                if len(j.text) > 2:
                    content_text += j.text
            output = {'date': date, 'title': title, 'content': content_text, 'href': href, 'tag': tag,
                      'clicks': clicks}
            with open(path % (title) + '.json', 'w', encoding='utf8') as f:
                json.dump(output, f)
            time.sleep(1)