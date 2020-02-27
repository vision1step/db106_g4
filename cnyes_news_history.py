import requests
import os
import json
import time
import datetime
year = 2017
path = r'./cnyesnewshistory'+r'/'+str(year)+r'/%s'
if not os.path.exists(r'./cnyesnewshistory'+r'/'+str(year)):
    os.mkdir(r'./cnyesnewshistory'+r'/'+str(year))
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

for i in range(1,12):
    starttime = int(datetime.datetime(year, i, 1).timestamp())
    endtime = int(datetime.datetime(year, i+1, 1).timestamp())
    timerange = [starttime,endtime]
    url_news_index = 'https://news.cnyes.com/api/v3/news/category/tw_stock?startAt=%s&endAt=%s' %(timerange[0],timerange[1])
    session = requests.session()
    response = session.get(url_news_index, headers = headers)
    index_json = response.json()
    lastpage = int(index_json['items']['last_page'])
    session.close()
    for l in range(1,lastpage+1):
        url_news_page = 'https://news.cnyes.com/api/v3/news/category/tw_stock?startAt=%s&endAt=%s&page=%d' % (
        timerange[0], timerange[1], l)
        response_news = session.get(url_news_page, headers = headers)
        news_page_json = response_news.json()
        data_perpage = len(news_page_json['items']['data'])
        for n in range(data_perpage):
            title = str(news_page_json['items']['data'][n]['title']).replace('<',' ').replace('>',' ').replace('/','').replace('＃','').replace('?','').replace('*','_').replace('\"','_').replace(':','_').replace('\n','_')
            if not os.path.exists(path %(title)):
                article_id = str(news_page_json['items']['data'][n]['newsId'])
                content_url = 'https://news.cnyes.com/api/v6/news/' + article_id
                date = time.ctime(news_page_json['items']['data'][n]['publishAt'])
                content_response = session.get(content_url, headers = headers)
                content_json = content_response.json()
                content = content_json['items']['content']
                tag = content_json['items']['keywords']
                href = 'https://news.cnyes.com/news/id/' + article_id
                output = {'date':date,'title':title,'content':content,'href':href,'tag':tag}
                session.close()
                with open(path %(title) + '.json', 'w', encoding='utf8') as f:
                    json.dump(output,f)
