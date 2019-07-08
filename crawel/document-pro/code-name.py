# coding=utf-8

all=[]
with open('国家自然科学基金申请代码.txt', encoding='utf-8') as fread:
    lines = fread.readlines()
    for line in lines:
        raw=[]
        lsp=line.split()
        for temp in lsp:
            if temp:
                print(temp,len(temp))
                raw.append(temp)
        if raw:
            all.append(raw)
print(len(all))