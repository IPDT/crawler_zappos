"""
    first crawler
    get the url for every detailed tag
    auther : wiki
"""

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

# for mac
# browserPath = '/Users/gbzhu/software/phantomjs-2.1.1-macosx/bin/phantomjs'  # 浏览器的地址

# for windows
# browserPath = 'C:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'  # 浏览器的地址

# for linux
browserPath = '/usr/lib/phantomjs/phantomjs'

driver = webdriver.PhantomJS(executable_path=browserPath)  # 加载浏览器
parser = 'html5lib'  # 解析器

# women's information
category_list = ['Sandals', 'Heels', 'Sneakers&Athletic', 'Flats', 'Loafers', 'Clogs&Mules', 'Oxfords', 'Slippers']
homepage_dict = {'Sandals': 'http://www.zappos.com/women-sandals/CK_XARC51wHAAQE.zso',
                 'Sneakers&Athletic': 'http://www.zappos.com/women-sneakers-athletic-shoes/CK_XARC81wHAAQE.zso',
                 'Flats': 'http://www.zappos.com/women-flats/CK_XARC11wHAAQE.zso',
                 'Heels': 'http://www.zappos.com/women-heels/CK_XARC41wHAAQE.zso',
                 'Loafers': 'http://www.zappos.com/women-loafers/CK_XARC21wHAAQE.zso',
                 'Clogs&Mules': 'http://www.zappos.com/women-clogs-mules/CK_XARC01wHAAQE.zso',
                 'Oxfords': 'http://www.zappos.com/women-oxfords/CK_XARC31wHAAQE.zso',
                 'Slippers': 'http://www.zappos.com/women-slippers/CK_XARC71wHAAQE.zso', }
all_tag_list = ['Brand']

# db information

# for mac
# db = pymysql.connect(host="localhost", user="root", password="gbzhuroot", database="zappos_v2", use_unicode=True,
#                      charset='utf8')

# for windows
# db = pymysql.connect(host="localhost", user="root", passwd="root", db="zappos_v2", use_unicode=True,
#                      charset='utf8')

# for linux
db = pymysql.connect(host="localhost", user="root", passwd="shenqinglengmo", db="zappos_v2", use_unicode=True,
                     charset='utf8')

cursor = db.cursor()

# table information
tag_info_table = 'women_tag_url_isscan'
id_info_table = 'women_id_brand_url_isdownload'


def first_crawler(category, homepage):
    print(category)
    # 访问目标网页地址
    driver.get(homepage)
    # 解析目标网页的 Html 源码
    bs_obj = BeautifulSoup(driver.page_source, parser)
    # 获取侧边栏的tag
    tag_list = bs_obj.find_all('h4', class_='stripeOuter navOpen')
    for temp in tag_list:
        # 确切的tag类型（Style等）
        tag = temp.get_text().splitlines()[2].lstrip()
        tag = tag.replace(' ', '')
        if tag in all_tag_list:

            print(category + '->' + tag)

            # 获取对应tag的div标签
            div = temp.find_next_sibling("div")
            # 拿到div标签下a标签的集合
            alist = div.find_all('a')
            for a in alist:
                # 取到具体的tag的name和href链接
                a_text = a.get_text().splitlines()[1].lstrip()
                a_text = a_text.replace("'", '')
                # 拼接tag的地址
                a_href = 'http://www.zappos.com' + a['href']

                print(category + '->' + tag + '->' + a_text)

                sql = "insert into " + tag_info_table + "(tagname,url,isscan)values('" + category + "-" + tag + "-" + a_text + "','" + a_href + "',0)"
                cursor.execute(sql)
                db.commit()


if __name__ == '__main__':
    for category in category_list:
        first_crawler(category=category, homepage=homepage_dict.get(category))
    driver.close()
    cursor.close()
    db.close()
