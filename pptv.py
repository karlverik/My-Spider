#coding=utf-8
import re
import sys
import os
import time
import requests
from tqdm import tqdm
from subprocess import Popen
from selenium import webdriver
from browsermobproxy import Server
from multiprocessing import Pool


class PPTV(object):
    def __init__(self,url):
        self.url = url
        self.server = None
        self.proxy = None
        self.driver = None
        self.vvid = None
        self.initial_url = None
        self.num = None
        self.title = None

    def browsermobproxy_set(self):
        self.server = Server("C:\\chromedriver\\browsermob-proxy-2.0-beta-6\\bin\\browsermob-proxy.bat")
        self.server.start()
        self.proxy = self.server.create_proxy()

    def webdriver_set(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={host}:{port}'.format(host="localhost", port=self.proxy.port)) #添加代理参数
        prefs = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1
        }
        options.add_experimental_option('prefs', prefs)    #允许flsh运行
        profile_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome Beta\User Data"
        options.add_argument("user-data-dir=" + os.path.abspath(profile_dir))    #添加cookies
        self.driver = webdriver.Chrome(chrome_options=options)

    def get_initial_url(self):
        self.proxy.new_har('pptv')
        self.driver.get(self.url)
        time.sleep(8)
        #self.title = self.driver.find_element_by_xpath('/html/head/title').text #获取标题名
        if self.proxy.har['log']['entries']:
            for i in self.proxy.har['log']['entries']:
                try:
                    if (re.search('fpp.ver=1.3.0.23&key', i['request']['url'])):
                        self.initial_url = i['request']['url']
                        #print(self.initial_url)
                        print('已找到视频源地址')
                        break
                except Exception as err:
                    print(err)
                    print('没有找到视频地址，请检测网络和输入URL是否正确')
                    sys.exit()
        self.server.stop()
        self.driver.close()
        self.driver.quit()

    def get_download_url(self):
        url_tmp = re.search('http://(.*?)/.*/(.*)',self.initial_url)
        #print(url_tmp)
        url_ip = url_tmp.group(1)
        url_param = url_tmp.group(2)
        self.vvid = re.search('(.*)\?fpp', url_param).group(1)
        headers = {
            'Referer': self.url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36',
            'X-Requested-With': 'ShockwaveFlash/29.0.0.171'
        }
        url_num = 'http://drag.synacast.com/' + self.vvid + '0drag'
        res = requests.get(url_num,headers=headers).text
        num = re.findall('<segment no="(\d+)"', res)
        filesize = re.findall('filesize="(\d+)"',res)
        #print(num)
        self.num = len(num)
        download_url = []
        #tree = lambda: defaultdict(tree)
        #self.download_url = tree()
        for i in range(len(num)):
            url = "http://%s/%s/%s"%(url_ip,num[i],url_param)
            dict_tmp = {}
            dict_tmp['url'] = url
            dict_tmp['name'] = num[i]
            dict_tmp['filesize'] = int(filesize[i])
            download_url.append(dict_tmp)
            del dict_tmp
        #print(download_url)
        return(download_url)

    def title_name(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36'}
        res = requests.get(self.url, headers=headers).text
        self.title = re.search('<title>(.*?)</title>',res).group(1)

    def main(self):
        self.browsermobproxy_set()
        self.webdriver_set()
        self.get_initial_url()
        self.title_name()
        download_url = self.get_download_url()
        return(download_url)

#-----------------------------分视频处理部分----------------------------#


def input_url():
    print('请输入下载视频地址\n')
    url = input()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36'}
    res = requests.head(url,headers=headers)
    if res.status_code == 200:
        return(url)
    else:
        print('地址错误，请输入正确的url地址')

def download_video(file_info):
    filename = 'C:\\video\\temp\\' + file_info['name'] + '.mp4'
    if os.path.exists(filename):
        first_byte = os.path.getsize(filename)
    else:
        first_byte = 0
    if first_byte >= file_info['filesize']:
        return file_info['filesize']
    pbar = tqdm(
        total=file_info['filesize'], initial=first_byte,
        unit='B', unit_scale=True, desc=filename)
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36'}
    req = requests.get(file_info['url'], headers=user_agent, stream=True)

    with(open(filename, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            f.write(chunk)
            pbar.update(1024)
    pbar.update()
    pbar.close()
    return(file_info['filesize'])

def ffmpeg(filename):
    file_list = os.listdir('C:\\video\\temp')
    n = len(file_list)
    f = open('C:\\video\\process.bat', 'w', encoding='utf-8')
    ts_all = ''
    for i in range(n):
        f.write('ffmpeg -i "%s.mp4" -codec copy -vbsf h264_mp4toannexb "%s.ts" \n' % (str(i), str(i)))
        ts_p = str(i) + '.ts|'
        ts_all += ts_p
    ts_all = ts_all[:-1]
    f.write('ffmpeg -i "concat:%s" -codec copy -absf aac_adtstoasc "%s.mp4"\n' % (ts_all, filename))
    f.write('del *.ts\n')
    f.close()
    p = Popen("process.bat", cwd=r"C:\video")
    stdout, stderr = p.communicate()
    os.remove('C:\\video\\process.bat')



if __name__ == '__main__':
    try:
        print('pptv视频下载程序开始运行')
        #url = input_url()
        url = 'http://v.pptv.com/show/KfP7eOBGtvRX1T0.html?rcc_src=L1'
        pptv = PPTV(url)
        print('寻找视频源地址中...')
        start = time.clock()
        download_url = pptv.main()
        pool = Pool(4)
        pool.map(download_video, download_url)
        pool.close()
        end = (time.clock() - start)
        print('下载共耗时', end, '秒')
        time.sleep(1)
        print('开始合并mp4文件')
        filename = pptv.title
        ffmpeg(filename)
        print('文件合并完成，存放在C:\\video\\',filename,'.mp4')
    except Exception as err:
        print(err)
        pass











