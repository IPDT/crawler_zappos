"""
    third crawler
    download the picture from url
    auther: wiki

"""

from zappos_v2.crawler_1st import BeautifulSoup, cursor, db, driver, parser, tag_info_table, id_info_table

from urllib import request
from urllib.request import HTTPError
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

angles_list = ['angle-p', 'angle-1', 'angle-2', 'angle-3', 'angle-4', 'angle-5', 'angle-6']


def third_crawler_img(sql_row: tuple):
    style_id, product_id, category, brand, url = sql_row[0], sql_row[1], sql_row[2], sql_row[3], sql_row[4]

    print(category + '->' + brand + ' : ' + str(style_id))

    try:
        # 压缩传输
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(url=req)
        html = response.read()
        compressed_stream = BytesIO(html)
        gzipper = gzip.GzipFile(fileobj=compressed_stream)
        data = gzipper.read()
        bs_obj = BeautifulSoup(data, 'lxml')
    except HTTPError:
        driver.get(url)
        bs_obj = BeautifulSoup(driver.page_source, 'lxml')
    a_s = bs_obj.find_all(name='a', class_='_1B_yd')
    if len(a_s) == 0:
        flag = 'p'
        for angle in angles_list:
            a_ = bs_obj.find(name='a', id=angle)
            a_s.append(a_)
    else:
        flag = '-p'
    if len(a_s) == 0:
        print("don't find pictures (not p and -p)")

        sql = "update " + id_info_table + " set isdownload=2 where style_id=" + str(style_id)
        cursor.execute(sql)
        db.commit()
        return None
    for a in a_s:
        if flag == '-p':
            angle_index = a['data-index']
            img_url = a['href']
        else:
            angle_index = a['data-angle']
            img_url = 'https://luxury.zappos.com' + a['href']

        print('angle: ' + angle_index)

        # for mac
        # output_dir = '/Users/gbzhu/data/sap_data/picture_v2/' + category + '/' + brand + '/' + 'angle-' + angle_index + '/'
        # for windows
        output_dir = 'C://Users//I342202//Desktop//picture_v2//' + category + '//' + brand + '//' + 'angle-' + angle_index + '//'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        img_name = output_dir + str(style_id) + '.jpg'
        if os.path.exists(img_name):

            print('exist')

            continue
        else:
            request.urlretrieve(img_url, img_name)
    sql = "update " + id_info_table + " set isdownload=1 where style_id=" + str(style_id)
    cursor.execute(sql)
    db.commit()


if __name__ == '__main__':
    sql = "select style_id,product_id,category,brand,url from " + id_info_table + " where isdownload=0"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        third_crawler_img(sql_row=row)
    cursor.close()
    db.close()
