import pymongo
import dns
client = pymongo.MongoClient("mongodb+srv://db_106_user:stockdb106@cluster0-iocac.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.json
tagjson = db.news.find({},{'_id':0,'tag':1})
tagset = set()
querynum = tagjson.count()
print(f'this query contain {querynum} data')
for tags in tagjson:
    try:
        tag = tags['tag']
        if type(tag) == str:
            tagset.add(tag)
        if type(tag) == list:
            for i in range(len(tag)):
                tagset.add(tag[i])
    except Exception as e:
        print(e.args[0])
print(tagset)