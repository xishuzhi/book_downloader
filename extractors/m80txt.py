# -*- coding：utf-8 -*-
# https://m.80txt.com/56121/page-1.html
from common import *
from lxml import etree

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


# 获取所有页面的连接
def get_page_list2(page_text):
    page_url_list = []
    try:
        html = etree.HTML(page_text)
        page_list = html.xpath('//span[@class="middle"]/select/option/@value')

        # 页码计数，从第1页开始
        index = 1
        for page_url in page_list:
            idstring = page_url[:-5]
            point = page_url.find('-')
            page_id = idstring[point + 1:]
            if int(page_id) != index:
                continue
            page_url_list.append((index, host_url + page_url))
            index = index + 1
        # # 去重,会打乱顺序
        # page_url_list = list(set(page_url_list))
        # # 排序
        # page_url_list.sort(key=lambda ele: ele[0])
        # # 访问元组中的数据
        # for url in page_url_list:
        #     print(url[1])
    except Exception as e:
        print('get_%s_page_list error::%s' % (mode_name, str(e)))
    finally:
        return page_url_list

def get_book_list2(page_text):
    book_url_list = []
    try:
        html = etree.HTML(page_text)
        catalog_list = html.xpath('//div[@class="book_last"]/dl/dd/a')
        catalog_url_list = html.xpath('//div[@class="book_last"]/dl/dd/a/@href')
        for c, u in zip(catalog_list, catalog_url_list):
            c_name = c.text
            u_url = host_url + u
            id = -1
            p = u.rfind('/')
            if p > 0:
                id = u[p + 1:-5]
            book_url_list.append({'chapter': c_name, 'url': u_url, 'id': id})
        # print('章节名：' + tag.a.text + ',url=' + host_url + tag.a['href']+',id='+id)
    except Exception as e:
        print('get_%s_book_list2 error::%s' % (mode_name, str(e)))
    finally:
        return book_url_list

def _thread_get_book_catalog(page_url, abl, lock):
    html_src = open_m80txt_html(page_url)
    l = get_book_list2(html_src)
    abl = abl + l
    lock.release()

def get_m80txt_info2(url, only_book_name=False):
    html = open_m80txt_html(url)
    all_bool_list = []
    try:
        page_list = get_page_list2(html)

        book_name = ''
        book_acter = ''

        # 获取书名部分
        book_names = html.xpath('//title')
        book_name = book_names[0].text
        book_name = book_name[:book_name.find('最新章节目录_')]
        # print('书名：' + book_name)


        import _thread
        locks = []
        thread_count = 10
        download_point = 0
        while len(page_list) > download_point:
            if len(locks) < thread_count:
                lock = _thread.allocate_lock()
                lock.acquire()
                locks.append(lock)
                chapter_info = page_list[download_point]
                _thread.start_new_thread(_thread_get_book_catalog, (chapter_info[1], lock))
                download_point = download_point + 1
            check_download_thread(locks)
        while check_download_thread(locks):
            check_download_thread(locks)



        print(page_list)

        for pl in page_list:
            page_html = open_m80txt_html(pl[1])
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

    # # # 获取章节内容 https://m.80txt.com/56121/16518284.html  https://m.80txt.com/79091/25374278.html
    # html = open_m80txt_html('https://m.80txt.com/56121/16742591.html')
    # metaSoup_0 = BeautifulSoup(html, "html.parser")
    # file_text = metaSoup_0.prettify()
    # file_text = file_text.replace('&nbsp;', ' ')
    # # file_text = file_text.replace('a&nbsp;', 'a ')
    # metaSoup_1  = BeautifulSoup(file_text, "html.parser")
    # strong_tag = metaSoup_1.find_all(['head', 'strong', 'a', 'table'])
    # for st in strong_tag:
    #     st.clear()
    # html2 = metaSoup_1.prettify()
    # html3 = html2[html2.find('<div id="nr1">'):html2.find('content2();')]
    # metaSoup_2 = BeautifulSoup(html3, "html.parser")
    # text = metaSoup_2.text
    # print(text)

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

    # # 从网络获取并保存页面
    import urllib
    from lxml import etree
    # url = 'https://m.80txt.com/56121/page-1.html'
    # url_request = urllib.request.Request(url)
    # url_request.add_header('Accept-encoding', 'gzip')
    # url_request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    # url_response = urllib.request.urlopen(url_request)
    # data = url_response.read()
    # html = gzip.decompress(data).decode("utf-8")
    # # print(html)
    # save_file('m80txt_urllib_test.html', html)
    # pass

    # html_src = open_file('m80txt_urllib_test.html')
    # html = etree.HTML(html_src)
    # page_list = html.xpath('//span[@class="middle"]/select/option/@value')
    # catalog_list = html.xpath('//div[@class="book_last"]/dl/dd/a')
    # catalog_url_list = html.xpath('//div[@class="book_last"]/dl/dd/a/@href')
    #
    # # 获取书名部分
    # book_names = html.xpath('//title')
    # book_name = book_names[0].text
    # book_name = book_name[:book_name.find('最新章节目录_')]
    # print('书名：' + book_name)
    #
    # # 连接数组
    # page_url_list = []
    # # 页码计数，从第1页开始
    # index = 1
    # for page_url in page_list:
    #     idstring = page_url[:-5]
    #     point = page_url.find('-')
    #     page_id = idstring[point+1:]
    #     if int(page_id) != index:
    #         continue
    #     page_url_list.append((index, host_url + page_url))
    #     index = index + 1
    #
    # print(page_url_list)
    # # 去重,会打乱顺序
    # page_url_list = list(set(page_url_list))
    # print(page_url_list)
    # # 排序
    # page_url_list.sort(key=lambda ele: ele[0])
    # print(page_url_list)
    # # 访问元组中的数据
    # for url in page_url_list:
    #     print(url[1])

    # for catalog in catalog_list:
    #     print(catalog.text)
    # for c_url in catalog_url_list:
    #     print(host_url + c_url)





    pass

# test('https://m.80txt.com/56121/page-1.html')

