#coding=utf-8
import requests
from myran import Myran
from lxml import etree
from multiprocessing import Queue
import threading
import re
import os

myran=Myran()
class Data(threading.Thread):
    def __init__(self):
        super(Data, self).__init__()
        self.headers = {
                'User-Agent':myran.agents()
            }
        self.url='http://www.ddzimu.com'
    def geturl(self,m_name):
        data={
            "key":m_name
        }
        try:
            response = requests.get("http://www.ddzimu.com/download/xslist.php?",headers=self.headers,params=data)
            print(response.status_code)
            if response.status_code==200:
                #print(response.text)
                htmlxpath = etree.HTML(response.text)
                t_url=htmlxpath.xpath('//div[contains(@class,"info")]/div[contains(@class,"pianmang")]/a/@href')
                if t_url==[]:
                    raise  Exception("没找到'%s'的字幕"%m_name)
                main_url=self.url+t_url[0]

                result = self.parse(main_url)
                print(result)
                if result:
                    rsp = requests.get(result['url'],headers=self.headers)
                    hz = os.path.splitext(re.findall(r"filename=(.*?)',",str(rsp.headers))[0])[1]
                    #
                    if hz in '.ass|.ssa|.srt':filename = hz.replace('.', '')
                    else:filename='zip'
                    with open('zimu/'+filename+'/'+m_name+hz,'wb') as f:
                        f.write(rsp.content)
                    print("下载完成！")

        except Exception as e:
            print(e.__traceback__.tb_lineno,e)
    def parse(self,main_url):
        try:
            rsp = requests.get(main_url,headers=self.headers)
            hxpath = etree.HTML(rsp.text)
            li_list = hxpath.xpath("//div[contains(@class,'listbox')]/div[contains(@class,'list')]/ul/li[position()>1]")

            result={}
            for li in li_list:
                zm_type = li.xpath("div[1]/span/text()")[0]
                print('zm_type',zm_type)
                place = li.xpath("div[2]/img/@title")
                downurl = li.xpath("div[1]/a/@href")[0]
                #print("zm_type",zm_type)
                if re.findall(r'ass|ssa|srt',zm_type,re.I):

                    if len(place)==1 and '简体' in str(place[0]):
                            result["url"]=downurl
                            break
                    elif len(place)>1 and '简体' in str(place[0]):
                        result['url']=downurl
                    else:
                        result['url']=downurl
            return result
        except Exception as e:
            print(e.__traceback__.tb_lineno,e)
if __name__ == '__main__':
    data = Data()
    data.geturl("大内密探零零发")