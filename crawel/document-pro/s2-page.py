# coding=utf-8
import datetime
import urllib
import urllib.request
from queue import Queue
from threading import Thread
import json
from bs4 import BeautifulSoup
import re
import random
import time
# 导入pymysql模块
import pymysql

# 批量插入数据，定义在消费者中会出现异常
# 连接database
conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="fund", charset="utf8")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()

def sqlSelectAll():
    sql = "select s2_code from s2"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        s2_code=[]
        for row in results:
            s2_code.append(row[0])
        return s2_code
    except Exception as e:
        print(e)

def sqlUpdate(raws):
    for raw in raws:
        try:
            year="year"+raw[0]
            sql = "update s2 set "+year+"=%s where s2_code=%s"
            cursor.execute(sql, raw[1:])
        except Exception as e:
            print(e)
            continue
    # 提交事务
    conn.commit()

def getHtml(url):
    # 获取文字页面返回html信息
    try:
        req0 = urllib.request.Request(url)
        # 使用add_header设置请求头，将代码伪装成浏览器
        req0.add_header("User-Agent",
                        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        # 使用urllib.request.urlopen打开页面，使用read方法保存html代码
        html0 = urllib.request.urlopen(req0).read()
        return html0
    except Exception as e:
        print(e)

if __name__ == "__main__":
    urls=[]
    infos = []
    starttime = datetime.datetime.now()
    # 生产者
    code_all=sqlSelectAll()
    ltTime_all = ["1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
              "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]
    for t in ltTime_all:
        for c in code_all:
            infos.append([t,"",c])
            url0 = "http://www.letpub.com.cn/index.php?page=grant&name=&person=&no=&company=&startTime="+t+"&endTime="+t+"&money1=&money2=&" \
           "subcategory=&addcomment_s1=&addcomment_s2=&addcomment_s3="+c+"&addcomment_s4=&currentpage="+str(1)+"#fundlisttable"
            urls.append(url0)

    for i in range(len(urls)):
        try:
            html0 = getHtml(urls[i])
            # 使用BeautifulSoup创建html代码的BeautifulSoup实例，存为soup0
            soup0 = BeautifulSoup(html0, "html.parser")
            total_page_html = soup0.find("center").div.string
            total_page = total_page_html.split("共")[1].split("页")[0]
            infos[i][1]=str(total_page)
        except Exception as e:
            print(e)
            continue

    with open("pageinfos.json", "w", encoding='utf-8') as fwrite:
        dict_str = json.dumps(infos)
        fwrite.write(dict_str)

    sqlUpdate(infos)

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)

    # 关闭游标、数据库
    cursor.close()
    conn.close()
