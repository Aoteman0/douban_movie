# coding=gbk
from selenium import webdriver
from myran import Myran
from selenium.webdriver.common.by import By
import time
from mongo_db import MyMongoClient

option = webdriver.ChromeOptions()
option.add_argument("--disable-extensions")  # 禁用拓展
# option.add_argument('--incognito')  # 隐身模式（无痕模式） 开启会抓不了
option.add_argument("--disable-software-rasterizer")  # 禁用3D光栅化器
option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
#option.add_argument("--disable-gpu")  # 谷歌禁用GPU加速
option.add_experimental_option("excludeSwitches", ["enable-automation"])  # 避免网站检测selenium 开发者模式调用
option.add_experimental_option('useAutomationExtension', False)  # 去掉提示以开发者模式调用
#option.page_load_strategy = 'none'  # 不等它加载完所有组件就往下执行
# prefs = {"profile.managed_default_content_settings.images": 2}
# option.add_experimental_option("prefs", prefs)#设置无图模式
option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
option.add_argument("User-Agent=%s" % Myran().agents())  # 无头模式下要添加请求头
#option.add_argument("--headless")  # 设置无头模式
option.add_argument("--window-size=1024,768")  # 无头模式设置窗口大小
#option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome.exe --remote-debugging-port=9222


#导航栏点击异步加载内容  采用selenium进行爬取
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
                    meta_m["selected_categories"]='{"地区":"%s","类型":"%s"}'%(m_place,m_type)
                    meta_m['tags']="%s,%s,%s"%(m_year,m_type,m_place)
                    mongo.insert_one(meta_m)
                    meta_list.append(['{"地区":"%s","类型":"%s"}'%(m_place,m_type),"%s,%s,%s"%(m_year,m_type,m_place)])

        return meta_list
mongo=MyMongoClient('type')
if __name__ == '__main__':
    aa=Alltype()
    aa.parse()
