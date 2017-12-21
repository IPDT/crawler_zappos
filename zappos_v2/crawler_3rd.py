"""
    third crawler
    download the picture from url
    auther: wiki

"""

from zappos_v2.crawler_1st import BeautifulSoup, cursor, db, driver, parser, tag_info_table, id_info_table

from urllib import request
from io import BytesIO
import gzip
import os

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive',
           'Host': 'www.zappos.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}


def third_crawler_img(sql_row: tuple):
    style_id, product_id, category, brand, url = sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]

    print(category + '->' + brand + ' : ' + str(style_id))

    # 压缩传输
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(url=req)
    html = response.read()
    compressed_stream = BytesIO(html)
    gzipper = gzip.GzipFile(fileobj=compressed_stream)
    data = gzipper.read()
    bs_obj = BeautifulSoup(data, 'lxml')
    a_s = bs_obj.find_all(name='a', class_='_1B_yd')
    for a in a_s:
        angle_index = a['data-index']
        print(angle_index)
        img_url = a['href']
        # for mac
        output_dir = '/Users/gbzhu/data/sap_data/picture_v2/' + category + '/' + brand + '/' + 'angle-' + angle_index + '/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        img_name = output_dir + str(style_id) + '.jpg'
        if os.path.exists(img_name):
            continue
        else:
            request.urlretrieve(img_url, img_name)


if __name__ == '__main__':
    sql = "select style_id,product_id,category,brand,url from " + id_info_table + " where isdownload=0"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        third_crawler_img(sql_row=row)
        sql = "update " + id_info_table + " set isdownload=1 where style_id=" + row[0]
    cursor.close()
    db.close()
