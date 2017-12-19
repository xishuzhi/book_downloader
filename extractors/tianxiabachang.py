# -*- coding：utf-8 -*-
# http://www.tianxiabachang.cn/1_1107/

from common import *
__all__ = ['get_tianxiabachang_info',"parss_tianxiabachang_text"]


catalog_list = list()
book_info = {'name': '','auteur': '', 'catalog':catalog_list}


def get_tianxiabachang_info(url):
    try:
        fp = request.urlopen(url)
        html = fp.read().decode('gb2312', 'ignore')
    except Exception as ea:
        print('get_tianxiabachang_info op url error:' + str(ea))
    # html = open_file(url)
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        book_name = metaSoup.select_one('#info > h1').text
        book_acter = metaSoup.select_one('#info').text
        book_acter = book_acter[book_acter.find('者：') + 2:]
        book_acter = book_acter[:book_acter.find('\n')]
        catalog_dl = metaSoup.select_one('#list > dl')
        l = list()
        dd = catalog_dl.findAll('dd')
        count = 9
        for j in dd:
            if count > 0:
                count -= 1
                continue
            chapter = str(j.a.text)
            url = r'http://www.tianxiabachang.cn' + str(j.a['href'])
            id = -1
            p = url.rfind('/')
            if p > 0:
                id = url[p + 1:-5]
            l.append({'chapter': chapter, 'url': url, 'id': id})
        book_info['name'] = book_name
        book_info['auteur'] = book_acter
        book_info['catalog'] = l
    except Exception as e:
        print('get_tianxiabachang_info BeautifulSoup error:::'+str(e))
        pass

    return book_info


def parss_tianxiabachang_text(text):
    try:
        html = text

        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('#content')
        text = textSoup.get_text()
        text = replace_block(text)
        text = '\n' + text
    except Exception as e:
        print('parss_tianxiabachang_text error:'+str(e))
        return '', html
    return text, ''


def print_mode_info():
    return "这是tianxiabachang模块"

get_info = get_tianxiabachang_info
get_text = parss_tianxiabachang_text
mode_info = print_mode_info


def test(url=''):
    print('test:' + print_mode_info() + ":" + url)
    # print(get_info(r'http://www.tianxiabachang.cn/1_1107/'))
    # print(get_text(open_file('tianxiabachang_v1.html')))
    # 'http://www.tianxiabachang.cn/1_1107/147691.html'
    # txt = get_html('http://www.tianxiabachang.cn/1_1107/147691.html','gb2312')
    # print('\n\n\n\n\n\n\n\n\n\n---------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n')
    # print(get_text(txt))
    pass

# test()


# print(parss_tianxiabachang_text(post_html('http://www.tianxiabachang.cn/1_1107/87802.html')))