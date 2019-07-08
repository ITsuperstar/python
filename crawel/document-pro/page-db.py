# coding=utf-8
import json
import pymysql

# 连接database
conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="fund", charset="utf8")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
sql = "INSERT INTO fund(person ,company, money, project_id, project_type, department, approval_year, subject,  subject_classification, subject_code, execution_time) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

def sqlInsert(raws):
    num = 0
    # 批量信息存到Mysq1数据库，一次10000
    for j in range(len(raws)):
        try:
            cursor.execute(sql, raws[j])
            num = num + 1
        except:
            print("数据库插入异常！")
            continue
    # 提交事务
    conn.commit()
    return num

if __name__ == "__main__":
    infos = []
    with open("page.json", "r", encoding="utf-8") as fread:
        line=fread.readline()
        while line:
            infos.append(json.loads(line))
            line = fread.readline()

    print(len(infos))
    # print(infos)
    insert_num=sqlInsert(infos)
    print(insert_num)

    # 关闭游标、数据库
    cursor.close()
    conn.close()