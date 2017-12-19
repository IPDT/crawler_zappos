"""
    second crawler
    get url for every image(image id)
    auther : wiki

"""
import pymysql
from zappos_v2.crawler_1st import BeautifulSoup, cursor, db, driver, parser, tag_info_table, id_info_table
import re


def second_crawler(brand_info, url):
    brand_info = str(brand_info)
    category, brand = brand_info.split('-')[0], brand_info.split('-')[2]

    print(category + '->' + brand)

    # access the url
    driver.get(url=url)
    # parse HTML
    bs_obj = BeautifulSoup(driver.page_source, parser)
    # 拿到第一页所有tag属性的图片
    div = bs_obj.find(id='searchResults')
    try:
        a_list = div.find_all('a')
    # when the brand be sold out
    except AttributeError:
        raise
    print('第1页')
    # 判断是否有下一页
    page_index_area = div.find_next_sibling("div", "paginationWrap bottom")
    texts = page_index_area.get_text()
    text_list = re.findall("\d+", texts)
    # 若存在下一页进行循环爬取，获取该tagName下所有图片
    if len(text_list) > 0:
        max_page_num = text_list[len(text_list) - 1]
        for num in range(2, int(max_page_num) + 1):
            try:

                print("第" + str(num) + "页")

                new_tag_url = ''
                tag_url_list = str(url).split('/')
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
    for a in a_list:
        style_id = a['data-style-id']
        product_id = a['data-product-id']
        img_url = 'http://www.zappos.com' + a['href']
        sql = "insert into " + id_info_table + "(style_id,product_id,category,brand,url,isdownload) values(" + style_id + "," + \
              product_id + ",'" + category + "','" + brand + "','" + img_url + "',0)"
        try:
            cursor.execute(sql)
            db.commit()
        # same picture
        except pymysql.err.IntegrityError:
            continue


if __name__ == '__main__':
    sql = 'SELECT tagname,url FROM ' + tag_info_table + ' where isscan = 0'
    cursor.execute(sql)
    tagname_url = cursor.fetchall()
    for row in tagname_url:
        try:
            second_crawler(row[0], row[1])
        except AttributeError:
            continue
        sql = "update " + tag_info_table + " set isscan=1 where tagname='" + row[0] + "'"
        cursor.execute(sql)
        db.commit()
    cursor.close()
    db.close()
