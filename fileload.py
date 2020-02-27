import json
with open(r"filepath",'r',encoding= 'utf-8') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)
