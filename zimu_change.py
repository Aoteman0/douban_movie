#coding=utf-8
import os
import re
from chardet import detect

def app(filepath):
    try:
        with open(filepath, 'rb') as f:
            result=f.read()
            encoding = detect(result)['encoding'] #获取二进制文件 编码格式
            if encoding=='GB2312':encoding='GBK'
            if encoding=='Big5':encoding='big5hkscs'

            #安原编码解码后再用utf-8编码  最后按utf-8解码
            result=result.decode(encoding).encode('utf-8').decode('utf-8')

            #print(result)
        #print("filepath", filepath)
        hz = filepath.split('.')[2]
        #print("hz",hz)
        result_list=[]
        if hz  in "ass|ssa":
            result_list=re.findall(r'Dialogue: 0,0:(.*?),.*?0,,(.*)[\r]',re.sub(r'{.*}','',result))
            #print(hz)
        elif hz in "srt":
            result_list=re.findall(r'.*\n(.*?)[,.]\d+ --> .*\n(.*)[\r]',re.sub(r'{.*}','',result))
            #print(hz)
        #print("result_list",result_list)
        if len(result_list)!=0:
            for i in result_list:
                print(i)
        else:
            raise Exception('正则没找到',filepath)
    except Exception as e:
        print(e.__traceback__.tb_lineno,e,filepath,encoding)
if __name__ == '__main__':
    pathlist = ['./zimu/ass/', './zimu/srt/']
    for path in pathlist:
        for i in os.listdir(path):
            bashpath = '%s%s' % (path, i)
            app(bashpath)