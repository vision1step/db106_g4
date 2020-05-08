import sys
import os
import jieba
from pymongo import MongoClient
import json

client = MongoClient('mongodb://hannibal:`1q@192.168.1.109/news')
db = client["news"]
collect = db["moneydj"]

filter1 = {"source":"https://www.moneydj.com"}
result = collect.find(filter1)

jieba.load_userdict('./mydict.txt')
# source_path = './chinatimes/'
# flist = os.listdir(source_path)#列出所有檔案
source_path = sys.path.append("./read_mongo")
Company = open(r'./company.txt',encoding='utf-8')
Company_list = Company.readlines()

'''
for line in sCompany:
    # print(line, end='')
    print(line)
'''

sb = ''


for i in result:
    #i['content']：內文
    sContent = i['content']
    #print(sContent)

    for j in Company_list:
        if j.strip() in sContent:
            print(j.strip() + "：比對到。")
            sb += j.strip().replace('\n', ' ')
            break


sb_cut = jieba.cut(sb)
wc = {}
for w in sb_cut:
    if len(w) < 2:
        continue
    if w in wc:
        wc[w] += 1
    else:
        wc[w] = 1

wc_list = [(w, wc[w]) for w in wc]
wc_list.sort(key = lambda x: x[1], reverse = False)
print(wc_list)
f = open('company_frequency.txt','w',encoding='utf-8')
f.writelines(str(wc_list))
f.close()



# source_path = './chinatimes/'
# flist = os.listdir(source_path)#列出所有檔
#
# sb = ''
# for f in flist:
#     with json.loads(source_path + f, 'r') as ff:
#         sb += ff.read().replace('\n', ' ')
#
# sb_cut = jieba.cut(sb)
#
# wc = {}
# for w in sb_cut:
#     if len(w) < 2:
#         continue
#     if w in wc:
#         wc[w] += 1
#     else:
#         wc[w] = 1
#
# wc_list = [(w, wc[w]) for w in wc]
# wc_list.sort(key = lambda x: x[1], reverse = True)
# print(wc_list)
