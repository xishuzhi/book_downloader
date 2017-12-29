# -*- coding：utf-8 -*-
#
from common import *

__all__ = ['get_biqugezw_info', "parss_biqugezw_text"]
host_url = r'http://www.biqugezw.com'
mode_name = 'biqugezw'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}


def get_biqugezw_info(url):
    html = open_html_nogzip(url, 'gbk')
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        book_name = metaSoup.select_one('#info > h1').text
        book_acter = metaSoup.select_one('#info > p').text
        book_acter = book_acter[book_acter.find('：')+1:]
        catalog_dl = metaSoup.select_one('#list > dl')
        l = list()
        dd = catalog_dl.findAll('dd')
        for j in dd:
            chapter = str(j.a.text)
            url = host_url + str(j.a['href'])
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


def parss_biqugezw_text(text):
    try:
        html = text
        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('#content')
        t = textSoup.prettify()
        t = t[:t.rfind('<br>')]
        tSoup = BeautifulSoup(t, "html.parser")
        text_list = tSoup.text.split('\n \n\n')
        index = 0
        t = ''
        for j in text_list:
            if index > 0 and index < len(text_list) - 1:
                t += '\n\n    ' + str(j)
            index += 1
        text = t
    except Exception as e:
        print('parss_%s_text error:%s' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_biqugezw_info
get_text = parss_biqugezw_text
mode_info = print_mode_info


def test(url=''):
    print('test %s url=%s' % (print_mode_info(), url))
    info = get_info(url)
    print(info)
    print(get_text(post_html(info['catalog'][0]['url'])))
    pass

#test('http://www.biqugezw.com/15_15701/')