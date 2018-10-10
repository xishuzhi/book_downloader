# -*- coding：utf-8 -*-
# https://m.80txt.com/56121/page-1.html
from common import *

__all__ = ['get_m80txt_info', "parss_m80txt_text"]
host_url = r'https://m.80txt.com'
mode_name = 'm80txt'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}



def open_m80txt_html(url, code_mode='utf-8', count=0):
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
        # print('open_html页面打开失败：[%s] error：%s' % (url, e))
        # if count > 5:
        #     return '404'
        # return open_88dus_html(url, count+1)
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




def get_m80txt_info(url, only_book_name=False):
    html = open_m80txt_html(url)
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
            page_html = open_m80txt_html(pl)
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


def parss_88dus_text(html):
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

get_info = get_m80txt_info
get_text = parss_88dus_text
get_html = open_m80txt_html
mode_info = print_mode_info


def test(url=''):

    # 打开在线页面
    # html = open_m80txt_html('https://m.80txt.com/56121/page-1.html')

    # # 打开本地文件,获取所有章节的页面列表
        # metaSoup = BeautifulSoup(open_file('m80txt_test.html'), "html.parser")
        # page = metaSoup.find('div', class_='listpage')
        # page_list = page.findAll('option')
        # page_url_list = []
        # for tag in page_list:
        #     page_url_list.append(host_url + tag['value'])
        # print(page_url_list)
    # # 函数
        # page_list = get_page_list(open_file('m80txt_test.html'))

    # # 获取章节目录
        # metaSoup = BeautifulSoup(open_file('m80txt_test.html'), "html.parser")
        # page = metaSoup.findAll('dd')
        # for tag in page:
        #     print('章节名：' + tag.a.text +',url=' + host_url + tag.a['href'])
    # # 函数
        # book_list = get_book_list(open_file('m80txt_test.html'))
        # print(book_list)

    # # 获取所有章节列表
        # page_list = get_page_list(open_file('m80txt_test.html'))
        # all_bool_list = []
        # print(page_list)
        # for pl in page_list:
        #     html = open_m80txt_html(pl)
        #     page = get_book_list(html)
        #     print(page)
        #     all_bool_list = all_bool_list + page
        # print(all_bool_list)

    # # 获取章节内容 https://m.80txt.com/56121/16518284.html  https://m.80txt.com/79091/25374278.html
    html = open_m80txt_html('https://m.80txt.com/56121/16742591.html')
    metaSoup_0 = BeautifulSoup(html, "html.parser")
    file_text = metaSoup_0.prettify()
    file_text = file_text.replace('&nbsp;', ' ')
    # file_text = file_text.replace('a&nbsp;', 'a ')
    metaSoup_1  = BeautifulSoup(file_text, "html.parser")
    strong_tag = metaSoup_1.find_all(['head', 'strong', 'a', 'table'])
    for st in strong_tag:
        st.clear()
    html2 = metaSoup_1.prettify()
    html3 = html2[html2.find('<div id="nr1">'):html2.find('content2();')]
    metaSoup_2 = BeautifulSoup(html3, "html.parser")
    text = metaSoup_2.text
    print(text)
    # print(file_text)
    # p = re.compile(r'<a.*</.*>')
    # t = p.sub('', file_text)
    # print(t)
    # '<a&nbsp;href="http://www.qiushu.cc"&nbsp;target="_blank">求书网www.qiushu.Cc</a>'
    # metaSoup = BeautifulSoup(t, "html.parser")
    # # strong_tag = metaSoup.find_all('a &nbsp;')
    # # print(strong_tag)
    # # for st in strong_tag:
    # #     st.clear()
    # strong_tag = metaSoup.find_all(['head', 'strong', 'a ', 'table'])
    # for st in strong_tag:
    #     st.clear()
    # # print('c------------------------')
    # # print(metaSoup)
    # # # strong_taga = metaSoup.findAll('a')
    # # # for sta in strong_taga:
    # # #     print(sta.text)
    # # #     sta.extract()
    # # #
    # # print('text------------------------')
    # html = metaSoup.select_one('#nr')
    # # print(html)
    # text = html.text
    # print('------------------------')
    # print(text)

    # # 获取书名作者
        # metaSoup = BeautifulSoup(open_file('m80txt_test.html'), "html.parser")
        # name_text = metaSoup.select_one('#bqgmb_h1')
        # tmp = name_text.text
        # tmp_list = tmp.split(' ')
        # name = tmp_list[0]
        # print(name)

    pass

# test('https://m.80txt.com/56121/page-1.html')

