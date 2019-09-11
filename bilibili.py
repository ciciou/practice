#-*-coding: utf-8 -*-
#author:cici
import requests
import time
import random
#获取网页原数据
def get_json(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    params={
       'page_size':10,
        'next_offset':str(num),
        'tag':'今日热门',
        'platform':'pc'
    }
    try:
        html=requests.get(url,headers=headers,params=params)
        return html.json()
    except:
        print("请求错误")
        pass
#下载视频
def downloader(url,path):
    start=time.time() #开始时间
    size=0
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    response=requests.get(url,headers=headers,stream=True)
    chunk_size=1024  #每次下载数据的大小
    content_size=int(response.headers['content-length'])#总体大小
    if response.status_code==200:
        print('[文件大小]:%0.2fMB' %(content_size/chunk_size/1024))#换算单位
        with open(path,'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                size+=len(data)

if __name__=='__main__':
    for i in range(10):
        url='https://api.vc.bilibili.com/board/v1/ranking/top?'
        num=i*10+1
        html=get_json(url)
        infos=html['data']['items']
        for info in infos:
            title=info['item']['description'] #小视频标题
            video_url=info['item']['video_playurl'] #视频地址
            print(title,video_url)
            try:
                downloader(video_url,path="%s.mp4"%title)
                print("成功下载一个")
            except Exception as e:
                print("下载失败",format(e))
                pass
            time.sleep(int(format(random.randint(5,10))))

