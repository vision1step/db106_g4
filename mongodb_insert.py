import json
import pymongo
import dns
import os
dirpath = ''
files = os.listdir(dirpath)
dbname =
collection =
for file in files:
    try:
        with open(dirpath+'\\'+'%s'% (file), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                load_dict = json.loads(line)
                client = pymongo.MongoClient(
                    "mongodb+srv://db_106_user:stockdb106@cluster0-iocac.gcp.mongodb.net/test?retryWrites=true&w=majority")
                db = client.dbname
                db.collection.insert_one(load_dict)
    except Exception as e:
        print(e.args[0])