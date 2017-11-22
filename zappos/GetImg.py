# -*- coding: utf-8 -*-
'''
download pictures
@auther  wiki zhu
'''
import os
from urllib.request import urlopen
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
import platform

print(platform.platform())

browserPath = 'C:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
outputDir = 'C:\\Users\\menShoes'
parser = 'html5lib'
driver = webdriver.PhantomJS(executable_path=browserPath)

# define db information
db = pymysql.connect("localhost", "root", "root", "zappos")
cursor = db.cursor()
# for women
# id_img_url_table = 'women_id_img_url'


# for men
id_img_url_table = 'men_id_img_url'


def third_crawler():
    '''
    三级爬虫，根据数据库中url下载图片
    '''
    # 从数据库中拿到图片的下载信息
    cursor.execute("select id,imgurl,isdownload from " + id_img_url_table)
    temp_id_img_url_dict = cursor.fetchall()
    for row in temp_id_img_url_dict:
        id = str(row[0])
        imgurl = row[1]
        isdownload = row[2]
        print(id)
        # 图片没有被下载过
        if isdownload == 0:

            print(id + ": begin")

            try:
                driver.get(imgurl)
                bs_obj = BeautifulSoup(driver.page_source, parser)
                span = bs_obj.find(id='angle-3').contents[1]
                pre1_target_img = span['style']
                pre1_target_img = str(pre1_target_img)
                pre2_target_img = pre1_target_img.split('(')[1]
                target_img = pre2_target_img.replace('_THUMBNAILS', '').replace(')', '')
                data = urlopen(target_img).read()
                img_name = outputDir + "/" + id + ".png"
                with open(img_name, 'wb') as f:
                    f.write(data)
                print(id + ": end")
                cursor.execute("update " + id_img_url_table + " set isdownload=1 WHERE id=" + id)
                db.commit()
            except Exception:
                cursor.execute("update " + id_img_url_table + " set isdownload=2 WHERE id=" + id)
                db.commit()
                continue
            except RuntimeError:
                cursor.execute("update " + id_img_url_table + " set isdownload=2 WHERE id=" + id)
                db.commit()
                continue
            except ReferenceError:
                continue


if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    while (True):
        third_crawler()
        print("Done")
        cursor.close()
        db.close()
