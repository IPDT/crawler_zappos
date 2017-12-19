import re
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

browserPath = 'C:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'  # 浏览器的地址
driver = webdriver.PhantomJS(executable_path=browserPath)  # 加载浏览器
parser = 'html5lib'  # 解析器

# women's information
# category_list = ['Sandals', 'Heels', 'Sneakers&Athletic', 'Flats', 'Loafers', 'Clogs&Mules', 'Oxfords', 'Slippers']
# homepage_dict = {'Sandals': 'http://www.zappos.com/women-sandals/CK_XARC51wHAAQE.zso',
#                  'Sneakers&Athletic': 'http://www.zappos.com/women-sneakers-athletic-shoes/CK_XARC81wHAAQE.zso',
#                  'Flats': 'http://www.zappos.com/women-flats/CK_XARC11wHAAQE.zso',
#                  'Heels': 'http://www.zappos.com/women-heels/CK_XARC41wHAAQE.zso',
#                  'Loafers': 'http://www.zappos.com/women-loafers/CK_XARC21wHAAQE.zso',
#                  'Clogs&Mules': 'http://www.zappos.com/women-clogs-mules/CK_XARC01wHAAQE.zso',
#                  'Oxfords': 'http://www.zappos.com/women-oxfords/CK_XARC31wHAAQE.zso',
#                  'Slippers': 'http://www.zappos.com/women-slippers/CK_XARC71wHAAQE.zso', }
# all_tag_list = ['Styles', 'Occasion', 'HeelHeight', 'HeelStyle', 'ToeStyle', 'Color', 'Materials', 'Insole',
#                 'Performance', 'Theme', 'Pattern', 'Accents']

# men's information
category_list = ['Sneakers&Athletic', 'Sandals', 'Boots', 'Oxfords', 'Loafers', 'Slippers', 'Boat&Shoes']
homepage_dict = {'Sneakers&Athletic': 'http://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQI.zso',
                 'Sandals': 'http://www.zappos.com/men-sandals/CK_XARC51wHAAQI.zso',
                 'Boots': 'http://www.zappos.com/men-boots/CK_XARCz1wHAAQI.zso',
                 'Oxfords': 'http://www.zappos.com/men-oxfords/CK_XARC31wHAAQI.zso',
                 'Loafers': 'http://www.zappos.com/men-loafers/CK_XARC21wHAAQI.zso',
                 'Slippers': 'http://www.zappos.com/men-slippers/CK_XARC71wHAAQI.zso',
                 'Boat&Shoes': 'http://www.zappos.com/men-boat-shoes/CK_XARCy1wHAAQI.zso'}
all_tag_list = ['Styles', 'Occasion', 'ToeStyle', 'Color', 'Performance', 'Theme']

# define db information
db = pymysql.connect("localhost", "root", "root", "zappos")
cursor = db.cursor()
# for women
# picture_tag_table = 'women_picture_with_tag'
# id_img_url_table = 'women_id_img_url'
# tag_scan_table = 'women_tag_scan'

# for man
picture_tag_table = 'men_picture_with_tag'
id_img_url_table = 'men_id_img_url'
tag_scan_table = 'men_tag_scan'

# 定义数据库中id的集合
db_idList = []
cursor.execute("select id from " + picture_tag_table)
db_id_result = cursor.fetchall()
for row in db_id_result:
    db_idList.append(str(row[0]))
print(len(db_idList))

# 定义图片的id与imgUrl的字典
db_img_id_list = []
cursor.execute("select id from " + id_img_url_table)
db_id_result = cursor.fetchall()
for row in db_id_result:
    db_img_id_list.append(str(row[0]))
print(len(db_img_id_list))

# 找到每个tag是否被scan过
tag_scan = {}
cursor.execute("select tagname,isscan from " + tag_scan_table)
db_tag_scan = cursor.fetchall()
for row in db_tag_scan:
    tag_scan[row[0]] = row[1]

'''
一级爬虫，爬取每个tag对应的url
'''


def main(category, homepage):
    print(category)
    driver.get(homepage)  # 访问目标网页地址
    bs_obj = BeautifulSoup(driver.page_source, parser)  # 解析目标网页的 Html 源码
    # 定义指定tag的基本属性
    tag_info_dict = {}
    # 获取侧边栏的tag
    tag_list = bs_obj.find_all('h4', class_='stripeOuter navOpen')
    for temp in tag_list:
        # 确切的tag类型（Style等）
        tag = temp.get_text().splitlines()[2].lstrip()
        tag = tag.replace(' ', '')
        if tag in all_tag_list:

            print(category + '->' + tag)

            # 定义指定tagname的基本属性
            tag_name_info_dict = {}
            # 获取对应tag的div标签
            div = temp.find_next_sibling("div")
            # 拿到div标签下a标签的集合
            alist = div.find_all('a')
            for a in alist:
                # 取到具体的tag的name和href链接
                a_text = a.get_text().splitlines()[1].lstrip()
                # 去掉空格与引号
                a_text = a_text.replace(' ', '')
                a_text = a_text.replace("'", '')
                # sql = "insert into " + tag_scan_table + "(tagname,isscan)values('" + category + "-" + tag + "-" + a_text + "',0)"
                # cursor.execute(sql)
                # db.commit()
                # 拼接tag的地址
                a_href = 'http://www.zappos.com' + a['href']
                tag_name_info_dict[a_text] = a_href
            tag_info_dict[tag] = tag_name_info_dict
            # 开始二级爬虫
    second_crawler(category, tag_info_dict)


