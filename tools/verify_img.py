"""
    verify whether the picture is complete

"""
import os
from PIL import Image

img_dir = '/Users/gbzhu/Desktop/picture_v0.1/'


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
                print(imgs_path + ' : ' + str(imgs_num))
                brand_num += imgs_num
                for img in imgs:
                    img_path = os.path.join(imgs_path, img)
                    try:
                        Image.open(img_path).verify()
                    except:
                        print(img_path)
                        return None
            print(category + ' : ' + brand + ' : ' + str(brand_num))
            category_num += brand_num
        print(category + ' : ' + str(category_num))


if __name__ == '__main__':
    verify_img(img_dir=img_dir)
