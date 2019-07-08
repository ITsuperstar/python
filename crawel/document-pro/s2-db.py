# coding=utf-8
# 导入pymysql模块
import pymysql

# 连接database
conn = pymysql.connect(host="127.0.0.1", user="root",password="root",database="fund",charset="utf8")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
sql = "INSERT INTO s2(s2_code ,s2_name) VALUES (%s, %s);"

all=[]
with open('国家自然科学基金申请代码.txt', encoding='utf-8') as fread:
    lines = fread.readlines()
    for line in lines:
        raw=[]
        lsp=line.split()
        for temp in lsp:
            if temp:
                raw.append(temp)
        if raw:
            all.append(raw)
# print(all)
# print(len(all))
#统计二级学科代码共有多少个
n=0
for code in all:
    if len(code[0])==5:
        n=n+1
print(n)

num = 0
for j in range(len(all)):
    try:
        if len(all[j][0])==5:
            cursor.execute(sql, all[j])
            num = num + 1
    except:
        print("数据库插入异常！")
        continue

# 提交事务
conn.commit()

# 关闭游标、数据库
cursor.close()
conn.close()