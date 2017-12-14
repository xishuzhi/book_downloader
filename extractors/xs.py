#-*- coding：utf-8 -*-
#https://www.xs.la/184_184338/

__all__ = ['get_xs_info',"parss_xs_text"]
from common import *

catalog_list = list()
book_info = {'name': '','auteur': '', 'catalog':catalog_list}

def get_xs_info(url):
    # fp = request.urlopen(url)
    # html = fp.read()
    html = open_file("xs.txt")
    metaSoup = BeautifulSoup(html, "html.parser")
    book_name = metaSoup.select_one('#info > h1').text
    book_acter = metaSoup.select_one('#info').text
    book_acter = book_acter[book_acter.find('者：')+2:]
    book_acter = book_acter[:book_acter.find('\n')]
    catalog_dl = metaSoup.select_one('#list > dl')
    l = list()
    dd = catalog_dl.findAll('dd')
    for j in dd:
        chapter = str(j.a.text)
        url = r'https://www.xs.la'+str(j.a['href'])
        id = -1
        p = url.rfind('/')
        if p > 0:
            id = url[p+1:-5]
        l.append({'chapter':chapter,'url':url,'id':id})
    book_info['name'] = book_name
    book_info['auteur'] = book_acter
    book_info['catalog'] = l
    return book_info

def parss_xs_text(text):
    html = text
    metaSoup = BeautifulSoup(html, "html.parser")
    textSoup = metaSoup.select_one('#content')
    t = textSoup.prettify()
    t = t[:t.rfind('<br>')]
    tSoup = BeautifulSoup(t, "html.parser")
    #print(tSoup.get_text())
    text = tSoup.get_text()
    return text

def download_book():
    pass
def print_mode_info():
    return "这是xs.la模块"

get_info = get_xs_info
get_text = parss_xs_text
mode_info = print_mode_info


def test(url=''):
    print('test:' + print_mode_info() + ":" + url)
    # print(get_xs_info(url))
    print(parss_xs_text(open_file('xs_v1.txt')))
    # parss_23us_text(open_file('xs_v1.txt'))
    pass

