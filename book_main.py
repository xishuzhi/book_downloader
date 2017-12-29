# -*- coding：utf-8 -*-
from sys import exit


def menu():
    print('输入书籍连接下载：')
    print('x. 退出')
    selection = input('输入书籍URL：')
    return selection


def start_main():
    try:
        while True:
            selection = menu()
            if len(selection) > 0:
                if selection == 'x' or selection == 'X':
                    exit(0)
                from common import url_to_module, start_download
                m, url = url_to_module(selection)
                if m is not None:
                    info = m.get_info(url)
                    start_download(m, info)

                else:
                    print("没有相应的下载模块")
            else:
                print('输入错误！')
        print('exit')
    except Exception as e:
        print('Error: %s,%s' % (selection,e))
        return start_main()
    finally:
        pass


def main():
    from os import path
    from common import open_file
    if path.exists('list.txt'):
        download_list = open_file('list.txt').split('\n')
        from common import url_to_module, start_download
        for i in download_list:
            if i[0] == '#':
                continue
            m, url = url_to_module(i)
            if m is not None:
                info = m.get_info(url)
                start_download(m, info)
        exit(0)
        pass
    else:
        start_main()


if __name__ == "__main__":
    main()



