# -*- coding：utf-8 -*-
# http://www.23wx.cm/24/24151/index.html
from common import *

__all__ = ['get_23wx_info', "parss_23wx_text"]
host_url = r'https://www.23wx.cm'
mode_name = '23wx'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}


def get_23wx_info(url):
    html = open_html_nogzip(url, 'gbk')
    c_url = url[:url.rfind('/')+1]
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        book_name = metaSoup.select_one('#info > h1').text
        book_acter = metaSoup.select_one('#info > div.options > span.item.red').text
        book_acter = book_acter[book_acter.find('：')+1:]
        catalog_dl = metaSoup.select_one('#main > div.box.mt10 > div.book_list > ul')
        l = list()
        dd = catalog_dl.findAll('li')
        for j in dd:
            chapter = str(j.a.text)
            url = c_url + str(j.a['href'])
            id = -1
            p = url.rfind('/')
            if p > 0:
                id = url[p + 1:-5]
            l.append({'chapter': chapter, 'url': url, 'id': id})
        book_info['name'] = book_name
        book_info['auteur'] = book_acter
        book_info['catalog'] = l
    except Exception as e:
        print('get_%s_info BeautifulSoup error::%s' % (mode_name, str(e)))
        pass
    return book_info


def parss_23wx_text(text):
    try:
        html = text
        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('#htmlContent')
        t = textSoup.prettify()
        t = t[:t.rfind('<br>')]
        tSoup = BeautifulSoup(t, "html.parser")
        text = tSoup.get_text()
    except Exception as e:
        print('parss_%s_text error:%s' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_23wx_info
get_text = parss_23wx_text
mode_info = print_mode_info


def test(url=''):
    print('test %s url=%s' % (print_mode_info(), url))
    info = get_info(url)
    print(info)
    print(get_text(post_html(info['catalog'][0]['url'])))
    pass

#test('http://www.23wx.cm/24/24151/index.html')
