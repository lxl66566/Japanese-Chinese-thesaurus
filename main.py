import json
import os
import pandas as pd
from tqdm import tqdm

findic = {}

def for_json():         #首先对所有json文件进行处理
    def deal_json(path):
        global findic
        with open(path,encoding = 'utf-8') as f:
            data = json.load(f)['data']
            for i in data:
                findic[i["wordName"]] = i["wordDesc"]

    for root, dirs, files in os.walk(os.path.dirname(__file__), topdown=False):
        for name in files:
            if name.find('.json') == -1:
                continue
            s1 = str(os.path.join(root, name))
            deal_json(s1)

def for_xlsx():
    global findic
    # pd_frame = pd.read_excel('jp_zhongji.xlsx')
    # for i in tqdm(range(len(pd_frame))):
    #     jp_words = pd_frame.iloc[i]['日文']
    #     kana = pd_frame.iloc[i]['假名']
    #     meaning = pd_frame.iloc[i]['中文']
    #     word_type = pd_frame.iloc[i]['类型']
    #     voc = pd_frame.iloc[i]['发音']
    #     if isinstance(kana, float) == False:
    #         temp = ['(',kana,voc,') ',word_type,' ',meaning]
    #         if isinstance(voc,float) == True:
    #             temp.pop(temp.index(voc))
    #         if isinstance(word_type,float) == True:
    #             temp.pop(temp.index(word_type))
    #         s = ''.join(temp)
    #         findic[jp_words] = s
    pd_frame = pd.read_excel('ABAB.xlsx')
    for i in tqdm(range(len(pd_frame))):
        jp_words = pd_frame.iloc[i]['副词']
        meaning = pd_frame.iloc[i]['意思']
        findic[jp_words] = meaning

def for_csv():
    global findic
    pd_frame = pd.read_excel('words.xlsx')#先将原csv手动转为xlsx，再处理
    for i in tqdm(range(len(pd_frame))):
        kanji = pd_frame.iloc[i]['kanji'].strip()
        kana = pd_frame.iloc[i]['kana'].strip()
        desc = pd_frame.iloc[i]['desc'].strip()
        pos = pd_frame.iloc[i]['pos'].strip()
        if kana.find('@') != -1:
            kana = ''.join(list(kana.split('@')))
        if isinstance(kanji, float) == False:
            s = ''.join(['(',kana,') ',pos,' ',desc])
            findic[kanji] = s
        else:
            if kana[-1].isdigit:
                kana.pop(-1)
            s = ''.join([pos,' ',desc])
            findic[kana] = s

def for_grammar():
    global findic
    pd_frame = pd.read_excel('grammar.xlsx')#先将原csv手动转为xlsx，再处理
    for i in tqdm(range(len(pd_frame))):
        expression = pd_frame.iloc[i]['expression']
        explanation = pd_frame.iloc[i]['explanation']
        shortexplain = pd_frame.iloc[i]['shortexplain']
        try:
            expression = expression.strip()
        except AttributeError:
            pass
        try:
            explanation = explanation.strip()
        except AttributeError:
            pass
        try:
            shortexplain = shortexplain.strip()
        except AttributeError:
            pass

        if isinstance(explanation, float) == False and explanation.strip() != '':
            findic[expression] = explanation
        elif isinstance(shortexplain, float) == False and shortexplain.strip() != '':
            findic[expression] = shortexplain

def for_js1():#将js文件转化为json（字符处理
    with open('word-list2.txt','r',encoding='utf-8') as f:
        s = f.readlines()
        print(len(s))
    l = []
    for i in s:
        for j in range(len(i)):
            if i[j] is '}':
                l.pop(-1)
                l.pop(-1)
            l.append(i[j])
    with open('word-list-.txt','w',encoding='utf-8') as f:
        f.write(''.join(l))

def for_js2():#进一步处理json为一般格式
    global findic
    with open('word-list-.txt',encoding='utf-8') as f:
        l = json.load(f)['_']
    for i in l:
        i["content"] = i["content"].strip()
        i['pron'] = i['pron'].strip()
        if i["content"] == i['pron']:
            findic[i["content"]] = i['definition']
        else:
            try:
                findic[i["content"]] = ''.join(['(',i['pron'],i['tone'],') ',i['definition']])
            except KeyError:
                findic[i["content"]] = ''.join(['(',i['pron'],') ',i['definition']])

def merge():
    global findic
    filenme = os.listdir(os.path.dirname(__file__))
    for i in filenme:
        if i.find('.json') != -1:
            with open(i,encoding='utf-8') as f:
                findic.update(json.load(f))

if __name__ == '__main__':
    merge()
    with open('final.json','w',encoding='utf-8') as fin:
        json.dump(findic,fin,indent = 4,sort_keys = True,ensure_ascii=False)
