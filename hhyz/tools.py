# encoding=utf-8
import requests
import hashlib
from qiniu import Auth, put_data

q = Auth('zivi19IhtL_jqlJAlW0Wz6oJR_nrKHTenS8dZMnu',
         'OKWfsVdwI9nUQ7n7ykc7gvm4PAFEVoQl7CJxnzY3')
baseurl = 'http://7xqubs.com1.z0.glb.clouddn.com'
token = q.upload_token('hhyz')


# 上传图片,并返回图片地址
def get_img_path(url):
    img = requests.get(url)
    md5 = hashlib.md5()
    md5.update(img.content)
    key = md5.hexdigest()
    put_data(token, key, img.content)
    return baseurl + '/' + key


def is_low_price(title):
    num = u''
    flag = False
    for c in title:
        if c >= '0' and c <= '9' or c == '.':
            num += c
            if not flag:
                flag = True
        else:
            if flag:
                break
    if float(num) <= 10.0:
        return True
    else:
        return False
