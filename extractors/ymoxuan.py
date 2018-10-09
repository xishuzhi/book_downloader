# -*- coding：utf-8 -*-
# https://www.ymoxuan.com/book/84/84602/index.html
from common import *

__all__ = ['get_ymoxuan_info', "parss_ymoxuan_text"]
host_url = r'https://www.ymoxuan.com'
mode_name = 'ymoxuan'

catalog_list = list()
book_info = {'name': '', 'auteur': '', 'catalog': catalog_list}


def open_url2html(url, code_mode='utf-8', count=0):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, default',
        'Accept-Language': 'zh-CN,zh;q=0.9,q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        # 返回页面内容
        r = requests.get(url, headers=headers, verify=False)
        html = r.text
        html = html.encode(r.encoding)
    except Exception as e:
        print('open_html页面打开失败：[%s] error：%s' % (url, e))
        if count > 5:
            return '404'
        return open_url2html(url, count+1)
    return html


def get_ymoxuan_info(url):
    html = open_url2html(url)
    host_head = url[:-10]
    book_name = ''
    book_acter = ''
    l = list()
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        tag = metaSoup.find('ul', class_='mulu')
        li_tags = tag.findAll('li', class_='col3')
        book_name = metaSoup.find('ul', class_='clearfix')
        names = book_name.findAll('a')
        for i in names:
            furl = i['href']
            p = furl.find('_')
            if p > 0:
                # furl = furl[p + 1:-5]
                book_name = i.string
                # print('小说名称：' + i.string + furl)

        # 跳过最新更新章节，这里跳过9章
        skip_start = 0
        skip_number = 9
        for j in li_tags:
            if skip_start < skip_number:
                skip_start = skip_start + 1
                continue
            try:
                chapter = str(j.a.text)
                hf = j.a['href']
                id = -1
                p = hf.rfind('/')
                if p > 0:
                    id = hf[p + 1:-5]
                u = host_head + id + '.html'
                l.append({'chapter': chapter, 'url': u, 'id': id})
                print("章节："+chapter+"，id："+id+'，url：'+u)
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


def parss_ymoxuan_text(html):
    try:
        metaSoup = BeautifulSoup(html, "html.parser")
        tag = metaSoup.find('div', class_='content')
        t = tag.next
        if t.text == 'applyChapterSetting();':
            t.clear()
        text = tag.text
    except Exception as e:
        print('parss_%s_text error:%s' % (mode_name, str(e)))
        return '', html
    return text, ''


def print_mode_info():
    return "这是%s模块" % mode_name

get_info = get_ymoxuan_info
get_text = parss_ymoxuan_text
get_html = open_url2html
mode_info = print_mode_info


def test(url=''):
    # print('test %s url=%s' % (print_mode_info(), url))
    # info = get_info(url)
    # print(info)
    # text, html = get_text(open_88dus_html("https://www.ymoxuan.com/book/84/84602/index.html"))
    metaSoup = BeautifulSoup(open_file('ymoxuan_test0.html'), "html.parser")
    # # text = metaSoup.select_one('body > div.novel > div.yd_text2').text
    # tag = metaSoup.find('ul', class_='mulu')


    # print(book_name.select("li > a"))

    # # 查找目录
    # li_tags = tag.findAll('li', class_='col3')
    # host_head = r'https://www.ymoxuan.com/book/84/84602/'
    # for j in li_tags:
    #     try:
    #         chapter = str(j.a.text)
    #         hf = j.a['href']
    #         u = host_head + str(j.a['href'])
    #         id = -1
    #         p = u.rfind('/')
    #         if p > 0:
    #             id = u[p + 1:-5]
    #         print("章节：" + chapter + "，id：" + id+'，url：'+host_head+id+'.html')
    #     except Exception as e:
    #         # print('a BeautifulSoup error::%s' % (mode_name, str(e)))
    #         pass

    # book_name = metaSoup.find('ul', class_='clearfix')
    # # url = '//www.ymoxuan.com/text_84602.html'
    # # furl = url[:-5]
    # # p = furl.rfind('_')
    # # if p > 0:
    # #     furl = furl[p+1:]
    # # print(furl)
    #
    # # 查找小说名称
    # names = book_name.findAll('a')
    # for i in names:
    #     furl = i['href']
    #     p = furl.find('_')
    #     if p > 0:
    #         furl = furl[p + 1:]
    #         furl = furl[:-5]
    #         print('小说名称：'+i.string+furl)



    # for i in book_name.li.next_siblings:
    #     if isinstance(i, bs4.element.Tag):
    #         print('这个是Tag类型')
    #         if i.has_attr('a') | True:
    #             print('you a')
    #             url = i.a['href']
    #             furl = url[:-5]
    #             p = furl.rfind('_')
    #             if p > 0:
    #                 furl = furl[p + 1:]
    #             print(furl)
    #     if isinstance(i, bs4.element.NavigableString):
    #         print('这个是NavigableString类型')



    # body > section > nav > ul > li: nth - child(3) > a
    # for t in tag.li.next_siblings:
    #     print(t.string)
    # for tt in li_tags:
    #     print(tt.string+'https:'+tt.a['href'])


    # print('tag\n\n\n' + tag.text)

    # tag = metaSoup.find('div', class_='content')
    # t = tag.next
    # if t.text == 'applyChapterSetting();':
    #     t.clear()
    # print('tag\n\n\n'+tag.text)
    # text = metaSoup.find('div', class_='content').text
    # print('text\n\n\n\n'+text)
    # print(type(text))


    # print(get_text(post_html(info['catalog'][0]['url'])))

    # r1 = requests.get('https://www.88dus.com/xiaoshuo/20/20363/11862683.html')
    # save_file('s1.txt', r1.text)
    # r2 = requests.get('https://www.88dus.com/xiaoshuo/20/20363/11862682.html')
    # save_file('s1.txt', r2.text)
    pass

# test('https://www.ymoxuan.com/book/84/84602/index.html')

