import requests
import json

headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
stocknumber = int
query = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{}.tw'.format(stocknumber)
session = requests.session()
response = requests.get(query, headers=headers)
content = json.loads(response.text)
'股票名稱' = content['msgArray'][0]['n']
'時間' = content['msgArray'][0]['t']
'昨日收盤價' = content['msgArray'][0]['y']
'開盤價' = content['msgArray'][0]['o']
'最高價' = content['msgArray'][0]['h']
'最低價' = content['msgArray'][0]['l']
'上市櫃' = content['msgArray'][0]['ex']
'最近成交價' = content['msgArray'][0]['z']
'最新交易成交張數' = content['msgArray'][0]['tv']
'當日成交量' = content['msgArray'][0]['v']
'五檔報價賣出價' = [i for i in content['msgArray'][0]['a'].split('_')][0:-1]
'五檔報價賣出量' = [i for i in content['msgArray'][0]['f'].split('_')][0:-1]
'五檔報價買入價' = [i for i in content['msgArray'][0]['b'].split('_')][0:-1]
'五檔報價買入量' = [i for i in content['msgArray'][0]['g'].split('_')][0:-1]
'漲停點' = content['msgArray'][0]['u']
'跌停點' = content['msgArray'][0]['w']
