#-*- coding：utf-8 -*-
#https://www.23us.la/html/209/209550/

__all__ = ['get_23us_info',"parss_23us_text"]
from common import *

def get_23us_catalog(url):
    #fp = request.urlopen(url)
    ftext = open("23us.txt",'r',encoding='utf-8')
    #html = fp.read()
    html = ftext.read()
    metaSoup = BeautifulSoup(html, "html.parser")
    #print(metaSoup)
    book_name = metaSoup.select_one('#container > div.bookinfo > div > span > h1').test
    book_acter = metaSoup.select_one('#container > div.bookinfo > div > span > em').test
    catalog_dl = metaSoup.select('#main > div > dl')

    l = list()

    for i in catalog_dl:
        print(type(i))
        dd = i.findAll('dd')
        for j in dd:
            chapter = str(j.a.text)
            url = r'https://www.23us.la'+str(j.a['href'])
            l.append({'chapter':chapter,'url':url})
            print("章节名="+str(j.a.text))
            print("url=" + r'https://www.23us.la'+str(j.a['href']))
    book_info['name'] = book_name
    book_info['auteur'] = book_acter
    book_info['catalog'] = l



catalog_list = list()
book_info = {'name': '','auteur': '', 'catalog':catalog_list}

def get_23us_info(url):
    fp = request.urlopen(url)
    html = fp.read()
    #html = open_file("23us.txt")
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
    return "这是23us.la模块"

get_info = get_23us_info
get_text = parss_23us_text
mode_info = print_mode_info


def test(url):
    # print('test:' + print_mode_info() + ":" + url)
    # print(get_23us_info(url))
    print(parss_23us_text(open_file('23us_v1.txt')))
    # parss_23us_text(open_file('23us_v1.txt'))

