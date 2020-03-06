import json
#import pandas as pd

with open(r"filepath",'r',encoding= 'utf-8') as load_f:
    load_dict = json.load(load_f)
    content = load_dict['content']

#df = pd.read_json(r"filepath")

import pymongo
import dns
client = pymongo.MongoClient("mongodb+srv://db_106_user:stockdb106@cluster0-iocac.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.json
db.news.insert_one(load_dict)
