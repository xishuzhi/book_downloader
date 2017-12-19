# -*- coding：utf-8 -*-
# https://www.23us.la/html/209/209550/
from common import *

__all__ = ['get_23us_info', "parss_23us_text"]


catalog_list = list()
book_info = {'name': '','auteur': '', 'catalog':catalog_list}


def get_23us_info(url):
    fp = request.urlopen(url)
    html = fp.read()
    # html = open_file("23us.txt")
    metaSoup = BeautifulSoup(html, "html.parser")
    book_name = metaSoup.select_one('#container > div.bookinfo > div > span > h1').text
    book_acter = metaSoup.select_one('#container > div.bookinfo > div > span > em').text
    catalog_dl = metaSoup.select_one('#main > div > dl')
    l = list()
    dd = catalog_dl.findAll('dd')
    for j in dd:
        chapter = str(j.a.text)
        url = r'https://www.23us.la'+str(j.a['href'])
        id = -1
        p = url.rfind('/')
        if p > 0:
            id = url[p+1:-5]
        l.append({'chapter':chapter,'url':url,'id':id})
    book_info['name'] = book_name
    book_info['auteur'] = book_acter
    book_info['catalog'] = l
    return book_info


def parss_23us_text(text):
    try:
        html = text
        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('#content')
        t = textSoup.prettify()
        t = t[:t.rfind('<br>')]
        tSoup = BeautifulSoup(t, "html.parser")
        text = tSoup.get_text()
    except Exception as e:
        print('parss_23us_text error:'+str(e))
        return '', html
    return text, ''

def print_mode_info():
    return "这是23us.la模块"

get_info = get_23us_info
get_text = parss_23us_text
mode_info = print_mode_info


def test(url):
    # print('test:' + print_mode_info() + ":" + url)
    # print(get_23us_info(url))
    print(parss_23us_text(open_file('23us_v1.txt')))
    # parss_23us_text(open_file('23us_v1.txt'))

# print(get_text(post_html('https://www.23us.la/html/209/209550/1475699.html')))
