# -*- coding：utf-8 -*-
import os
import re
import gzip
import requests
import json
import ssl
import bs4
from importlib import import_module
from threading import Thread
from urllib import request, error
from bs4 import BeautifulSoup


# 解决https不受信任
ssl._create_default_https_context = ssl._create_unverified_context

SITES = {
    'www.qidian.com': 'qidian',
    'www.23us.la': '23us',
    'www.23us.cc': '23us_cc',
    'www.xs.la': 'xs',
    'www.paomov.com': 'paomov',
    'www.tianxiabachang.cn': 'tianxiabachang',
    'www.luoqiuzw.com': 'luoqiuzw',
    'www.23wx.cm': '23wx',
    'www.biqugezw.com': 'biqugezw',
    'www.x88dushu.com': '88dus',
    'www.ymoxuan.com': 'ymoxuan',
    'm.80txt.com': 'm80txt'

}

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0'
}


global cookies_dict


def set_cookies(value):
    # 告诉编译器我在这个方法中使用的cookies_dict是刚才定义的全局变量cookies_dict,而不是方法内部的局部变量.
    global cookies_dict
    cookies_dict = value


def get_cookies():
    # 同样告诉编译器我在这个方法中使用的cookies_dict是刚才定义的全局变量cookies_dict,并返回全局变量cookies_dict,而不是方法内部的局部变量.
    global cookies_dict
    return cookies_dict


def save_cookise(path, cookies):
    save_file(path, json.dumps(cookies))


def open_cookise(path):
    return json.loads(open_file(path))


def open_html(url, code_mode='utf-8', count=0):
    try:
        req = request.Request(url)
        req.add_header('Accept-encoding', 'gzip,deflate,sdch')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3033.0 Safari/537.36')
        # 返回页面内容
        doc = request.urlopen(req).read()  # python3.x read the html as html code bytearray
        # 解码
        try:
            html = gzip.decompress(doc).decode(req.encoding, 'ignore')
            # print('返回gzip格式的文件')
        except Exception as e_gzip:
            html = doc.decode(code_mode, 'ignore')
            # print('返回正常格式的文件:' + str(e_gzip))
    except Exception as e:
        print('open_html页面打开失败：[%s] error：%s' % (url, e))
        if count > 5:
            return '404'
        return open_html(url, count+1)
    return html


def open_html_nogzip(url, code_mode='utf-8', count=0):
    try:
        webheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = request.Request(url=url, headers=webheader)
        webPage = request.urlopen(req)
        data = webPage.read()
        data = data.decode(code_mode)
        return data
    except Exception as e:
        print("open_html_nogzip error:" + str(e))
        if count < 5:
            open_html_nogzip(url, code_mode, count+1)


def get_html(url, count=0):
    try:
        if get_cookies():
            r = requests.get(url, headers=fake_headers, cookies=get_cookies(), timeout=10)
        else:
            r = requests.get(url, headers=fake_headers, timeout=10)
        encodings = requests.utils.get_encodings_from_content(r.text)
        if encodings:
            r.encoding = encodings[0]
    except Exception as e:
        print('get_html页面打开失败：[%s] error：%s' % (url, e))
        if count > 5:
            return '404'
        return get_html(url, count+1)
    return r.text


def post_html(url, count=0):
    try:
        r = requests.post(url, headers=fake_headers, timeout=10)
        encodings = requests.utils.get_encodings_from_content(r.text)
        if encodings:
            r.encoding = encodings[0]
    except Exception as e:
        print('post_html页面打开失败：[%s] error：%s' % (url, e))
        if count > 5:
            return '404'
        return post_html(url, count+1)
    return r.text


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
        book_host = r1(r'https?://([^/]+)/', url)
        assert book_host
    except:
        book_host = r1(r'https?://([^/]+)/', url)
    # print("检测："+book_host)
    if book_host in SITES:
        # print(book_host+"在模块中")
        return import_module('.'.join(['extractors', SITES[book_host]])), url
    else:
        # print("失败：" + book_host)
        return None, "None"


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
    path = path.replace('/', '\\')
    if path[:-1] == '\\':
        path = path[0:-1]
    return path


def path_linux(path):
    path = path.replace('\\', '/')
    if path[:-1] == '/':
        path = path[0:-1]
    return path


def path_format(path):
    if os.name == 'nt':
        path = path_win(path)
    elif os.name == 'Android' or 'posix':
        path = path_linux(path)
    return path


def save_file(path, data):
    try:
        path = path_format(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(data))
            f.close()
            return True
    except Exception as e:
        print('save_file error:file(%s):%s' % (path, e))
        return False
        pass


