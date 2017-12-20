# -*- coding：utf-8 -*-
# http://www.paomov.com/txt90211.shtml
from common import *
__all__ = ['get_pamomov_info', "parss_pamomov_text"]
host_url = r'http://www.paomov.com'
mode_name = 'pamomov'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog' : catalog_list}


def get_pamomov_info(url):
    html = post_html(url)
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        book_name = metaSoup.select_one('body > div > div.catalog > div > div.introduce > h1').text
        book_acter = metaSoup.select_one('body > div > div.catalog > div > div.introduce').a.text
        catalog_dl = metaSoup.select_one('body > div > div.ml_content > div.zb > div.ml_list > ul')
        l = list()
        dd = catalog_dl.findAll('li')
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
        print('get_%s_info BeautifulSoup error:%s' % (mode_name, str(e)))
        pass

    return book_info


def parss_pamomov_text(text):
    try:
        html = text
        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('#nr_content > div.novelcontent')
        text = textSoup.get_text()
        text = replace_block(text)
    except Exception as e:
        print('parss_%s_text error:' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_pamomov_info
get_text = parss_pamomov_text
mode_info = print_mode_info


def test(url=''):
    print('test %s url=%s' % (print_mode_info(), url))
    info = get_info(url)
    print(info)
    print(get_text(post_html(info['catalog'][0]['url'])))
    pass

# test('http://www.paomov.com/txt99026.shtml')



