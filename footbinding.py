#coding=utf-8
import requests
from bs4 import BeautifulSoup


def article_url():
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    count=[]
    for i in range(1,6):
        url = 'http://www.footbinding.com.tw/bbs/dv_rss.asp?s=xhtml&boardid=21&page={num}&count=93'
        url = url.format(num=i)
        res = requests.get(url,headers=header).text
        soup = BeautifulSoup(res,'lxml')
        url_a = soup.select('a[href^="http://www.footbinding.com.tw/bbs/dv_rss.asp?s=xhtml&boardid=21&id"]')
        for k in url_a:
            count.append(int(k['href'][67:-7]))
    count.sort()
    return(count)


def article(count):
    for i in range(len(count)):
        url = 'http://www.footbinding.com.tw/bbs/dv_rss.asp?s=xhtml&boardid=21&id={count}&page=1'
        url = url.format(count=count[i])
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        r = requests.get(url, headers=header).text
        soup = BeautifulSoup(r, 'lxml')
        test = soup.select('.postbody ')[0].select('p')
        txt = open('C:\\footbinding.txt', 'a',encoding='utf-8')
        print(i)
        for k in test:
            txt.write(k.get_text())
            txt.write('\n')
        txt.close()

if __name__=="__main__":
    count = article_url()
    article(count)





