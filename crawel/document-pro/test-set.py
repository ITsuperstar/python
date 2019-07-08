import json
s=set()
s.add(json.dumps(["ss","dd"]))
s.add(json.dumps(["ss","dd"]))
s.add(json.dumps(["ss","dsd"]))
s.add(json.dumps(["ss","ddd"]))
print(s)
print(list(s))

with open("set.json","w",encoding="utf-8") as fwrite:
    json_str=json.dumps(list(s))
    fwrite.write(json_str)
with open("set1.json","w",encoding="utf-8") as fwrite:
    for json_str in s:
        fwrite.write(json_str+"\n")

with open("set.json","r",encoding="utf-8") as fread:
    line = fread.readline()
    list_info = json.loads(line)
    infos=[]
    for info in list_info:
        infos.append(json.loads(info))
    print(list_info)
    print(infos)


with open("pageinfos.json","r",encoding="utf-8") as fread:
    line=fread.readline()
    list_info=json.loads(line)
    print(len(list_info))