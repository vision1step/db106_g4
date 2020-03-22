import requests
from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
import random
import time

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

# path=r'./res_yahoo_news'
#
# if not os.path.exists(path):
#     os.mkdir(path)

#印出程式執行時系統時間字串
now = datetime.now()
nowTime_str = datetime.now().strftime('%Y-%m-%d')
print(now)


#翻頁
for i in range(1,20):
    url = "https://tw.stock.yahoo.com/news_list/url/d/e/N1.html?q=&pg=%s"%i
    siteMark = requests.get(url)
    soup = BeautifulSoup(siteMark.text, 'html.parser')
    title = soup.select('a.mbody')[1::2]
    print("page: "+str(i))



    #印出每篇文章抬頭
    for each_title in title:
        #print(each_title ['href'])
        article_title = each_title.text.replace('【','').replace('/','').replace('】','')
        print(article_title)


        try:
            #隨機停留0-3秒
            timedelay = random.randrange(0,3)
            time.sleep(timedelay)

            #新聞文章連結
            article_url = each_title['href']
            # print(article_url)

            #找出新聞內文及發佈時間
            res_article = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(res_article.text, 'html.parser')
            # print(article_soup.prettify())
            article = article_soup.select('p[class="canvas-atom canvas-text Mb(1.0em) Mb(0)--sm Mt(0.8em)--sm"]')
            # print(article)
            article_time = article_soup.select('time')[0]['datetime'].replace('T',' ').replace('Z','000')
            # print(article_time)
            a_time = datetime.strptime(article_time, '%Y-%m-%d %H:%M:%S.%f')
            a_str = article_time.split(' ')[0]

            #對比程式執行時間與新聞發布時間只抓當天新聞,並將新聞出處做分類
            if nowTime_str == a_str:
                article_type = -1
                for each_paragraph in article[0:-1]:
                    if re.search(r"【時報", each_paragraph.text) is not None:
                        article_type = 1
                    elif re.search(r"【財訊", each_paragraph.text) is not None:
                        article_type = 2
                    elif re.search("MoneyDJ", each_paragraph.text) is not None:
                        print(each_paragraph.text)
                        article_type = 3
                    else:
                        article_type = 4
                    break


                article_body = ''
                if article_type==1:
                    article_body = ''
                    for each_paragraph in article:
                        article_body += each_paragraph.text
                    # print(article_body)
                    print(1)
                elif article_type==2:
                    article_body = ''
                    for each_paragraph in article[0:-2]:
                        article_body += each_paragraph.text
                    # print(article_body)
                    print(2)
                elif article_type== 3:
                    print(3)
                    continue

                else:
                    print(4)
                    for each_paragraph in article:
                        article_body += each_paragraph.text
                    print(article_body)
                    print(article_type)

                #JSON存檔
                article_file = """{
                        "time":"%s",
                        "title":"%s",
                        "content":"%s",
                        "url":"%s"}""" % (article_time, article_title, article_body, article_url)

                    # article_json = json.dumps(article_file)
                    # print(article_json)
                print(article_file)

                with open(r'%s/%s.json' % (r'./res_yahoo_news', article_title), 'w',encoding='utf-8') as w:
                    w.write(article_file)

            else:
                break

        except KeyError as e:
            print(e.args)
        print('==================================================')











