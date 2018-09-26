# -*- coding：utf-8 -*-

from common import *


__all__ = ['get_qidiana_catalog',"print_qidian_mode_info"]


def get_qidiana_catalog(url):
    pass


def get_limit_list():
    fp = request.urlopen("https://f.qidian.com/")
    html = fp.read()
    metaSoup = BeautifulSoup(html, "html.parser")
    # print(metaSoup)
    limit_list = metaSoup.find('div', attrs={'id': 'limit-list'})
    # print(limit_list)
    book_info_list = limit_list.findAll('div', attrs={'class': 'book-mid-info'})
    book = []
    for i in book_info_list:
        id_link = i.h4.a['href']
        id = i.h4.a['data-bid']
        #print(id_link.split('/')[-1])
        data = {'name':i.h4.get_text(),'url':'https://book.qidian.com/info/' + id+"#Catalog",'id':id}
        book.append(data)
    #print(book)
    return book


def print_qidian_mode_info():
    return "这是Qidian模块"

#
# BookName
# Author
getCatalog = get_qidiana_catalog
download = getCatalog
get_html = post_html
mode_info = print_qidian_mode_info
