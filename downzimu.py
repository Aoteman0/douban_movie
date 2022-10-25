#coding=utf-8
import requests
from myran import Myran
from lxml import etree
from multiprocessing import Queue
import threading
import re
import os
from mongo_db import MyMongoClient
from threading import Lock

myran=Myran()
class Data(threading.Thread):
    def __init__(self):
        super(Data, self).__init__()
        self.headers = {
                'User-Agent':myran.agents()
            }
        self.url='http://www.ddzimu.com'
    def run(self):
        while not m_empty:
            try:
                m_name=m_queue.get(False)
                data={
                    "key":m_name['mid']
                }
                #print(m_name)
                try:
                    response = requests.get("http://www.ddzimu.com/download/xslist.php?",headers=self.headers,params=data)
                    #print(response.status_code)
                    if response.status_code==200:
                        #print(response.text)
                        htmlxpath = etree.HTML(response.text)
                        t_url=htmlxpath.xpath('//div[contains(@class,"info")]/div[contains(@class,"pianmang")]/a/@href')
                        if t_url==[]:
                            raise  Exception("没找到'%s'的字幕"%m_name['title'])
                        main_url=self.url+t_url[0]
                        self.parse(main_url,m_name)

                except Exception as e:
                    print(e.__traceback__.tb_lineno,e)
            except:
                pass
    def parse(self,main_url,m_name):
        try:
            rsp = requests.get(main_url,headers=self.headers)
            hxpath = etree.HTML(rsp.text)
            li_list = hxpath.xpath("//div[contains(@class,'listbox')]/div[contains(@class,'list')]/ul/li[position()>1]")

            result= {'url1':0,'url2':0,'url3':0}
            for li in li_list:
                try:
                    zm_type = li.xpath("div[1]/span/text()")[0]
                    print('zm_type',zm_type)
                    place = li.xpath("div[2]/img/@title")
                    downurl = li.xpath("div[1]/a/@href")[0]
                    #print("zm_type",zm_type)
                    if re.findall(r'ass|ssa|srt',zm_type,re.I):

                        if len(place)==1 and '简体' in str(place[0]):
                                result['url1']=downurl
                        elif len(place)>1 and '简体' in str(place[0]):
                            result['url2']=downurl
                        else:
                            result['url3']=downurl
                except Exception as e:
                        print(e.__traceback__.tb_lineno, e)
            #{'url1':0,'url2':0,'url3':0} 分为三个优先级 遍历所有
            print(result)
            for rst in result:
                if result[rst]!=0:
                    try:
                        rsp = requests.get(result[rst], headers=self.headers)
                        hz = os.path.splitext(re.findall(r"filename=(.*?)',", str(rsp.headers))[0])[1]
                        if hz in '.ass|.ssa|.srt':
                            filename = hz.replace('.', '')
                        else:
                            filename = 'zip'
                        filepath='zimu/%s/%s%s' % (filename, m_name['title'], hz)
                        #print("filepath",filepath)
                        with lock:
                            if not os.path.exists(filepath):
                                with open(filepath, 'wb') as f:
                                    f.write(rsp.content)
                                print("下载完成！还剩%s" % m_queue.qsize())
                            else:print("字幕文件已存在",filepath)
                            break
                    except Exception as e:
                        print(e.__traceback__.tb_lineno, e)
        except Exception as e:
            print(e.__traceback__.tb_lineno,e)
            
m_queue=Queue()
m_empty=False
lock=Lock()
def app():
    global m_empty
    mongo = MyMongoClient("xjcol")
    #筛选时间>2010 分数>0 包涵"中国"、"喜剧"关键词的电影
    dict1 = {'year': {'$gt': '2010'}, 'scores': {'$gt': 0}, 'card_subtitle': {'$regex': "中国.*喜剧"}}
    result = mongo.find_2(dict1)
    for i in result:
        i['title'] = i['title'].encode('gbk', 'ignore').decode('gbk')
        if not os.path.exists('./zimu/ass/%s.ass'%i['title']) and not os.path.exists('./zimu/srt/%s.srt'%i['title']) and not os.path.exists('./zimu/zip/%s.zip'%i['title']) and not os.path.exists('./zimu/zip/%s.rar'%i['title']):
            m_queue.put(i)
    print("m_queue大小：",m_queue.qsize())
    m_threadname_list = ['线程%s' % s for s in range(1, 10 if m_queue.qsize() > 5 else m_queue.qsize())]
    m_thread_list = []
    for m_threadname in m_threadname_list:
        data = Data()
        data.start()
        m_thread_list.append(data)
    while not m_queue.empty():
        pass
    m_empty = True
    for m_thread in m_thread_list:
        m_thread.join()
        print('线程%s结束了' % m_thread.getName())
if __name__ == '__main__':
    app()


    #data.geturl()