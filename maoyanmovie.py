#-*-coding: utf-8 -*-
#author:cici
import re
import requests
import json
import pymysql
from multiprocessing import Pool
from requests.exceptions import RequestException
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Host':'maoyan.com'
}
class Sql(object):
    connection=pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='lzy6352341',
        db='maoyan',
        charset = 'utf8'
    )
    def addnews(self,movienum,moviename,moviegrade,movietime,moviemessage,moviecountry):
        cur=self.connection.cursor()
        cur.execute(
            "insert into maoyanmovie(movienum,moviename,moviegrade,movietime,moviemessage,moviecountry) values('%s','%s','%s','%s','%s','%s') " % (
            movienum, moviename, moviegrade, movietime, moviemessage,moviecountry))
        lastrowid=cur.lastrowid
        cur.close()
        self.connection.commit()
        return lastrowid
mysql=Sql()

def get_one_page(url):
    try:
        response = requests.get(url,headers=headers,timeout=1)
        if response.status_code==200:
            return response.text
        else:
            return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?"name"><a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1].split('@')[0],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:15],
            'score':item[5]+item[6],
            'country':item[4].strip()[16:-1]
        }

#def write_to_file(content):
#    with open('result.txt','a',encoding='utf-8')as f:
#        f.write(json.dumps(content,ensure_ascii=False)+'\n')
#        f.close()

def main(offset):
    url='https://maoyan.com/board/4?offset='+ str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        mysql.addnews(item['index'],item['title'],item['score'],item['time'],item['actor'],item['country'])
        print(item)
#        write_to_file(item)


if __name__=='__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])