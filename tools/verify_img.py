"""
    verify whether the picture is complete

"""
import os
from PIL import Image

img_dir = 'C://Users\I342202\Desktop\server_backup\picture_v2'


def verify_img(img_dir: str):
    for category in os.listdir(img_dir):
        category_num = 0
        brands = os.path.join(img_dir, category)

        for brand in os.listdir(brands):
            brand_num = 0
            angles = os.path.join(brands, brand)
            for angle in os.listdir(angles):
                imgs_path = os.path.join(angles, angle)
                imgs = os.listdir(imgs_path)
                imgs_num = len(imgs)
                # print(imgs_path + ' : ' + str(imgs_num))
                brand_num += imgs_num
                for img in imgs:
                    img_path = os.path.join(imgs_path, img)
                    if not IsValidImage(img_path):
                        print(img_path)
            print(category + ' : ' + brand + ' : ' + str(brand_num))
            category_num += brand_num
        print(category + ' : ' + str(category_num))


def IsValidImage(file):
    bValid = True
    fileObj = open(file, 'rb')
    buf = fileObj.read()
    if buf[6:10] in (b'JFIF', b'Exif'):  # jpg图片
        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
            bValid = False
    else:
        try:
            Image.open(fileObj).verify()
        except:
            bValid = False
    return bValid


if __name__ == '__main__':
    verify_img(img_dir=img_dir)
