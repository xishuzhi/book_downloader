#-*- coding：utf-8 -*-

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
            s_l = str(selection).split(',')
            if len(selection) > 0:
                from common import url_to_module, start_download
                m, url = url_to_module(selection)
                if m is not None:
                    info = m.get_info(url)
                    start_download(m, info)
                else:
                    print("nnnn")
            else:
                print('输入错误！')
        print ('exit')
    except Exception as e:
        print ('Error: %s,%s' % (selection,e))
        return start_main()
    finally:
        pass
def main():
        start_main()

if __name__ == "__main__":
    main()
    # print(".......")
    # from common import url_to_module,start_download
    # m,url = url_to_module(r"https://www.23us.la/html/209/209550/")
    # if m is not None:
    #     #m.test(url)
    #     info = m.get_info(url)
    #     start_download(m,info)
    # else:
    #     print("nnnn")



