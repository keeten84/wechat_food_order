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
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
]