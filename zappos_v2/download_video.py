"""
    download video from url
"""
import os
from urllib import request
from urllib.error import ContentTooShortError
from urllib.error import HTTPError

from zappos_v2.crawler_1st import cursor, db, id_info_table


def download_video(db_row: tuple):
    pre_url = 'https://www.zappos.com/media/video/replace_chars.mp4'
    product_id, category, brand = str(db_row[0]), db_row[1], db_row[2]

    print(category + ' - ' + brand + ' - ' + product_id)

    replace_chars = product_id[0] + '/' + product_id[1] + '/' + product_id[2] + '/' + product_id
    # for mac
    output_dir = '/Users/gbzhu/data/sap_data/video_v2/' + category + '/' + brand + '/' + 'video' + '/'

    # for windows
    # output_dir = 'C://Users//I342202//Desktop//video_v2//' + category + '//' + brand + '//' + 'video' + '//'

    # linux
    # output_dir = '/home/I342202/video_v2/' + category + '/' + brand + '/' + 'video' + '/'

    url = pre_url.replace('replace_chars', replace_chars)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    video_path = output_dir + product_id + '.mp4'
    if os.path.exists(video_path):
        print('exist')
    else:
        try:
            request.urlretrieve(url, video_path)
        except ContentTooShortError:
            print('this video interrupted')
            sql = "update " + id_info_table + " set video_tag=2 where product_id=" + product_id
            cursor.execute(sql)
            db.commit()
            return None
        except HTTPError:
            print('url 404')
            sql = "update " + id_info_table + " set video_tag=404 where product_id=" + product_id
            cursor.execute(sql)
            db.commit()
            return None
        sql = "update " + id_info_table + " set video_tag=1 where product_id=" + product_id
        cursor.execute(sql)
        db.commit()


if __name__ == '__main__':
    sql = "select product_id,category ,brand from " + id_info_table + " where isdownload=1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        download_video(db_row=row)
    cursor.close()
    db.close()
