"""
    third crawler
    download the picture from url
    auther: wiki

"""

from zappos_v2.crawler_1st import BeautifulSoup, cursor, db, driver, parser, tag_info_table, id_info_table


def third_crawler(sql_row: tuple):

    style_id, product_id, category, brand, url = sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]

    print(category + '->' + brand + ' : ' + style_id)



    return None


if __name__ == '__main__':
    sql = "select style_id,product_id,category,brand,url from " + id_info_table + "where isdownload=0"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        third_crawler(sql_row=row)
        sql = "update " + id_info_table + " set isdownload=1 where style_id=" + row[0]
    cursor.close()
    db.close()
