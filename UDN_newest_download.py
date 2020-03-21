import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
ss = requests.session()

path = r'./res_money_udn'
if not os.path.exists(path):
    os.mkdir(path)

for i in range(0,1):
    # url = 'https://money.udn.com/rank/newest/1001/0/'+str(i)
    url = 'https://money.udn.com/money/breaknews/1001/0//' + str(i)
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # title = soup.select('div[id="ranking_body"] a')
    ttlpage = soup.select('span[class="total"]')[0].text
    # ttlpage = str(ttlpage)
    ttlnum = ''.join([x for x in str(ttlpage) if x.isdigit()])
    ttlnum = int(ttlnum)
    # title = soup.select('div[id="ranking_body"] a')[0]
    #print(title)

    for i in range(1, ttlnum):
        url = 'https://money.udn.com/money/breaknews/1001/0//' + str(i)
        #     url = 'https://money.udn.com/rank/newest/1001/0/1'

        res = ss.get(url, headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.select('div[id="ranking_body"] a')
        print("==============================第 "+ str(i) + "/" + str(ttlnum) +" 頁=============================")
        ttl_content = ""
        for each_title in title:
            # print(each_title.text+": "+each_title['href'])
            try:
                article_url = each_title['href']
                # article_url = title['href']
                # article_url = 'https://money.udn.com/money/story/5621/4337347'
                print(article_url)
                res_article = ss.get(article_url, headers=headers)
                article_soup = BeautifulSoup(res_article.text, 'html.parser')
                # content = article_soup.select('div[id="story_body"]')
                story_art_time = article_soup.select('div[class="shareBar__info--author"] span')[0].text
                if not story_art_time.replace('-','').replace(':','').replace(' ','').isdigit(): continue
                story_art_title = article_soup.select('h2[id="story_art_title"]')[0].text
                story_artile_body = article_soup.select('div[id="article_body"] p')#多個
                story_art_body = ""
                for i in story_artile_body: story_art_body += i.text
                story_art_body = story_art_body.replace("\r","").replace("\n","").strip()
                story_art_url  = article_url
                story_art_hit  = article_soup.select('span[class="_5n6h _2pih"]') if article_soup.select('span[class="_5n6h _2pih"]') else 0
                story_artile_keywd = article_soup.select('div[id="story_tags"] a') #多個
                story_art_keywd = "" ; count = 0
                for i in story_artile_keywd:
                    count += 1
                    # print("count: "+str(count)+"  "+"len: "+str(len(story_artile_keywd)))
                    if len(story_artile_keywd) > 1 and count <= len(story_artile_keywd)-1 :
                        story_art_keywd =story_art_keywd + i.text+","
                        # print("if")
                    # if i < len(story_artile_keywd) & len(story_artile_keywd) > 1 : story_art_keywd =story_art_keywd + story_artile_keywd(i).text+","
                    # elif story_artile_keywd.index()+1 = len(story_artile_keywd): story_art_keywd =story_art_keywd + i.text
                    else:
                        story_art_keywd =  story_art_keywd + i.text
                        #story_art_keywd = story_art_keywd[0]
                        # print("else")
                # print(story_art_time)
                # print(story_art_title)
                # print(story_art_body)
                # print(story_art_url)
                # print(story_art_hit)
                # print(story_art_keywd)
                content ="""{\n"時間":"%s",\n"新聞標題":"%s",\n"內文":"%s",\n"出處":"%s",\n"點擊數":%s,\n"關鍵字":[%s]\n}"""\
                            % (story_art_time,story_art_title,story_art_body,story_art_url,story_art_hit,story_art_keywd)
                print(content)
                # ttl_content += content
                time.sleep(8)

                with open(path + '/' + each_title.text + '.json', 'w', encoding='utf8') as f:
                    f.write(content)
            except KeyError as e:
                print(e.args)
            except:
                print(each_title.text)
                continue
        # with open(path + '/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.json', 'w', encoding='utf8') as f:
        #     f.write(ttl_content)
        #
        # ttl_content = ""
