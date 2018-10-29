import urllib3
from urllib3 import PoolManager
http = urllib3.PoolManager()  # type: PoolManager
import cv2
import numpy as np
import os


def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
    neg_image_urls = http.request('GET', neg_images_link).data.decode('utf-8')
    pic_num = 1

    if not os.path.exists('neg'):
        os.makedirs('neg')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            r = http.request('GET',i,preload_content=False)
            with open("neg/" + str(pic_num) + ".jpg",'wb') as out:
                while True:
                    data = r.read()
                    if not data:
                        break
                    out.write(data)
            r.release_conn()
            img = cv2.imread("neg/" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/" + str(pic_num) + ".jpg", resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))


store_raw_images()
