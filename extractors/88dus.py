# -*- coding：utf-8 -*-
# https://www.88dus.com/xiaoshuo/20/20363/
from common import *

__all__ = ['get_88dus_info', "parss_88dus_text"]
host_url = r'https://www.88dus.com'
mode_name = '88dus'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}


# def open_88dus_html(url, code_mode='utf-8', count=0):
#     try:
#         req = request.Request(url)
#         req.add_header('Accept-encoding', 'gzip,deflate,sdch')
#         req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
#                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3033.0 Safari/537.36')
#         # 返回页面内容
#         doc = request.urlopen(req).read()  # python3.x read the html as html code bytearray
#         # 解码
#         try:
#             html = gzip.decompress(doc)
#         except Exception as e_gzip:
#             html = doc.decode(code_mode, 'ignore')
#             # print('返回正常格式的文件:' + str(e_gzip))
#     except Exception as e:
#         print('open_html页面打开失败：[%s] error：%s' % (url, e))
#         if count > 5:
#             return '404'
#         return open_88dus_html(url, count+1)
#     return html


def open_88dus_html(url, code_mode='utf-8', count=0):
    headers = {
        'Connection': 'keep-alive',
        # 'Content-Length': '11',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'DNT': '1',
        'Accept-Encoding': 'gzip, default',
        'Accept-Language': 'zh-CN,zh;q=0.9,q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        # 返回页面内容
        r = requests.get(url, headers=headers, timeout=5)
        html = r.text
        html = html.encode(r.encoding)

    except Exception as e:
        # print('open_html页面打开失败：[%s] error：%s' % (url, e))
        # if count > 5:
        #     return '404'
        # return open_88dus_html(url, count+1)
        print('open_html页面打开失败：[%s]' % (url))
    return html


def get_88dus_info(url):
    html = open_88dus_html(url)
    host_88dus = url
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        book_name = metaSoup.select_one('body > div.jieshao > div.rt > h1').text
        book_acter = metaSoup.select_one('body > div.jieshao > div.rt > div.msg').em.text
        book_acter = book_acter[3:len(book_acter)]
        book_acter = book_acter.rstrip()
        catalog_dl = metaSoup.select_one('body > div.mulu')
        l = list()
        dd = catalog_dl.findAll('li')
        for j in dd:
            try:
                chapter = str(j.a.text)
                u = host_88dus + str(j.a['href'])
                id = -1
                p = u.rfind('/')
                if p > 0:
                    id = u[p + 1:-5]
                l.append({'chapter': chapter, 'url': u, 'id': id})
                print("章节："+chapter+"，id："+id)
            except Exception as e:
                # print('a BeautifulSoup error::%s' % (mode_name, str(e)))
                pass
        book_info['name'] = book_name
        book_info['auteur'] = book_acter
        book_info['catalog'] = l
    except Exception as e:
        print('get_%s_info BeautifulSoup error::%s' % (mode_name, str(e)))
        pass
    return book_info


def parss_88dus_text(html):
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        textSoup = metaSoup.select_one('body > div.novel > div.yd_text2')
        text = textSoup.text
    except Exception as e:
        print('parss_%s_text error:%s' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_88dus_info
get_text = parss_88dus_text
get_html = open_88dus_html
mode_info = print_mode_info


def test(url=''):
    # print('test %s url=%s' % (print_mode_info(), url))
    # info = get_info(url)
    # print(info)
    # text, html = get_text(open_88dus_html("https://www.88dus.com/xiaoshuo/20/20363/11862682.html"))
    metaSoup = BeautifulSoup(open_file('88dus_test2.html'), "html.parser")
    # text = metaSoup.select_one('body > div.novel > div.yd_text2').text
    text = metaSoup.find('div', class_='yd_text2').text
    # text = text[0]
    print(text)
    print(type(text))
    # print(get_text(post_html(info['catalog'][0]['url'])))

    # r1 = requests.get('https://www.88dus.com/xiaoshuo/20/20363/11862683.html')
    # save_file('s1.txt', r1.text)

    r2 = requests.get('https://www.88dus.com/xiaoshuo/20/20363/11862682.html')

    save_file('s1.txt', r2.text)
    pass

test('https://www.88dus.com/xiaoshuo/20/20361/')

