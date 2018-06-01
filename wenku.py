
import requests
import re
import time
import json
import collections
import os
from math import floor
from multiprocessing import Pool



def get_response(url,headers):
    try:
        response = requests.get(url, headers=headers)
        return (response)
    except Exception as error:
        print(error)
        pass


def doc_type(url):
    headers = {
        'Host': 'wenku.baidu.com',
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'}
    text = get_response(url,headers).content.decode('gbk')
    doc_id = re.search('view/(.*?)\.html',url).group(1)
    doc_type = re.search(r'docType\': \'(.*?)\'', text).group(1)
    dict = {}
    dict['doc_id'] = doc_id
    dict['text'] = text
    dict['doc_type'] = doc_type
    print('判断文档类型...')
    return(dict)

def dict_cookies():
    cookie = '_ga=GA1.2.1519955624.1523859360; _gid=GA1.2.1709601367.1527612873; PHPSESSID=web1~5m8vtcjcn5b3g9mhjr26973ob8; Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1527613329,1527625554,1527663554,1527663712; Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1527663712'
    cookie = cookie.split(';')
    cookies = {}
    for i in cookie:
        k = i.split('=')
        cookies[k[0]] = k[1]


class type_txt(object):
    def __init__(self,url,id):
        self.url = url
        self.txt_id = id
        self.txt_title = None
        self.headers = {
            'Host':'wenku.baidu.com',
            'Connection':'close',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9'}

    def get_txt_information(self):
        #self.txt_id=re.findall(r'view/(.*?).html',self.url)[0]  #各类型都是这个id
        u1 = 'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id='
        url_json_p = u1+self.txt_id
        headers = self.headers
        headers['X-Requested-With'] = 'XMLHttpRequest'
        #获取txt信息
        json_p = get_response(url_json_p,headers).text
        json_p = json_p[7:-1]
        json_info = json.loads(json_p)
        params = collections.OrderedDict()
        self.txt_title = json_info['docInfo']['docTitle']
        #{'downloadToken': '32fba83b4ccdecbcb9dad26e496f7596', 'na_render_type': 'retype', 'isOrgCustomized': False, 'vip_info': {'edu_vip_type': 0, 'vip_type': 0, 'flag': 0, 'jiaoyu_vip_type': 0}, 'is_login': 0, 'freepagenum': None, 'bcsParam': False, 'mydoc': 0, 'doc_id_update': 'd723724e2b160b4e767fcf85', 'docInfo': {'docPrice': '1', 'isPaymentDoc': 0, 'totalPageNum': '5', 'docType': '8', 'docTitle': 'win7office2010升级密钥', 'cai': 0, 'zan': 0, 'docSize': '11627', 'mydoc': 0, 'docTicket': 1, 'valueCount': '9', 'docDesc': '各种密钥', 'cid4': None, 'downloadCount': '78', 'flag': '0', 'avadar': 'https://gss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portraitn/item/afd031353639313331393231e51b', 'ishide': '0', 'show_create_time': '2011-10-25 23:45:34', 'cid1': '3', 'valueScore': '26', 'createUser': '1569131921', 'cid3': '0', 'cid2': '63', 'main_status': '2', 'qualityScore': '5.0', 'keyWord': '各种密钥', 'show_update_time': '2011-10-25 23:45:34', 'createTime': '1319557534', 'viewCount': '3820'}, 'rtcs_flow': 100, 'rsign': 'p_5-r_0-s_0adb1', 'hasImage': 0, 'rtcs_flow_wap': 0, 'isPaymentDoc': 0, 'ori_render_type': 'retype', 'wap_render_type': 'retype', 'ispaper': 0, 'business_info': {'business_doc': 0}, 'bucketNum': 13, 'htmlBcs': False, 'doc_id': 'd723724e2b160b4e767fcf85', 'md5sum': '&md5sum=154fe74a9c2153c94d1b5cb43ee47d3a&sign=e4962b3685', 'rtcs_flow_rem': 74, 'isHtml': True, 'official_info': {'uid': '468045999', 'block_ad': 1, 'org_name': '1569131921', 'official_id': None, 'official_name': None, 'create_time': '2018-05-31', 'title': 'win7office2010升级密钥', 'pic_url': None}, 'crumbs': [{'cname': '专业资料', 'cid': 'pro'}, {'cname': 'IT/计算机', 'cid': '63'}]}
        md5 = json_info['md5sum'].split('&sign=')
        params['md5sum'] = md5[0][8:]
        params['sign'] = md5[1]
        params['callback'] = 'cb'
        params['pn'] = '1'
        params['rn'] = json_info['docInfo']['totalPageNum']
        params['type'] = 'txt'
        params['rsign'] = json_info['rsign']
        return(params)

    def get_txt_content(self):
        params = self.get_txt_information()
        user_agent={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        u1 = 'https://wkretype.bdimg.com/retype/text/'
        url = u1+self.txt_id
        json_content = requests.get(url, headers=user_agent, params=params).content.decode('utf-8')
        json_content = json_content[3:-1]
        txt_content = json.loads(json_content)
        #输出txt
        filename = 'C:\\Output\\'+self.txt_title+'.txt'
        print('文件保存在' + filename)
        if os.path.isdir('C:\\Output'):
            pass
        else:
            os.mkdir('C:\\Output')
        file=open(filename,'a')
        for i in range(len(txt_content)):
            print(txt_content[i]['parags'][0]['c'])
            file.write(txt_content[i]['parags'][0]['c'])
        file.close()

class type_doc(object):
    def __init__(self,content,url):
        self.content = content
        self.url = url
        self.doc_num = None
        self.doc_title = None
        self.page = '&pn='
        self.headers = {
            'Host': 'wenku.baidu.com',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'}


    def other_page_josn(self,url):                                  #处理大于50页的文档
        res = get_response(url,headers=self.headers).text
        jsonlist_pre = re.findall(r'docconvert(.*?)\\x22', res)
        jsonlist = jsonlist_pre[0:int(len(jsonlist_pre) / 2)]
        return(jsonlist)

    def get_doc_json_list(self):
        self.doc_title = re.search(r'<title>(.*?)_',self.content).group(1)
        jsonlist_pre = re.findall(r'docconvert(.*?)\\x22',self.content)
        self.doc_num = re.search('totalPageNum\D+(.*?)\D+//',self.content).group(1)
        print(self.doc_num)
        jsonlist = jsonlist_pre[0:int(len(jsonlist_pre) / 2)]
        count = len(jsonlist)
        self.doc_num = int(floor(int(self.doc_num) / 50))    #判断word文档的页数是否大于50，如大于需要再获取新网页源码
        if self.doc_num == 0:
            pass
        else:
            for i in range(1,self.doc_num+1):
                pagenum = self.url + self.page + str(i*50+1)
                jsonlist += self.other_page_josn(pagenum)
        for i in range(count):  #提取整理doc文档内容与图片的json地址
            jsonlist[i] = re.sub(r'\\', '', jsonlist[i])
            jsonlist[i] = 'https://wkbos.bdimg.com/v1/docconvert'+jsonlist[i]
        return(jsonlist)

    def get_doc_content(self):
        jsonlist = self.get_doc_json_list()
        sum_1 = 0
        for k in range(len(jsonlist)):   #判断是文字还是图片
            determine_wp = re.search(r'/0\.(.*?)\?',jsonlist[k]).group(1)
            try:
                if determine_wp == 'json':
                    sum_1 += 1
                    headers_json = {
                        'Host': 'wkbos.bdimg.com',
                        'Connection': 'close',
                        'Referer': 'https://wenku.baidu.com/view/dab732096d85ec3a87c24028915f804d2b1687da.html?from=search',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9'}
                    wenku_c = get_response(jsonlist[k], headers=headers_json).text
                    ws = len(str(sum_1+1))
                    wenku_c = wenku_c[7+ws:-1]
                    test = json.loads(wenku_c)
                    list_1 = test['body']
                    print(list_1)
                    filename = 'C:\\Output\\' + self.doc_title + '.txt'   #建立保存目录和文件名
                    if os.path.isdir('C:\\Output'):
                        pass
                    else:
                        os.mkdir('C:\\Output')
                    file = open(filename, 'a')
                    print('文件保存在'+filename)
                    a=''
                    print('正在打印第' + str(k + 1) + '页Word文档')
                    if list_1[0]['p']['y'] == list_1[1]['p']['y'] and type(list_1[0]['c']) == str :
                        a += list_1[0]['c']
                    elif type(list_1[0]['c']) == str:
                        file.write(list_1[0]['c'])
                    else:
                        pass
                    for i in range(len(list_1) - 1):
                        if type(list_1[i + 1]['c']) == dict:
                            pass
                        else:
                            if list_1[i]['p']['y'] == list_1[i + 1]['p']['y']:
                                a += list_1[i + 1]['c']
                            else:
                                file.write(a)
                                a = ''
                                file.write('\n')
                                a += list_1[i + 1]['c']
                    file.write(a)
                    file.close()
                else:
                    pass
            except ValueError:
                print('error json url'+jsonlist[k])

class type_ppt(object):
    def __init__(self,url,id):
        self.url = url
        self.ppt_id = id
        self.ppt_title = None
        self.headers = {
            'Host': 'wenku.baidu.com',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest' }

    def get_url_list(self):
        p1 = 'https://wenku.baidu.com/browse/getbcsurl?doc_id='
        p2 = '&pn=1&rn=99999&type=ppt'
        url = p1 + self.ppt_id + p2
        res = requests.get(url, headers=self.headers).text
        js = json.loads(res)
        return (js)

    def download_jpg(self,js):
        res = requests.get(js['zoom'])
        if res.status_code == 200:
            file = open('C://pic//' + str(js['page']) + '.jpg', 'wb')
            file.write(res.content)
            file.close()

    def write_to_pptx(self):
        js = self.get_url_list()
        pool = Pool(4)
        pool.map(self.download_jpg, js)
        pool.close()
        print('download finish')



def main():
    url = 'https://wenku.baidu.com/view/21c6094284868762cbaed58c.html?from=search'
    tmp = doc_type(url)
    type = tmp['doc_type']
    text = tmp['text']
    doc_id = tmp['doc_id']
    print('准备下载'+type+'文档')
    if type == 'txt':
        type_txt(url,doc_id).get_txt_content()
    elif type == 'doc':
        #type_doc(text,url).get_doc_json_list()
        type_doc(text, url).get_doc_content()
    elif type == 'ppt':
        type_ppt(url,doc_id).write_to_pptx()
    else:
        pass


if __name__ == '__main__':
    start = time.clock()
    main()
    elapsed = (time.clock()-start)
    print("程序运行时间为",elapsed,'秒')

