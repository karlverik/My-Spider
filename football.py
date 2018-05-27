#coding=utf-8
import requests
import random
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import xlwt

agent_list = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36']

def nation():
    headers = {'User-Agent':random.choice(agent_list)}
    url = 'http://zq.win007.com/cn/paiming.html'
    r = requests.get(url,headers=headers).text
    soup = BeautifulSoup(r,'lxml')
    team_name1 = soup.select('a[href^="/cn/team/Summary"]')
    num = 0
    tree = lambda: defaultdict(tree)
    data = tree()
    for team_name in team_name1:
        url_id = team_name['href']
        team_name = team_name.text.rstrip()
        num=num+1
        data[num]['rank'] = num
        data[num]['url_id'] = url_id
        data[num]['nation'] = team_name
    data = json.dumps(data,ensure_ascii=False)
    data = json.loads(data)
    return(data)

def number(id):
    r1 = 'http://zq.win007.com/cn/team/CTeamSche/'
    r2 = '.html'
    refer = r1 + id + r2  # refer headers
    header = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Host': 'zq.win007.com',
        'Refer': refer,
        'User-Agent': random.choice(agent_list),
        'X-Requested-With': 'XMLHttpRequest'
    }
    u1 = 'http://zq.win007.com/cn/team/TeamScheAjax.aspx?TeamID='

    url = u1 + id
    res = requests.get(url, headers=header).text
    res = res.split(';', 1)[0]
    num_p = re.split(r' = ', res)
    num = eval(num_p[1])[0]  # 页码数
    return num

def find_data(id,num):
    r1 = 'http://zq.win007.com/cn/team/CTeamSche/'
    r2 = '.html'
    refer = r1 + id + r2  # refer headers
    header = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Host': 'zq.win007.com',
        'Refer': refer,
        'User-Agent': random.choice(agent_list),
        'X-Requested-With': 'XMLHttpRequest'
    }
    u1 = 'http://zq.win007.com/cn/team/TeamScheAjax.aspx?TeamID='
    u2 = '&pageNo='
    url = u1 + id+u2+str(num)
    res = requests.get(url, headers=header).text
    res = res.split(';', 1)
    country = res[1]
    country = re.split(r' = ', country)
    c_x = country[1][:-2]
    output = eval(c_x)
    for i in range(len(output)):
        del output[i][15]
        del output[i][12]
        del output[i][9]
        del output[i][2]
    return(output)


def factual_data():
    data=nation()
    wbk = xlwt.Workbook()
    for i in data:
        url_x=data[i]['url_id']
        name=data[i]['nation']
        print(name)
        id=re.findall('\d+',url_x)[0] #数字Id
        num=number(id)
        item = ['赛程编号', '赛事编号', '日期', '主队编号', '客队编号', '全场比分', '半场比分', '赛事', '赛事英', '主队', '主队英', '客队', '客队英', '主红', '客红',
                '', '让球盘路', '让球盘口', '大小球盘路', '赛果盘路']
        nation_data=[]
        for k in range(num):
            k+=1
            f=[]
            f=find_data(id,k)
            nation_data=nation_data+f
        #excel 操作
        sheet = wbk.add_sheet(name)
        for title in range(len(item)):
            sheet.write(0, title, item[title])

        for row in range(len(nation_data)):
            for col in range(0, len(nation_data[row])):
                sheet.write(row + 1, col, nation_data[row][col])
        wbk.save(r'C:\football.xls')

if __name__ == "__main__":
    factual_data()
