import json
with open("pageinfos.json","r",encoding="utf-8") as fread:
    line=fread.readline()
    list_info=json.loads(line)
    num=0
    for info in list_info:
        num=num+int(info[1])
        if int(info[1])>50:
            print(info)

    print(num)