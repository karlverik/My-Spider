#coding=utf-8
import requests
import random
import re
from lxml import etree
from multiprocessing import Pool

agent_list = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36']

def get_nation_list():
    url = 'http://zq.win007.com/cn/paiming.html'
    data = {
        'sex': '0',
        'season': '2018',
        'month': '5'
    }
    headers = {"User-Agent":random.choice(agent_list)}
    res = requests.post(url, headers=headers, data=data).text
    tree = etree.HTML(res)
    rank = tree.xpath('//*[@id="div_Table1"]/tr[position()>1]/td[1]/text()')
    id = tree.xpath('//*[@id="div_Table1"]/tr/td[2]/a/@href')
    name = tree.xpath('//*[@id="div_Table1"]/tr/td[2]/a/text()')
    nation_list = []
    for i in range(len(rank)):
        nation_tmp = []
        nation_tmp.append(rank[i])
        nation_tmp.append(name[i].rstrip())
        nation_tmp.append(id[i][:-5].replace('Summary/','TeamScheAjax.aspx?TeamID='))
        print(id[i][:-5].replace('Summary/','TeamScheAjax.aspx?TeamID='))
        nation_list.append(nation_tmp)
    return(nation_list)

def get_nation_data(nation_list):
    nation_rank = nation_list[0]
    nation_name = nation_list[1]
    nation_id = nation_list[2]
    url = "http://zq.win007.com"+nation_id
    headers = {
        "User-Agent":random.choice(agent_list)
    }
    print(url)
    res = requests.get(url,headers=headers).text
    res = res[2:].split(';', 1)[0]
    num_p = re.split(r' = ', res)
    print(num_p)


def main():
    r = get_nation_list()








if __name__ == '__main__':
    r = get_nation_list()
    for i in r:
        get_nation_data(i)









