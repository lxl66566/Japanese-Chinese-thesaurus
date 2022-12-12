import json
s = {}
with open('nihonngo_for_final.json','r',encoding='utf-8') as f:
    s = json.load(f)
with open('nihonngo_for_final.json','w',encoding='utf-8') as f:
    json.dump(s,f,indent = 4,sort_keys = True,ensure_ascii=False)