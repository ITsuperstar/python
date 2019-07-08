#coding=utf-8

import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import random
import time
# 导入pymysql模块
import pymysql

# 连接database
conn = pymysql.connect(host="127.0.0.1", user="root",password="root",database="fund",charset="utf8")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
sql = "INSERT INTO fund(person ,company, money, project_id, project_type, department, approval_year, subject,  subject_classification, subject_code, execution_time) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

raws=[]
num=0
#重大研究计划 494页
for k in range(1,495):
    page=k
    # 设置目标url，使用urllib.request.Request创建请求
    url0 = "http://www.letpub.com.cn/index.php?page=grant&name=&person=&no=&company=&startTime=1997&endTime=2018&money1=&money2=&" \
           "subcategory=%E9%87%8D%E5%A4%A7%E7%A0%94%E7%A9%B6%E8%AE%A1%E5%88%92&addcomment_s1=&addcomment_s2=&addcomment_s3=&addcomment_s4=&" \
           "currentpage="+str(page)+"#fundlisttable"
    try:
        req0 = urllib.request.Request(url0)

        # 使用add_header设置请求头，将代码伪装成浏览器
        req0.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")

        # 使用urllib.request.urlopen打开页面，使用read方法保存html代码
        html0 = urllib.request.urlopen(req0,timeout=3).read()
    except:
        continue

    # 使用BeautifulSoup创建html代码的BeautifulSoup实例，存为soup0
    soup0 = BeautifulSoup(html0,"html.parser")

    # 获取尾页（对照前一小节获取尾页的内容看你就明白了）
    total_tr = soup0.find("table",class_= "table_yjfx").findAll("tr")

    for i in range(2, 52, 5):
        try:
            raw=[]
            total_td=total_tr[i].findAll("td")
            for t in total_td:
                raw.append(t.get_text())
            raw.append(total_tr[i+1].findAll("td")[1].get_text())
            raw.append(total_tr[i+2].findAll("td")[1].get_text())
            raw.append(total_tr[i+3].findAll("td")[1].get_text())
            raw.append(total_tr[i+4].findAll("td")[1].get_text())
            raws.append(raw)
        except:
            continue


# 执行SQL语句
for j in range(len(raws)):
    try:
        cursor.execute(sql, raws[j])
        num=num+1
        # 提交事务
        conn.commit()
    except:
        continue

print("共写入：",str(num))

cursor.close()
conn.close()