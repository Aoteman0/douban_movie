import requests
from myran import Myran
import json
from mongo_db import MyMongoClient
import random,time
from li_selenium import Alltype

myran = Myran()
mongo_xjcol = MyMongoClient('xjcol')
mongo_type = MyMongoClient('type')
alltype=Alltype()
def appmain(start,count,*args):
    url='https://m.douban.com/rexxar/api/v2/movie/recommend'
    xpath = "//div[@class='explore']/div/ul/li"
    try:
        meta={
            'refresh':'0',
            'start':str(start),
            'count':str(count),
            'selected_categories':args[0],
            'uncollect':'false',
            'tags':args[1]
        }
        headers = {
            'Cookie':'ll="118281"; bid=7DqLNDuk6JA; ap_v=0,6.0; __utma=30149280.506682031.1666155704.1666155704.1666155704.1; __utmb=30149280.0.10.1666155704; __utmc=30149280; __utmz=30149280.1666155704.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=6d07c66be7a9ed09-2201e0655bd700a6:T=1666155714:RT=1666155714:S=ALNI_MYjr6lFh2EplHVP7rpyMHQ6D-PCow; __gpi=UID=00000b65bbf3e6c0:T=1666155714:RT=1666155714:S=ALNI_Mb_BF-n7C0AcE7DlCNJ63IU78OmKg',
            'Referer':'https://movie.douban.com/explore',
            'User-Agent':myran.agents()
        }
        proxies = {
            "http":"127.0.0.1:10809",
            "https":"127.0.0.1:10809"
        }

        session = requests.session()
        response = session.get(url=url,headers=headers,params=meta)
        gaoxiao_dict = json.loads(response.text)
        gaoxiao_items = gaoxiao_dict['items']
    except Exception as e:
        print(e.__traceback__.tb_lineno,args[1],e)
    if gaoxiao_items:
        for item in gaoxiao_items:
            try:
                movie_dict ={}
                movie_dict['mid'] = item.get('id')
                movie_dict['title'] = item.get('title')
                rating = item.get('rating')
                if rating:movie_dict['scores'] = rating.get('value')
                else:movie_dict['scores']='0'
                movie_dict['year'] = item.get('year')
                movie_dict['card_subtitle'] = item.get('card_subtitle')
                print(movie_dict)
                mongo_xjcol.insert_one(movie_dict)
            except Exception as e:
                print(e.__traceback__.tb_lineno,movie_dict['title'],e)
    else:
        raise Exception('item值为空')
if __name__ == '__main__':
    type_dict_list = []
    try:
        for i in mongo_type.findall():
            type_dict_list.append(i)
        id = mongo_type.find('60年代,动画,意大利').next()["_id"]
        for type_dict in type_dict_list:
            if type_dict["_id"] > id:
                print(type_dict)
                start = 0
                while True:
                    try:
                        num = random.choice(list(range(2, 5))) + random.random()
                        time.sleep(num)
                        appmain(start,20,type_dict["selected_categories"],type_dict["tags"])
                        start += 20
                    except Exception as e:
                        #print(e.__traceback__.tb_lineno,e)
                        print('start:', start)
                        break
    except Exception as e:
        print(e.__traceback__.tb_lineno,e)
