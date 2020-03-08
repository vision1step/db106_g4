import json
#import pandas as pd

with open(r"filepath",'r',encoding= 'utf-8') as load_f:
    load_dict = json.load(load_f)
    content = load_dict['content']

#df = pd.read_json(r"filepath")

