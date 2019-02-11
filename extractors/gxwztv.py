# -*- coding：utf-8 -*-
# https://www.gxwztv.com/141/141108/
from common import *
from lxml import etree

__all__ = ['get_gxwztv_info', "parss_gxwztv_text"]
host_url = r'https://www.gxwztv.com'
mode_name = 'gxwztv'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}



def open_gxwztv_html(url, code_mode='utf-8', count=0):
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
        # html = html.encode(r.encoding)

    except Exception as e:
        print('open_html页面打开失败：[%s]' % (url))
    return html


def get_page_list(page_text):
    page_url_list = []
    try:
        metaSoup = BeautifulSoup(page_text, "html.parser")
        page = metaSoup.find('div', class_='listpage')
        page_list = page.findAll('option')
        for tag in page_list:
            page_url_list.append(host_url + tag['value'])
    except Exception as e:
        print('get_%s_page_list error::%s' % (mode_name, str(e)))
    finally:
        return page_url_list


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


def get_gxwztv_info(url, only_book_name=False):
    html = open_gxwztv_html(url)
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        name_text = metaSoup.select_one('#bqgmb_h1')
        tmp = name_text.text
        tmp_list = tmp.split(' ')
        book_name = tmp_list[0]
        if only_book_name:
            return book_name
        book_acter = ''

        page_list = get_page_list(html)
        all_bool_list = []
        print(page_list)
        for pl in page_list:
            page_html = open_gxwztv_html(pl)
            page = get_book_list(page_html)
            print(page)
            all_bool_list = all_bool_list + page
        print(all_bool_list)

        book_info['name'] = book_name
        book_info['auteur'] = book_acter
        book_info['catalog'] = all_bool_list
    except Exception as e:
        print('get_%s_info BeautifulSoup error::%s' % (mode_name, str(e)))
        pass
    return book_info


def parss_gxwztv_text(html):
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

get_info = get_gxwztv_info
get_text = parss_gxwztv_text
get_html = open_gxwztv_html
mode_info = print_mode_info


def test(url=''):
    # # 打开连接并保存为文件
    # url = 'https://www.gxwztv.com/141/141108/168606629.html'
    # html = open_gxwztv_html(url)
    # save_file('gxwztv_test2.html', html)
    # # print(html)
    # html_code = open_file('gxwztv_test.html')
    # html = etree.HTML(html_code)
    # catalog_list = html.xpath('//ul[@id="chapters-list"]/li/a')
    # catalog_url = html.xpath('//ul[@id="chapters-list"]/li/a/@href')
    # # for i in catalog_list:
    # #     print('章节名：'+i.text)
    # # for j in catalog_url:
    # #     print('连接：' + host_url + j)

    html_code = open_file('gxwztv_test2.html')
    file_text = html_code[html_code.find('<div id="txtContent">'):]
    file_text = file_text[:html_code.find('</div>')]
    print(file_text)
    html = etree.HTML(html_code)
    print(html.text)
    pass

test('https://www.gxwztv.com/141/141108/')

