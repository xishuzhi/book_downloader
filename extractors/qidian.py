# -*- coding：utf-8 -*-

from common import *

import urllib.request
import re

__all__ = ['get_qidian_info', "parss_qidian_text"]
host_url = r'https://www.qidian.com'
mode_name = 'qidian'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}



#获取书籍信息和目录的JSON
def getBookInfoData(bookID):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=%s' % bookID
    url_request = urllib.request.Request(url)
    url_request.add_header('Accept-encoding', 'gzip')
    url_request.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')
    url_response = urllib.request.urlopen(url_request)
    data = url_response.read()
    html = gzip.decompress(data).decode("utf-8")
    json_data = json.loads(html)
    return json_data
#获取章节详细信息 return [{'v_vip': 0, 'v_cid': 0000000, 'v_name': '章节名', 'v_url': 'https://vipreader.qidian.com/chapter/书ID_id/章节ID_cid'}, ]


def get_qidian_json(bookID):
    headers = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000'
    }
    try:
        url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=%s' % bookID
        # 返回页面内容
        r = requests.get(url, headers=headers, timeout=5)
        html = r.text
        # html = html.encode(r.encoding)
        print(html)
        json_file = r.json()
        print(json_file)
    except Exception as e:
        print('open_html页面打开失败：[%s]' % (url))
    return json_file


def get_g_data_chapter(page_tet):
    # 查找章节信息g_data.chapter
    t = page_tet
    # 查找信息主体
    req = re.compile('g_data.chapter = \{(.*?)\}', re.S)
    text = re.findall(req, t)
    text = text[0]
    # 去除注释部分
    reeq = re.compile('//.*\n')
    text = reeq.sub('', text)
    # 去除空格和换行
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    # 切分参数
    parms = text.split(',')
    # ['id:414121845', 'vipStatus:0', 'prevId:-1', 'nextId:414136648', 'isBuy:0']
    return parms

