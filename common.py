#-*- coding：utf-8 -*-
import os
import re
import gzip
import json
from importlib import import_module
from threading import Thread
from urllib import request
from bs4 import BeautifulSoup
#解决https不受信任
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SITES = {
    'qidian'            : 'qidian',
    '23us'              :'23us',
    'xs'                :'xs',
    'paomov'            :'paomov',

}

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0'
}

# DEPRECATED in favor of match1()
def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

# DEPRECATED in favor of match1()
def r1_of(patterns, text):
    for p in patterns:
        x = r1(p, text)
        if x:
            return x

def url_to_module(url):
    try:
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except:
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)

    # if video_host.endswith('.com.cn'):
    #     video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domain, 'unsupported url: ' + url
    #return video_host,video_url

    k = r1(r'([^.]+)', domain)
    print("检测："+k)
    if k in SITES:
        print(k+"在模块中")
        return import_module('.'.join(['extractors', SITES[k]])), url
    else:
        return None,"None"
    #     import http.client
    #     conn = http.client.HTTPConnection(video_host)
    #     conn.request("HEAD", video_url, headers=fake_headers)
    #     res = conn.getresponse()
    #     location = res.getheader('location')
    #     if location and location != url and not location.startswith('/'):
    #         return url_to_module(location)
    #     else:
    #         return import_module('you_get.extractors.universal'), url


class downloadbook(Thread):
    def __init__(self, book_name, book_info, downloadmode, dir_path):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_info = book_info
        self.book_downloadmod = downloadmode
        self.dir_path = dir_path


    def run(self):
        print('run')


def path_win(path):
    path =  path.replace('/', '\\')
    if path[:-1] == '\\':
        path = path[0:-1]
    return path

def path_linux(path):
    path =  path.replace('\\', '/')
    if path[:-1] == '/':
        path = path[0:-1]
    return path

def path_format(path):
    if os.name == 'nt':
        path = path_win(path)
    elif os.name == 'Android' or 'posix':
        path = path_linux(path)
    return path

def open_file(path):
    try:
        path = path_format(path)
        with open(path,'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            return data;
    except Exception as e:
        print('error:file(%s):%s'% (path,e))
        return ''
        pass

def save_gzip(path, data):
    try:
        path = path_format(path)
        content = str(data).encode('utf-8')
        with gzip.open(path, 'wb') as f:
            f.write(content)
            f.close()
            return True
    except Exception as e:
        print('save_gzip error:file(%s):%s' % (path, e))
        return False
        pass

def open_gzip(path):
    try:
        with gzip.open(path, 'rb') as f:
            data = f.read().decode('utf-8')
            f.close
            return data
    except Exception as e:
        print('open_gzip error file:(%s);%s' % (path,e))
        return ''

# 制作字符替换字典
def make_dict(s_in,s_out):
    d = dict()
    if len(s_in) <= len(s_out):
        l = len(s_in)
        for i in range(l):
            d.update(str.maketrans(s_in[i],s_out[i]))
    else:
        l = len(s_out)
        for i in range(l):
            if i < l:
                d.update(str.maketrans(s_in[i],s_out[i]))
            else:
                d.update(str.maketrans(s_in[i], ''))
    return d
#替换标题不用做路径和文件名
def replace_title(text):
    t = make_dict('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０，．！?!\n', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890，。！？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text

#替换字符串
def replace_file_path(path):
    path = path.replace('/', '-')
    path = path.replace('\\', '-')
    path = path.replace('*', '-')
    path = path.replace('?', '？')
    path = path.replace('!', '！')
    path = path.replace('\n', '')
    path = path.replace('', ' ')
    path = path.replace('|', '_')
    path = path.replace(':', '：')
    path = path.strip()
    path = path.lstrip()
    return path

def getPath():
    path = './'
    if os.name == 'nt':
        path = os.getcwd()
    elif os.name == 'Android' or 'posix':
        path = os.path.dirname(__file__)
        if path == './':
            path = '/storage/emulated/0/qpython/scripts3/projects3/qidian'
    return path


#合并文本
def join_text(name,file_list):
    try:
        with open(name, 'w', encoding='utf-8') as f:
            for i in file_list:
                    t = path_format(str(i))
                    if os.path.exists(t):
                        with open(t, 'r', encoding='utf-8') as a:
                            f.write(a.read())
                            f.write('\n')
                            f.write('\n')
                            a.close()
                    elif os.path.exists(t+'.gz'):
                        with gzip.open(t+'.gz', 'rb') as a:
                            data = a.read().decode('utf-8')
                            f.write(data)
                            f.write('\n')
                            f.write('\n')
                            a.close
            f.close()
    except Exception as e:
        print('join_text_error : %s : %s' % (f,e))
        pass
def join_text_gz(name, file_list):
    try:
        with gzip.open(name, 'w') as f:
            for i in file_list:
                t = path_format(str(i))
                if os.path.exists(t):
                    if t.endswith(r'.txt'):
                        with open(t, 'r', encoding='utf-8') as a:
                            txt = a.read()+'\n\n'
                            f.write(txt.encode('utf-8'))
                            a.close()
                    elif t.endswith(r'.txt.gz'):
                        with gzip.open(t, 'rb') as a:
                            txt = a.read().decode('utf-8') + '\n\n'
                            f.write(txt.encode('utf-8'))
                            a.close
        f.close()
    except Exception as e:
        print('join_text_error : %s : %s' % (f, e))
        pass


def start_download(mode,info,path =''):
    thisPath = path
    if thisPath == '':
        thisPath = getPath()
    book_name = info['name']
    dir_path = path_format(thisPath+'/'+book_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    save_gzip(path_format(dir_path+'/'+'info.txt.gz'),str(info))
    download_list = list()
    for i in info['catalog']:
        print(i)
        f_name = i['id'] + '.txt.gz'
        full_path = path_format(dir_path + '/' + f_name)
        download_list.append(full_path)
        if not os.path.exists(full_path) or len(open_gzip(full_path)) < 20:
            fp = request.urlopen(i['url'])
            html = fp.read()
            text = mode.get_text(html)
            text = i['chapter'] + '\n' + text
            save_gzip(full_path,text)
            print('download+++++++++'+i['chapter'])
        else:
            print('download========'+i['chapter'])
    print('join file')
    join_text_gz(path_format(dir_path+'/'+book_name+'.txt.gz'),download_list)


