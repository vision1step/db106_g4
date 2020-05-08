import os
import json
import requests
from bs4 import BeautifulSoup

def crawler(sUrl,sHeaders,sFilter):
    req = requests.get(url = sUrl, headers = sHeaders)
    soup = BeautifulSoup(req.text, 'html.parser')
    listContent = soup.select(sFilter)
    return listContent

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

url = 'https://www.chinatimes.com/money/realtimenews?page=1&chdtv'
content = ''
counter = 0
keyword = ''
# url_list=[]
resource_path = r'./chinatimes'
url_storage_path = r'url_storage.txt'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

if os.path.exists(url_storage_path):
    url_file = open(url_storage_path, 'r', encoding='utf-8')
    url_list = url_file.readlines()
    # url_file.close()
    print("該url_stroage檔案已存在。")
    # print(str(type(url_list)))
else:
    url_file = open(url_storage_path, 'w+', encoding='utf-8')
    url_list = url_file.readlines()
    # url_file.close()
    print("該url_stroage檔案不存在。")
    # print(str(type(url_list)))

pages = function.crawler(url, headers, 'ul[class="pagination"] a[class="page-link"]')
# print("url索引長度："+str(len(pages)))

for index in range(0, len(pages) - 1):
    title = function.crawler(url, headers, 'h3[class="title"] a')
    for each_title in title:

        sTitle = each_title.text.replace('/', r'月')
        print(sTitle)
        try:
            article_url = r'https://www.chinatimes.com' + each_title['href']
            print(article_url)

            if article_url + str('\n') not in url_list:
                print("寫入：" + article_url)
                url_list.append(str(article_url) + '\n')
                url_file = open(url_storage_path, 'w', encoding='utf-8')
                url_file.writelines(url_list)
                url_file.close()

                article = function.crawler(article_url, headers, 'div[class="article-body"] p')
                # print("article_content的資料型態："+str(type(article)))
                for article_content in article:
                    # print(article_content.text)
                    content = content + article_content.text

                date_soup = function.crawler(article_url, headers, 'div[class="meta-info"] time')
                date = date_soup[0]['datetime']
                # print(date)

                source_soup = function.crawler(article_url, headers, 'div[class="source"]')
                source = source_soup[0].text
                # print(source)

                keyword_soup = function.crawler(article_url, headers,
                                                'div[class="article-hash-tag"] span[class="hash-tag"]')
                for key in keyword_soup:
                    keyword = keyword + key.text + ", "

                file = open(resource_path + '/' + sTitle, "w+", encoding='utf-8')
                output = [{'Time': date}, {'Title': each_title.text}, {'Content': content}, {'From': source},
                          {'KeyWord:': keyword}]
                json.dump(output, file, ensure_ascii=False)
                file.close()
                counter = counter + 1
            else:
                print("此資料已抓取過。")

        except KeyError as e:
            print(e.args)
        print()

    url = 'https://www.chinatimes.com' + str(pages[index]['href']) + '&chdtv'
    # print('修改後的url：'+url)