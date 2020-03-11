import requests
from bs4 import BeautifulSoup
import os
import json
import re
import time
def req(url,headers):
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def find_final(soup):
    finalpage = soup.select('div[class="pagination boxTitle"]  a[data-desc="最後一頁"]')[0]['href']
    finalpage_number = re.search(r"\d+",finalpage)[0]
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

headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
path =r'./ltn_strategy/%s'
if not os.path.exists(r'./ltn_strategy'):
    os.mkdir(r'./ltn_strategy')
url_list = 'https://ec.ltn.com.tw/list/strategy'
session = requests.session()
soup_list = req(url_list ,headers)
finalpage_number = find_final(soup_list)
session.close()
breaktoken = 0 
for i in range(1,int(finalpage_number)+1):
    if breaktoken != 0:
        break
    try:
        url_indexed_list = 'https://ec.ltn.com.tw/list/strategy/' + str(i)
        soup = req(url_indexed_list, headers)
        for t in range(0, 3):
            title, output = content_header(soup, t)
            if os.path.exists(path % (title) + '.json'):
                break
            file_save(path, title)
    except:
        print('there are no news on the header')
    url_indexed_list = 'https://ec.ltn.com.tw/list/strategy/' + str(i)
    soup = req(url_indexed_list, headers)
    for k in range(len(soup.select('div[data-desc="文章列表"] a[class="boxText"] div[class="tit"] p'))):
        title, output = content(soup, k)
        if os.path.exists(path % (title) + '.json'):
            breaktoken += 1
            break
        file_save(path, title)
        time.sleep(1)
session.close()
