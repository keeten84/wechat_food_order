# _*_ coding: utf-8 _*_
# @File  : base_settings.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/3
# @Desc  : 用于配置项目的所有公共部分服务器端的配置



# 服务器端口
SERVER_PORT = 5000

# 默认debug模式为关闭
DEBUG = False

SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "shike_food_order"


# 自定义一些需要过滤不需要检测对url相对路径
IGNORE_URLS = [
    "^/user/login",
    "^/api"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
]


PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}

MINI_APP = {
    'appid':'wx562d223ab4b0869d',
    'appkey':'8697ee1021cdeb7308ce126c6cd74cf6'
}

# 上传图片的相关配置
UPLOAD = {
    'ext': ['jpg','gif','bmp','jpeg','png','JPG','GIF','BMP','JPEG','PNG'],
    'perfix_path':'/web/static/upload/',
    'perfix_url':'static/upload/'
}



APP = {
    'domain': 'http://0.0.0.0:8999/'

}