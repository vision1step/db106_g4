from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import datetime
import time
from random import randrange
import pymongo


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


def read_log_rt():
    with open(log_dir + log_file_name, 'r', encoding='utf-8') as log_file:
        s = log_file.read().split(";")
        if len(s) > 2:
            s = s[1].lstrip("{").rstrip("}").split(',')
            log_dict = {}
            for i in s:
                key = i.split(":")[0].strip().replace("\'","")
                value = i.split(":")[1].strip().replace("\'","")
                log_dict[key]=value
            return log_dict
        else:
            return {}

# connect to mongodb
# mng = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = mng["newsdb"]


# Initial setup for crawler and file directory
# Build up file directories and the files for data and log
to_dir = './'+'moneydj'+'/'
log_dir = to_dir+'log/'
mkpath_check(to_dir)
mkpath_check(log_dir)
mkfile_check(to_dir+'News_Data.txt', 'data')
log_file_name = 'Log_realtime.txt'
mkfile_check(log_dir+'Log_realtime.txt', 'log')

# Get start pages from log file
log_dict = read_log_rt()
if not log_dict:
    log_dict = {'article_time': int(datetime.timestamp(datetime.now()))}
    page = 1
else:
    page = int(log_dict['page'])
print(log_dict)

# Setting
url = 'https://www.moneydj.com/KMDJ/RssCenter.aspx?svc=NR&fno=1&arg=MB010000'
host = 'https://www.moneydj.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/80.0.3987.100 Safari/537.36'}

res = requests.get(url, headers=headers)
soup = bs(res.text, 'html.parser')
news_title = soup.select('title')[1:]
news_url = soup.select('description')[1:]
news_time = soup.select('pubDate')
print(len(news_title), len(news_time), len(news_url))
for i, each_url in enumerate(news_url):
    a_url = str(each_url).split('"')[1]
    a_res = requests.get(a_url, headers=headers)
    a_soup = bs(a_res.text, 'html.parser')
    a_title = news_title[i].text
    a_time = news_time[i].text

    content = a_soup.select('article[id="MainContent_Contents_mainArticle"] p')
    a_soup.select('div[class="viewer_lg"]')[0].text.replace('\n', '').replace('\r', '').split(')')[-1]
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

    # log = {'time': datetime.timestamp(datetime.now()),
    #        'article_time': str_to_timestamp(a_time),
    #        'page': page,
    #        'article_title': a_title}
    print(article)
    # if int(str(log['article_time'])[0:-2]) > int(log_dict['article_time'][0:-2]):
    #     with open(to_dir+'News_Data.txt', 'a', encoding="utf-8") as file:
    #         file.write(str(article)+';')
    #         file.close()
    #     with open(log_dir+log_file_name, 'a', encoding='utf-8') as log_file:
    #         log_file.write(str(log)+';')
    #         log_file.close()