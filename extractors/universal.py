#-*- coding：utf-8 -*-
__all__ = ['get_universal_catalog','get_universal_info','parss_universal_text']
from common import *


catalog_list = list()
book_info = {'name': '', 'catalog':catalog_list}

def get_universal_catalog(url):
    return catalog_list

def get_universal_info():
    return book_info

def parss_universal_text(text):
    return text

def download_book():
    pass
def print_mode_info():
    return "这是universal模块"

get_catalog = get_universal_catalog
get_info = get_universal_info
get_text = parss_universal_text
download = get_catalog
mode_info = print_mode_info


def test(url):
    print('test:'+print_mode_info()+":"+url)