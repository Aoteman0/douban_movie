# douban_movie 
爬取douban电影信息 爬虫电影字幕 格式化字幕 可以根据字幕搜索经典片段剪辑视频

douban.py  爬取douban电影信息 并且保存到mongodb

downzimu.py  data.geturl("大内密探零零发") 传入影视名称或者豆瓣id 优先下载简体中文 按下载文件类型自动保存到zimu文件夹

li_selenium  用selenium拿到douban电影类型并且保存到mongodb 配合douban.py按类型请求电影json数据

zim_change.py  格式化字幕文件 输出字幕起始时间和字幕
