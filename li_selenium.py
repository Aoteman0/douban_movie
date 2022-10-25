# coding=gbk
from selenium import webdriver
from myran import Myran
from selenium.webdriver.common.by import By
import time
from mongo_db import MyMongoClient

option = webdriver.ChromeOptions()
option.add_argument("--disable-extensions")  # ������չ
# option.add_argument('--incognito')  # ����ģʽ���޺�ģʽ�� ������ץ����
option.add_argument("--disable-software-rasterizer")  # ����3D��դ����
option.add_argument('--no-sandbox')  # ���DevToolsActivePort�ļ������ڵı���
#option.add_argument("--disable-gpu")  # �ȸ����GPU����
option.add_experimental_option("excludeSwitches", ["enable-automation"])  # ������վ���selenium ������ģʽ����
option.add_experimental_option('useAutomationExtension', False)  # ȥ����ʾ�Կ�����ģʽ����
#option.page_load_strategy = 'none'  # �������������������������ִ��
# prefs = {"profile.managed_default_content_settings.images": 2}
# option.add_experimental_option("prefs", prefs)#������ͼģʽ
option.add_argument('blink-settings=imagesEnabled=false')  # ������ͼƬ, �����ٶ�
option.add_argument("User-Agent=%s" % Myran().agents())  # ��ͷģʽ��Ҫ�������ͷ
#option.add_argument("--headless")  # ������ͷģʽ
option.add_argument("--window-size=1024,768")  # ��ͷģʽ���ô��ڴ�С
#option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome.exe --remote-debugging-port=9222


#����������첽��������  ����selenium������ȡ
class Alltype:
    def data(self):
        type_list=['m_type','m_place','m_year']
        type_dict = {}
        with webdriver.Chrome(options=option) as driver:
            driver.get("https://movie.douban.com/explore")
            driver.implicitly_wait(10)
            base_title_list  = driver.find_elements(By.XPATH,"//div[@class='base-selector-title']")

            for i in range(3):
                #print(base_title.get_attribute("textContent"))
                base_title_list[i].click()
                type_dict[type_list[i]] = list()
                time.sleep(1)
                driver.implicitly_wait(10)
                li_list = driver.find_elements(By.XPATH, "//div[@class='expand-card']/div/div/ul/li")
                for li in li_list[1:]:
                    type_dict[type_list[i]].append(li.get_attribute("textContent"))
                    #print(li.get_attribute("textContent"))
        return type_dict

    def parse(self):
        type_dict = self.data()

        meta_list=[]
        for m_type in type_dict["m_type"]:
            for m_place in type_dict["m_place"]:
                for m_year in type_dict["m_year"]:
                    meta_m = {}
                    meta_m["selected_categories"]='{"����":"%s","����":"%s"}'%(m_place,m_type)
                    meta_m['tags']="%s,%s,%s"%(m_year,m_type,m_place)
                    mongo.insert_one(meta_m)
                    meta_list.append(['{"����":"%s","����":"%s"}'%(m_place,m_type),"%s,%s,%s"%(m_year,m_type,m_place)])

        return meta_list
mongo=MyMongoClient('type')
if __name__ == '__main__':
    aa=Alltype()
    aa.parse()
