from confluent_kafka import Producer
import sys
import time
import requests
import json

def get_liveprice(no):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
    stocknumber = no
    query = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{}.tw'.format(stocknumber)
    session = requests.session()
    response = session.get(query, headers=headers)
    content = json.loads(response.text)
    股票名稱 = content['msgArray'][0]['n']
    時間 = content['msgArray'][0]['t']
    昨日收盤價 = content['msgArray'][0]['y']
    開盤價 = content['msgArray'][0]['o']
    最高價 = content['msgArray'][0]['h']
    最低價 = content['msgArray'][0]['l']
    上市櫃 = content['msgArray'][0]['ex']
    最近成交價 = content['msgArray'][0]['z']
    最新交易成交張數 = content['msgArray'][0]['tv']
    當日成交量 = content['msgArray'][0]['v']
    五檔報價賣出價 = [i for i in content['msgArray'][0]['a'].split('_')][0:-1]
    五檔報價賣出量 = [i for i in content['msgArray'][0]['f'].split('_')][0:-1]
    五檔報價買入價 = [i for i in content['msgArray'][0]['b'].split('_')][0:-1]
    五檔報價買入量 = [i for i in content['msgArray'][0]['g'].split('_')][0:-1]
    漲停點 = content['msgArray'][0]['u']
    跌停點 = content['msgArray'][0]['w']
    return 股票名稱, 時間, 昨日收盤價, 開盤價, 最高價, 最低價

def error_cb(err):
    print('Error: %s' % err)

def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        if int(msg.key()) % 5 == 0:
            sys.stderr.write('%% Message delivered to topic:[{}]\n'.format(msg.topic()))

if __name__ == '__main__':
    props = {
        'bootstrap.servers': 'localhost:9092',
        'error_cb': error_cb,
        'retries' : '3',
        'max.in.flight.requests.per.connection' : '1'
    }
    producer = Producer(props)
    topicName = 'stock'
    try:
        no = '2330'
        股票名稱, 時間, 昨日收盤價, 開盤價, 最高價, 最低價 = get_liveprice(str(no))
        content = f'股票名稱:{股票名稱}, 時間:{時間}, 昨日收盤價:{昨日收盤價}, 開盤價:{開盤價}, 最高價:{最高價}, 最低價:{最低價}'
        while True:
            producer.produce(topicName, key=no, value=content,callback=delivery_callback)
            producer.poll(0)
            print("messages have received by broker", end="\r")
            time.sleep(4)
        print(f'Send {no}'  + ' messages to Kafka')
    except BufferError as e:
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    producer.flush(5)
    print('Message sending completed!')