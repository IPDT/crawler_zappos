# -*- coding: utf-8 -*-
"""
find duplicated files by comparing MD5
need one parameter: the folder path
1. firstly check size
2. check md5 when size equals
Created on Fri Jun 23 16:17:00 2017
@author: aaran wang

find duplicated picture then update the datebase.
@modifier wiki zhu

"""
import hashlib
import os
from time import clock as now
import pymysql

# initial datebase connection
db = pymysql.connect("localhost", "root", "root", "zappos")
cursor = db.cursor();


def getmd5(filename):
    """
    Get MD5 of file
    :param filename: the full path of the file
    :return: MD5 of file
    """
    file_txt = open(filename, 'rb').read()
    m = hashlib.md5(file_txt)
    return m.hexdigest()


def main():
    # get folder
    path = input("path: ")
    all_sizes = {}  # file size dictionary: {file_size, [file_path, file_md5]}
    total_files = 0  # count of total files
    total_duplicates = 0  # total number of duplicated files
    time_start = now()
    for file in os.listdir(path):
        total_files += 1
        real_file_path = os.path.join(path, file)
        if os.path.isfile(real_file_path):
            file_size = os.stat(real_file_path).st_size  # calc file size
            name_and_md5 = [real_file_path, '']
            if file_size in all_sizes.keys():  # found equal sized file, need to compare md5
                new_md5 = getmd5(real_file_path)  # calc new file's md5
                if all_sizes[file_size][1] == '':  # old file's md5 is initial
                    all_sizes[file_size][1] = getmd5(all_sizes[file_size][0])  # calc old file's md5
                if new_md5 in all_sizes[file_size]:  # found equal md5
                    print(file, ' duplicated with ', os.path.basename(all_sizes[file_size][0]))
                    file2 = os.path.basename(all_sizes[file_size][0])
                    file1_index = file.replace(".png", '')
                    file2_index = file2.replace(".png", '')
                    cursor.execute(
                        "update id_imgurl set isdownload=3 WHERE id IN (" + file1_index + "," + file2_index + ")")
                    db.commit()

                    total_duplicates += 1
                else:
                    all_sizes[file_size].append(new_md5)  # append new entry with new md5
            else:  # no equal sized file found
                all_sizes[file_size] = name_and_md5  # insert new entry without md5
    time_end = now()
    time_last = time_end - time_start
    print('total files：', total_files)
    print('duplicated files：', total_duplicates)
    print('elapsed time：', time_last, 'seconds')


if __name__ == '__main__':
    main()
    print("Done")
    cursor.close()
    db.close()