'''
二级爬虫，爬取图片的url
'''


def second_crawler(category, tag_info_dict):
    for tag, tagInfo in tag_info_dict.items():

        print(category + '->' + tag)

        for tagName, tagUrl in tagInfo.items():

            print(category + '->' + tag + '->' + tagName)

            # 判断tagname有没有被scan过
            cate_tag_tag_name = category + "-" + tag + "-" + tagName
            # scan 没有爬过的tag
            if tag_scan[cate_tag_tag_name] == 0:
                try:
                    driver.get(tagUrl)
                    bs_obj = BeautifulSoup(driver.page_source, parser)
                    # 拿到第一页所有tag属性的图片
                    div = bs_obj.find(id='searchResults')
                    a_list = div.find_all('a')
                    print(tag + " -> " + tagName + ": 第1页")
                    # 判断是否有下一页
                    page_index_area = div.find_next_sibling("div", "paginationWrap bottom")
                    texts = page_index_area.get_text()
                    text_list = re.findall("\d+", texts)
                    # 若存在下一页进行循环爬取，获取该tagName下所有图片
                    if len(text_list) > 0:
                        max_page_num = text_list[len(text_list) - 1]
                        for num in range(2, int(max_page_num) + 1):
                            try:
                                print(category + '->' + tag + " -> " + tagName + ": 第" + str(num) + "页")
                                new_tag_url = ''
                                tag_url_list = str(tagUrl).split('/')
                                tag_url_list[0] = tag_url_list[0] + "//"
                                tag_url_list[2] = tag_url_list[2] + "/"
                                tag_url_list[3] = tag_url_list[3] + "-page" + str(num) + "/"
                                for partUrl in tag_url_list:
                                    new_tag_url = new_tag_url + partUrl
                                new_tag_url = new_tag_url + "?p=" + str(num - 1)
                                driver.get(new_tag_url)
                                bs_obj = BeautifulSoup(driver.page_source, parser)
                                child_div = bs_obj.find(id='searchResults')
                                child_a_list = child_div.find_all('a')
                                a_list = a_list + child_a_list
                            except Exception:
                                continue
                            except RuntimeError:
                                continue
                            except ReferenceError:
                                continue
                    # 对对应tagNmae下的图片进行分析
                    for a in a_list:
                        picture_id = a['data-style-id']
                        # 判断图片id是否重复，若重复，需分析tag
                        if picture_id in db_idList:
                            cursor.execute(
                                "select Category," + tag + " from " + picture_tag_table + " where id =" + picture_id)
                            result = cursor.fetchone()
                            db__category = result[0]
                            old__tag_name__value = result[1]
                            db__category = str(db__category)
                            old__tag_name__value = str(old__tag_name__value)
                            new_category = db__category + "/" + category
                            # 要update新的tag
                            if old__tag_name__value == 'None':
                                # 同一个category
                                if db__category.count(category) != 0:
                                    cursor.execute(
                                        "update " + picture_tag_table + " set " + tag + "='" + tagName + "' where id=" + picture_id)
                                    db.commit()
                                    print("only update new tag")
                                # 不同category
                                else:
                                    cursor.execute(
                                        "update " + picture_tag_table + " set Category='" + new_category + "'," + tag + "='" + tagName + "' where id=" + picture_id)
                                    db.commit()
                                    print("update category and new tag")
                            # 要更新老的tag
                            elif old__tag_name__value.count(tagName) == 0 and old__tag_name__value != 'None':
                                new__tag_name__value = old__tag_name__value + "/" + tagName
                                # 同一个category
                                if db__category.count(category) != 0:
                                    cursor.execute(
                                        "update " + picture_tag_table + " set " + tag + "='" + new__tag_name__value + "' where id=" + picture_id)
                                    db.commit()
                                    print("only update old tag")
                                # 不同category
                                else:
                                    cursor.execute(
                                        "update " + picture_tag_table + " set Category='" + new_category + "'," + tag + "='" + new__tag_name__value + "' where id=" + picture_id)
                                    db.commit()
                                    print("update category and old tag")
                            # 不用更新tag
                            elif old__tag_name__value.count(tagName) != 0:
                                # 要更新Category
                                if db__category.count(category) == 0:
                                    cursor.execute(
                                        "update " + picture_tag_table + " set Category='" + new_category + "' where id=" + picture_id)
                                    db.commit()
                                    print("only updata category")
                                # 都不用update
                                else:
                                    pass
                        # 图片id不重复，直接update
                        else:
                            cursor.execute(
                                "insert into " + picture_tag_table + "(id,Category," + tag + ") values(" + picture_id + ",'" + category + "','" + tagName + "')")
                            db.commit()
                            img_url = 'http://www.zappos.com' + a['href']
                            cursor.execute(
                                "insert into " + id_img_url_table + "(id,imgurl,isdownload) values(" + picture_id + ",'" + img_url + "',0)")
                            db.commit()
                            db_img_id_list.append(picture_id)
                            db_idList.append(picture_id)
                            print("insert a new row")
                    cursor.execute(
                        "update " + tag_scan_table + " set isscan=1 WHERE tagname='" + cate_tag_tag_name + "'")
                    db.commit()
                    print("img")
                    print(len(db_img_id_list))
                    print("id")
                    print(len(db_idList))
                except Exception:
                    continue
                except RuntimeError:
                    continue
                except ReferenceError:
                    continue
            else:
                continue


if __name__ == '__main__':
    for index in category_list:
        main(index, homepage_dict.get(index))
    print("Done")
    driver.close()
    cursor.close()
    db.close()
