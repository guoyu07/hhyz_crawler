#encoding=utf-8
import requests
import hashlib
from qiniu import Auth,put_data
q=Auth('zivi19IhtL_jqlJAlW0Wz6oJR_nrKHTenS8dZMnu',
       'OKWfsVdwI9nUQ7n7ykc7gvm4PAFEVoQl7CJxnzY3')
baseurl='http://7xqubs.com1.z0.glb.clouddn.com'
token = q.upload_token('hhyz')
md5=hashlib.md5()

# 上传图片,并返回图片地址
def get_img_path(url):
    img=requests.get(url)
    md5.update(img.content)
    key=md5.hexdigest()
    put_data(token,key,img.content)
    return baseurl+'/'+key



print get_img_path('http://imgsrc.baidu.com/forum/w%3D580/sign=d096f1149c16fdfad86cc6e6848f8cea/ccde18fa513d26972e97026254fbb2fb4316d87f.jpg')