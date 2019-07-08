# coding=utf-8
import datetime
import urllib
import urllib.request
from queue import Queue
from threading import Thread
import json
from bs4 import BeautifulSoup


class Consumer(Thread):
    # Producer 的任务是获取信息,放到queue
    def __init__(self, queue, infos):
        Thread.__init__(self)
        # 队列,用于线程间通信
        self.queue = queue
        self.infos = infos
        # 用于存放所有信息
        self.active = True

    def run(self):
        while True:
            # 获取页面:延迟很多的
            url0 = self.queue.get()  # 从队列中获得信息
            try:
                html0 = self.getHtml(url0)
                # 使用BeautifulSoup创建html代码的BeautifulSoup实例，存为soup0
                soup0 = BeautifulSoup(html0, "html.parser")
                # 获取尾页（对照前一小节获取尾页的内容看你就明白了）
                total_tr = soup0.find("table", class_="table_yjfx").findAll("tr")
            except Exception as e:
                #print(e)
                pass

            for i in range(2, 52, 5):
                try:
                    raw = []
                    total_td = total_tr[i].findAll("td")
                    for t in total_td:
                        raw.append(t.get_text())
                    raw.append(total_tr[i + 1].findAll("td")[1].get_text())
                    raw.append(total_tr[i + 2].findAll("td")[1].get_text())
                    raw.append(total_tr[i + 3].findAll("td")[1].get_text())
                    raw.append(total_tr[i + 4].findAll("td")[1].get_text())
                    json_raw = json.dumps(raw)
                    self.infos.add(json_raw)
                except:
                    continue

            # 睡眠2s
            self.queue.task_done()  # 每次get后需要调用task done ,直到所有任务都task done ,join才取消

    def getHtml(self, url):
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
            #print(e)
            pass

if __name__ == "__main__":
    queue = Queue()  # 队列对象
    infos = set()
    starttime = datetime.datetime.now()
    # 生产者

    with open("pageinfos.json", "r", encoding="utf-8") as fread:
        line = fread.readline()
        list_info = json.loads(line)
        for info in list_info:
            for page in range(1, (int(info[1]) + 1)):
                url0 = "http://www.letpub.com.cn/index.php?page=grant&name=&person=&no=&company=&startTime=" + info[0] + "&endTime=" + info[0] + "&money1=&money2=&" \
                       "subcategory=&addcomment_s1=&addcomment_s2=&addcomment_s3=" + info[2] + "&addcomment_s4=&currentpage=" + str(page) + "#fundlisttable"
                queue.put(url0)

    print(queue.qsize())

    # 消费者
    for i in range(100):
        worker = Consumer(queue, infos)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    queue.join()

    # print(worker.infos)
    print(len(worker.infos))

    # save as json
    lt_infos = list(worker.infos)
    with open("page.json", "w", encoding="utf-8") as fwrite:
        for json_str in lt_infos:
            fwrite.write(json_str + "\n")
    with open("page1.json", "w", encoding="utf-8") as fwrite:
        fwrite.write(json.dumps(lt_infos))

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
