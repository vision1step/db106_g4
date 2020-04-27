from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import datetime, date
import time
from random import randrange
import pymongo
import re


# check directory existence and make one if not exist
def mkpath_check(diry):
    if not os.path.exists(diry):
        os.mkdir(diry)


# check log/data file existence and create one if not exist
def mkfile_check(file_dir, file_for):
    if not os.path.exists(file_dir):
        with open(file_dir, 'w', encoding='utf-8') as f:
            if file_for == 'log':
                crawl_log = "Initialization': Crawler log start at %s" % (str(datetime.now().date())) + ';'
                f.write(crawl_log)
            elif file_for == 'data':
                news_data = "Initialization: Crawler start at %s" % (str(datetime.now().date())) + ';'
                f.write(news_data)
            f.close()


def str_to_timestamp(t_str):
    dt_obj = datetime.strptime(t_str, "%Y/%m/%d %H:%M")
    result = datetime.timestamp(dt_obj)
    return result


def read_log(last_log):
    with open(log_dir + last_log, 'r', encoding='utf-8') as log_file:
        s = log_file.read().split(";")
        if len(s) > 2:
            s = s[-2].lstrip("{").rstrip("}").split(',')
            log_dict = {}
            for i in s:
                key = i.split(":")[0].strip().replace("\'","")
                value = i.split(":")[1].strip().replace("\'","")
                log_dict[key]=value
            return log_dict
        else:
            return {}

cli = pymongo.MongoClient("mongodb://hannibal:`1q@localhost:27017/news")
db = cli['news']
news_col = db['moneydj']


# Initial setup for crawler and file directory
# Build up file directories and the files for data and log
to_dir = './'+'moneydj'+'/'
log_dir = to_dir+'log/'
mkpath_check(to_dir)
mkpath_check(log_dir)
# mkfile_check(to_dir+'News_Data.txt', 'data')
log_file_name = '{}-Log.txt'.format(str(date.today()))
mkfile_check(log_dir+log_file_name, 'log')

# Get latest news from log file
td = str(datetime.today().date()) # date of today
if not td == os.listdir(log_dir)[-1].split("-Log.")[0]:
    log_dict = read_log(os.listdir(log_dir)[-1])
else:
    if len(os.listdir(log_dir)) <= 1:
        log_dict = read_log(os.listdir(log_dir)[-1])
    else:
        log_dict = read_log(os.listdir(log_dir)[-2])
page = 1

# Setting
url = 'https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?index1={}&a=MB010000'.format(page)
host = 'https://www.moneydj.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/80.0.3987.100 Safari/537.36'}

# Find maximum number of pages
res = requests.get(url, headers=headers)
soup = bs(res.text, 'html.parser')
max_page = soup.select('table[class="paging3"] td')[-1].a['href'].split("=")[1].split("&")[0]
finish_flag = 0
# print('Total pages of news:' + str(max_page))
print(page)

l_time = news_col.find_one(sort=[("time", -1)])['time']
latest_news = int(str(str_to_timestamp(l_time))[0:-2])
print(latest_news)


for i in range(page, int(max_page)+1):
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    news_title = soup.select('table[class="forumgrid"] tr a')
    for each_title in news_title:
        time.sleep(randrange(1, 3))
        a_url = host + each_title['href']
        a_title = each_title['title']
        a_res = requests.get(a_url, headers=headers)
        a_soup = bs(a_res.text, 'html.parser')

        content = a_soup.select('article[id="MainContent_Contents_mainArticle"] p')
        a_time = a_soup.select('div[class="viewer_lg"]')[0].text.replace('\n', '').replace('\r', '').split(')')[-1]
        a_category = a_soup.select('div[class ="viewer_ft"]')[0].text.split('：')[1].split('‧')

        if len(content) < 2:
            content = a_soup.select('article[id="MainContent_Contents_mainArticle"]')
        a_text = ''
        for each in content:
            a_text += each.text.replace('\n', '').replace('\r', '').strip()

        article = {'url': a_url,
                   'title': a_title,
                   'time': a_time,
                   'source': host,
                   'category': a_category,
                   'content': a_text}

        log = {'time': datetime.timestamp(datetime.now()),
               'article_time': str_to_timestamp(a_time),
               'page': page,
               'article_title': a_title}

        if int(str(str_to_timestamp(a_time))[0:-2]) > latest_news:
            # news_col.insert_one(article)
            print(log)
            # with open(log_dir+log_file_name, 'a', encoding='utf-8') as log_file:
            #     log_file.write(str(log)+';')
            #     log_file.close()
        else:
            finish_flag = 1

    if finish_flag == 1:
        break
    page += 1
    url = 'https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?index1={}&a=MB010000'.format(page)
