# -*- coding：utf-8 -*-

from common import *

__all__ = ['get_universal_catalog', 'get_universal_info', 'parss_universal_text']
host_url = r''
mode_name = 'universal'

catalog_list = list()
book_info = {'name': '', 'catalog': catalog_list}


def get_universal_info():
    return book_info


def parss_universal_text(text):
    return text


def print_mode_info():
    return "这是%s模块" % mode_info


get_info = get_universal_info
get_text = parss_universal_text
get_html = post_html
mode_info = print_mode_info


def test(url=''):
    print('test %s url=%s' % (print_mode_info(), url))
    info = get_info(url)
    print(info)
    print(get_text(post_html(info['catalog'][0]['url'])))
    pass

# test('')
