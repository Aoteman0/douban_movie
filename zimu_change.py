#coding=utf-8
import ffmpeg
import re
from chardet import detect

def app(filepath):
    try:
        with open(filepath, 'rb') as f:
            result=f.read()
            encoding = detect(result)['encoding'] #获取二进制文件 编码格式
            if encoding=='GB2312':encoding='GBK'
            #安原编码解码后再用utf-8编码  最后按utf-8解码
            result=result.decode(encoding).encode('utf-8').decode('utf-8')

            print(result)
    except Exception as e:
        print(e.__traceback__.tb_lineno,e)

    hz = filepath.split('.')[1]
    if hz  in "ass|ssa":
        result_list=re.findall(r'Dialogue: 0,0:(.*?),.*?0,,(.*)[\r]',re.sub(r'{.*}','',result))
        print(hz)
    elif hz in "srt":
        result_list=re.findall(r'.*\n(.*?)[,.]\d+ --> .*\n(.*)[\r]',result)
        print(hz)
    print("result_list",result_list)
    for i in result_list:
        print(i)

if __name__ == '__main__':
    app('zimu/srt/大内密探零零发.srt')