def open_file(path):
    try:
        path = path_format(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            return data
    except Exception as e:
        print('open_file error:file(%s):%s' % (path, e))
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
        print('open_gzip error file:(%s);%s' % (path, e))
        return ''


# 制作字符替换字典
def make_dict(s_in,s_out):
    d = dict()
    if len(s_in) <= len(s_out):
        l = len(s_in)
        for i in range(l):
            d.update(str.maketrans(s_in[i], s_out[i]))
    else:
        l = len(s_out)
        for i in range(l):
            if i < l:
                d.update(str.maketrans(s_in[i], s_out[i]))
            else:
                d.update(str.maketrans(s_in[i], ''))
    return d


# 替换标题不用做路径和文件名
def replace_title(text):
    t = make_dict('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０・，．！?!\n', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890·，。！？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text


# 替换UTF-8的空格
def replace_block(text):
    # u"\xa0\n\t"
    #move = dict.fromkeys((ord(c) for c in u"\xa0"))
    t = make_dict(u'\xa0', ' ')
    text = text.translate(t)
    return text


# 替换字符串
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


# 合并文本
def join_text(name, file_list):
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


# 合并文本存为gz
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


def start_download(mode, info, path='', retry=0):
    thisPath = path
    retry_count = retry
    if retry_count >= 5:
        return
    if thisPath == '':
        thisPath = getPath()
    book_name = info['name']
    dir_path = path_format(thisPath+'/'+book_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    save_gzip(path_format(dir_path+'/'+'info.txt.gz'), str(info))
    download_list = list()
    for i in info['catalog']:
        print(i)
        f_name = i['id'] + '.txt.gz'
        full_path = path_format(dir_path + '/' + f_name)
        download_list.append(full_path)
        if not os.path.exists(full_path) or len(open_gzip(full_path)) < 20:
            try:
                # fp = request.urlopen(i['url'], timeout=10)
                # html = fp.read()
                # html = post_html(i['url'])
                html = mode.get_html(i['url'])
                text, text_code = mode.get_text(html)
                if len(text) == 0 and len(text_code) > 0:
                    save_gzip(path_format(dir_path + '/error_' + f_name), text_code)
                else:
                    text = i['chapter'] + '\n' + text
                    save_gzip(full_path, text)
            except error.URLError as e:
                print('download error,Time out! :'+str(e))
                start_download(mode, info, path, retry_count+1)
            except Exception as ee:
                print('download other error:' + str(ee))

            print('download+++++++++'+i['chapter'])
        else:
            print('download========'+i['chapter'])
    print('join file')
    join_text_gz(path_format(dir_path+'/'+book_name+'.txt.gz'), download_list)


def test_url(url):
    out_str = 'start url_to_module(%s)---------:' % url
    try:
        mode, t_url = url_to_module(url)
        if mode:
            out_str += "成功"
        else:
            out_str += "失败"
    except Exception as e:
        print('error:' + url + 'Message:' + str(e))
    finally:
        print(out_str)


def _thread_download(chapter_info, full_path, mode, lock, retry=0):
    retry_count = retry
    if retry_count >= 5:
        lock.release()
        return
    if not os.path.exists(full_path) or len(open_gzip(full_path)) < 20:
        try:
            html = mode.get_html(chapter_info['url'])
            text, text_code = mode.get_text(html)
            if len(text) == 0 and len(text_code) > 0:
                dir_path = os.path.dirname(full_path)
                f_name = os.path.basename(full_path)
                save_gzip(path_format(dir_path + '/error_' + f_name), text_code)
            else:
                text = chapter_info['chapter'] + '\n\n' + text
                save_gzip(full_path, text)
        except error.URLError as e:
            print('download error,Time out! :' + str(e))
            _thread_download(chapter_info, full_path, mode, lock, retry_count + 1)
        except Exception as ee:
            print('download other error:' + str(ee))

        print('download+++++++++' + chapter_info['chapter'])
    else:
        print('download========' + chapter_info['chapter'])
    lock.release()


def check_download_thread(thread_list):
    for l in thread_list:
        if not l.locked():
            thread_list.remove(l)
    if len(thread_list) is 0:
        return False
    else:
        return True


def test_download(mode, info=None, book_name='', path='', retry=0):
    retry_count = retry
    if retry_count >= 5:
        return

    if info is None:
        if len(book_name) > 1:
            _book_name = book_name
        else:
            return
    else:
        _book_name = info['name']

    thisPath = path

    if thisPath == '':
        thisPath = getPath()

    dir_path = path_format(thisPath + '/' + _book_name)
    is_new_download = True
    info_json_file_path = dir_path + '/' + 'info.json.gz'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        try:
            if os.path.exists(info_json_file_path) and info is None:
                info_file = open_gzip(info_json_file_path)
                info = json.loads(info_file)
                print(info)
                is_new_download = False
        except Exception as e:
            print(e)
    if info is None:
        return
    if is_new_download:
        save_gzip(path_format(dir_path + '/' + 'info.txt.gz'), str(info))
        save_gzip(path_format(dir_path + '/' + 'info.json.gz'), json.dumps(info))
    download_list = list()
    locks = []
    thread_count = 10
    download_point = 0

    import _thread
    chapter_infos = info['catalog']
    while len(chapter_infos) > download_point:
        if len(locks) < thread_count:
            lock = _thread.allocate_lock()
            lock.acquire()
            locks.append(lock)
            chapter_info = chapter_infos[download_point]
            f_name = chapter_info['id'] + '.txt.gz'
            full_path = path_format(dir_path + '/' + f_name)
            download_list.append(full_path)
            _thread.start_new_thread(_thread_download, (chapter_info, full_path, mode, lock))
            download_point = download_point + 1
        check_download_thread(locks)
    while check_download_thread(locks):
        check_download_thread(locks)
    print('join file')
    join_text_gz(path_format(dir_path+'/'+_book_name+'.txt.gz'), download_list)

# test_url('http://www.biqugezw.com/15_15701/')
# test_url('http://www.paomov.com/txt99026.shtml')
# test_url('http://www.biqugezw.com/15_15701/')
# test_url('http://www.23wx.cm/24/24151/index.html')
# test_url('https://www.xs.la/184_184338/')
# test_url('http://www.tianxiabachang.cn/1_1107/')


# from common import url_to_module
# m = import_module('.'.join(['extractors', SITES['m.80txt.com']]))
# test_download(m, '')