def open_qidian_html(url, code_mode='utf-8', count=0):
    headers = {
        'Connection': 'keep-alive',
        # 'Content-Length': '11',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'DNT': '1',
        'Accept-Encoding': 'gzip, default',
        'Accept-Language': 'zh-CN,zh;q=0.9,q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        # 返回页面内容
        r = requests.get(url, headers=headers, timeout=5)
        html = r.text
        html = html.encode(r.encoding)

    except Exception as e:
        print('open_html页面打开失败：[%s]' % (url))
    return html


def get_chapt_list(page_text):
    chapt_url_list = []
    try:
        req = ('<a href=.*?data-cid="(.*?)" title=".*?">(.*?)</a>')
        urls = re.findall(req, page_text)
        for l in urls:
            print('url: https:' + l[0] + '，章节:' + l[1])
            chapt_url_list.append({'url': l[0], 'chapter': l[1]})

    except Exception as e:
        print('get_%s_page_list error::%s' % (mode_name, str(e)))
    finally:
        return chapt_url_list

# 通过etree解析网页获取信息
def get_chapt_lxml(page_text):
    from lxml import etree
    etree_html = etree.HTML(page_text)
    # 选择书名
    book_names = etree_html.xpath('//div[@class="book-info "]/h1/em')

    # 选择作者
    book_acters = etree_html.xpath('//div[@class="book-info "]/h1/span/a')

    # 选择章节名
    names = etree_html.xpath('//ul[@class="cf"]/li/a')

    # 选择章节连接
    urls = etree_html.xpath('//ul[@class="cf"]/li/a/@href')



    print(book_names[0].text)

    book_name = book_names[0].text
    book_acter = book_acters[0].text
    all_bool_list = []

    for na, ur in zip(names, urls):
        all_bool_list.append({'name': na.text, 'url': 'https:'+ur})

    book_info['name'] = book_name
    book_info['auteur'] = book_acter
    book_info['catalog'] = all_bool_list

    return book_info

def get_book_list(page_text):
    book_url_list = []
    try:
        metaSoup = BeautifulSoup(page_text, "html.parser")
        page = metaSoup.findAll('dd')
        for tag in page:
            chapter = tag.a.text
            u = host_url + tag.a['href']
            id = -1
            p = u.rfind('/')
            if p > 0:
                id = u[p + 1:-5]
            book_url_list.append({'chapter': chapter, 'url': u, 'id': id})
        # print('章节名：' + tag.a.text + ',url=' + host_url + tag.a['href']+',id='+id)
    except Exception as e:
        print('get_%s_book_list error::%s' % (mode_name, str(e)))
    finally:
        return book_url_list




def get_qidian_info(url, only_book_name=False):
    html = open_qidian_html(url)
    return get_chapt_lxml(html)


def parss_qidian_text(html):
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        file_text = metaSoup.prettify()
        # 处理'&nbsp;
        file_text = file_text.replace('&nbsp;', ' ')
        metaSoup = BeautifulSoup(file_text, "html.parser")
        # 处理标签
        strong_tag = metaSoup.find_all(['head', 'strong', 'a', 'table'])
        for st in strong_tag:
            st.clear()
        # 处理文章内容
        file_text = metaSoup.prettify()
        file_text = file_text[file_text.find('<div id="nr1">'):file_text.find('content2();')]
        metaSoup = BeautifulSoup(file_text, "html.parser")
        # 转换为文本
        text = metaSoup.text
    except Exception as e:
        print('parss_%s_text error:%s' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_qidian_info
get_text = parss_qidian_text
get_html = open_qidian_html
mode_info = print_mode_info


def test(url=''):

    url = 'https://book.qidian.com/info/1012209059'
    # 打开在线页面
    # html = open_qidian_html(url)
    # save_file('qidian_test2.html', html.decode('UTF-8'))


    # # html = urllib.request.urlopen(url)
    # # save_file('qidian_test3.html', html.read().decode('utf8'))
    html = open_file('qidian_test3.html')
    req = ('<a href=.*?data-cid="(.*?)" title=".*?">(.*?)</a>')
    urls = re.findall(req, html)
    # print(urls)
    # for l in urls:
    #     print('url: https:'+l[0]+'，章节:'+l[1])

    # # 使用etree解析页面获取书名，章节名，章节连接
    # from lxml import etree
    # etree_html = etree.HTML(html)
    # # 选择章节名
    # names = etree_html.xpath('//ul[@class="cf"]/li/a')
    # # 选择章节连接
    # urls = etree_html.xpath('//ul[@class="cf"]/li/a/@href')
    #
    # # 选择书名
    # book_names = etree_html.xpath('//div[@class="book-info "]/h1/em')
    #
    # print(book_names[0].text)
    #
    # for i in names:
    #     # print(i.values())
    #     # print(i.text)
    #     pass
    # item = []
    # for na, ur in zip(names, urls):
    #     item.append({'name': na.text, 'url': 'https:'+ur})
    # print(item)

    print(get_chapt_lxml(html))



    # # json
    # json_file = getBookInfoData(1012209059)
    # save_file('qidian_json_test.json', json_file)
    # print(json_file)

    # 打开一个章节并保存
    # html = urllib.request.urlopen('https://read.qidian.com/chapter/ODKTpdJbs5dgi2M3GqM4mg2/38aRKekByqaaGfXRMrUjdw2')
    # save_file('qidian_test4.html', html.read().decode('utf8'))

    # # 查找章节信息g_data.chapter
    # t = open_file('qidian_test4.html')
    # req = re.compile('g_data.chapter = (\{.*?\})', re.S)
    # text = re.findall(req, t)
    # text = text[0]
    # print(text)
    # print('------------')
    # reeq = re.compile('//.*\n')
    # text = reeq.sub('', text)
    # print(text)
    # text = text.replace('\n', '')
    # text = text.replace(' ', '')
    # # parm = text.split(',')
    # # print(parm)
    # text2json = json.loads(text)
    # print(text2json)

    # #匹配全部
    # req = ('<a href=.*?data-cid="(.*?)" title=".*?">(.*?)</a>')
    # req = re.compile(req.re.S)
    # text = re.findall(req,html)
    # text = text[0]

    # t = get_qidian_json(1009996289)
    # print(t)
    pass

test('')